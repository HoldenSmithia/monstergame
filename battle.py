"""Battle system."""

import random
import math
from typing import List, Tuple, Optional

try:
    from .entities import Monster, Trainer, Player
    from .data.moves import get_move_data
    from .constants import get_type_multiplier
except ImportError:
    from entities import Monster, Trainer, Player
    from data.moves import get_move_data
    from constants import get_type_multiplier

class BattleAction:
    """Represents a battle action."""
    FIGHT = "fight"
    SWITCH = "switch"
    ITEM = "item"
    RUN = "run"

class BattleResult:
    """Result of a battle."""
    VICTORY = "victory"
    DEFEAT = "defeat"
    ESCAPE = "escape"
    IN_PROGRESS = "in_progress"

class BattleMessage:
    """A message from the battle system."""
    def __init__(self, text: str, type: str = "normal"):
        self.text = text
        self.type = type

class BattleSystem:
    """Handles battle logic."""

    CRITICAL_MULTIPLIER = 1.5
    STAB_MULTIPLIER = 1.5

    def __init__(self, player: Player, opponent: Trainer, is_wild: bool = False):
        self.player = player
        self.opponent = opponent
        self.is_wild = is_wild
        self.player_active = player.active_monster
        self.opponent_active = opponent.active_monster
        self.result = BattleResult.IN_PROGRESS
        self.messages: List[BattleMessage] = []
        self.turn_count = 0
        self.escape_attempts = 0

    def add_message(self, text: str, msg_type: str = "normal"):
        """Add a battle message."""
        self.messages.append(BattleMessage(text, msg_type))

    def get_messages(self) -> List[BattleMessage]:
        """Get and clear messages."""
        msgs = self.messages[:]
        self.messages = []
        return msgs

    def process_turn(self, player_action: Tuple[str, any], opponent_action: Tuple[str, any] = None):
        """Process a full battle turn."""
        self.turn_count += 1

        # If opponent action not provided, AI chooses
        if opponent_action is None:
            opponent_action = self.ai_choose_action()

        # Determine action order based on priority and speed
        actions = [
            (player_action, self.player, self.player_active),
            (opponent_action, self.opponent, self.opponent_active),
        ]

        # Sort by priority first, then speed
        def action_priority(action_tuple):
            action, trainer, monster = action_tuple
            action_type, action_data = action

            # Running has highest priority
            if action_type == BattleAction.RUN:
                return (999, monster.get_modified_stat("speed"))

            # Switching is next
            if action_type == BattleAction.SWITCH:
                return (500, monster.get_modified_stat("speed"))

            # Using items
            if action_type == BattleAction.ITEM:
                return (400, monster.get_modified_stat("speed"))

            # Attacks - check move priority
            if action_type == BattleAction.FIGHT:
                move_idx = action_data
                move = monster.moves[move_idx] if 0 <= move_idx < len(monster.moves) else None
                if move:
                    return (200 + move.priority, monster.get_modified_stat("speed"))

            return (0, monster.get_modified_stat("speed"))

        actions.sort(key=action_priority, reverse=True)

        # Process actions in order
        for action, trainer, monster in actions:
            if self.result != BattleResult.IN_PROGRESS:
                break

            action_type, action_data = action

            if action_type == BattleAction.FIGHT:
                if trainer == self.player:
                    self.execute_attack(self.player_active, self.opponent_active, action_data)
                else:
                    self.execute_attack(self.opponent_active, self.player_active, action_data)
            elif action_type == BattleAction.SWITCH:
                self.execute_switch(trainer, action_data)
            elif action_type == BattleAction.ITEM:
                if trainer == self.player:
                    self.execute_item_use(action_data)
            elif action_type == BattleAction.RUN:
                self.execute_escape(trainer)

        # Check for faints and switch
        self.handle_faints()

        # Check end conditions
        self.check_battle_end()

    def execute_attack(self, attacker: Monster, defender: Monster, move_idx: int):
        """Execute an attack."""
        if move_idx >= len(attacker.moves):
            return

        move = attacker.moves[move_idx]

        # Check PP
        if move.pp <= 0:
            self.add_message(f"{attacker.nickname} has no PP left for {move.name}!")
            move = attacker.moves[0]  # Use struggle

        # Use PP
        move.use()

        # Name display
        attacker_name = f"{attacker.nickname}" if attacker == self.player_active else f"Enemy {attacker.nickname}"
        defender_name = f"{defender.nickname}" if defender == self.player_active else f"Enemy {defender.nickname}"

        self.add_message(f"{attacker_name} used {move.name}!")

        # Check accuracy
        if move.accuracy is not None:
            accuracy = move.accuracy * (attacker.stat_stages.get("accuracy", 0) + 2) / (defender.stat_stages.get("evasion", 0) + 2)
            if random.randint(1, 100) > accuracy:
                self.add_message(f"{attacker_name}'s attack missed!")
                return

        # Status moves
        if move.category == "status":
            self.apply_status_effect(move, attacker, defender)
            return

        # Calculate damage
        damage = self.calculate_damage(attacker, defender, move)

        # Apply damage
        fainted = defender.take_damage(damage)

        # Type effectiveness message
        multiplier = get_type_multiplier(move.type, defender.types[0])
        if len(defender.types) > 1:
            multiplier *= get_type_multiplier(move.type, defender.types[1])

        if multiplier >= 2:
            self.add_message("It's super effective!", "super_effective")
        elif multiplier == 0:
            self.add_message(f"It doesn't affect {defender_name}...", "immune")
            return
        elif multiplier < 1:
            self.add_message("It's not very effective...", "not_effective")

        # Critical hit
        if random.random() < 0.0625:  # 1/16 chance
            damage = int(damage * self.CRITICAL_MULTIPLIER)
            self.add_message("A critical hit!", "critical")

        self.add_message(f"{defender_name} took {damage} damage!")

        # Check faint
        if fainted:
            self.add_message(f"{defender_name} fainted!", "faint")

    def calculate_damage(self, attacker: Monster, defender: Monster, move) -> int:
        """Calculate damage for an attack."""
        if move.power == 0:
            return 0

        # Get attacking and defending stats
        if move.category == "physical":
            attack_stat = attacker.get_modified_stat("attack")
            defense_stat = defender.get_modified_stat("defense")
        else:  # special
            attack_stat = attacker.get_modified_stat("special")
            defense_stat = defender.get_modified_stat("special")

        # Base damage formula
        damage = ((2 * attacker.level / 5 + 2) * move.power * attack_stat / defense_stat) / 50 + 2

        # Apply modifiers
        modifiers = 1.0

        # Type effectiveness
        for def_type in defender.types:
            modifiers *= get_type_multiplier(move.type, def_type)

        # STAB (Same Type Attack Bonus)
        if move.type in attacker.types:
            modifiers *= self.STAB_MULTIPLIER

        # Random factor (85-100%)
        modifiers *= random.randint(85, 100) / 100

        damage = int(damage * modifiers)
        return max(1, damage)

    def apply_status_effect(self, move, attacker: Monster, defender: Monster):
        """Apply a status effect."""
        attacker_name = f"{attacker.nickname}" if attacker == self.player_active else f"Enemy {attacker.nickname}"
        defender_name = f"{defender.nickname}" if defender == self.player_active else f"Enemy {defender.nickname}"

        if move.effect == "lower_attack":
            defender.modify_stat_stage("attack", -1)
            self.add_message(f"{defender_name}'s Attack fell!")
        elif move.effect == "lower_defense":
            defender.modify_stat_stage("defense", -1)
            self.add_message(f"{defender_name}'s Defense fell!")
        elif move.effect == "lower_speed":
            defender.modify_stat_stage("speed", -1)
            self.add_message(f"{defender_name}'s Speed fell!")
        elif move.effect == "raise_defense":
            attacker.modify_stat_stage("defense", 1)
            self.add_message(f"{attacker_name}'s Defense rose!")
        elif move.effect == "sleep":
            defender.set_status("sleep")
            self.add_message(f"{defender_name} fell asleep!")
        elif move.effect == "burn":
            defender.set_status("burn")
            self.add_message(f"{defender_name} was burned!")
        elif move.effect == "paralysis":
            defender.set_status("paralysis")
            self.add_message(f"{defender_name} is paralyzed!")
        elif move.effect == "poison":
            defender.set_status("poison")
            self.add_message(f"{defender_name} was poisoned!")
        elif move.effect == "boost_physical":
            attacker.modify_stat_stage("attack", 1)
            attacker.modify_stat_stage("speed", 1)
            self.add_message(f"{attacker_name}'s Attack and Speed rose!")
        elif move.effect == "boost_special":
            attacker.modify_stat_stage("special", 1)
            attacker.modify_stat_stage("special_defense", 1)
            attacker.modify_stat_stage("speed", 1)
            self.add_message(f"{attacker_name}'s Sp. Atk, Sp. Def, and Speed rose!")

    def execute_switch(self, trainer: Trainer, switch_idx: int):
        """Execute a monster switch."""
        if trainer.switch_monster(switch_idx):
            monster = trainer.active_monster
            name = f"{monster.nickname}" if trainer == self.player else f"Enemy {monster.nickname}"
            self.add_message(f"{trainer.name} sent out {name}!")

            if trainer == self.player:
                self.player_active = monster
            else:
                self.opponent_active = monster

    def execute_item_use(self, item_data):
        """Execute item use (player only)."""
        item_id, target_idx = item_data
        from .data.items import get_item_data

        item = get_item_data(item_id)
        if not item:
            return

        self.add_message(f"Used {item['name']}!")

        if target_idx < len(self.player.team):
            monster = self.player.team[target_idx]

            if item["effect"] == "heal_hp":
                heal_amount = item.get("value", 20)
                monster.heal(heal_amount)
                self.add_message(f"{monster.nickname} recovered HP!")
            elif item["effect"] == "heal_hp_full":
                monster.heal()
                self.add_message(f"{monster.nickname} recovered full HP!")
            elif item["effect"] == "cure_status":
                monster.cure_status()
                self.add_message(f"{monster.nickname} was cured!")
            elif item["effect"] == "revive":
                monster.current_hp = int(monster.stats.hp * item.get("value", 0.5))
                monster.status = None
                self.add_message(f"{monster.nickname} was revived!")

        self.player.remove_item(item_id)

    def execute_escape(self, trainer: Trainer):
        """Attempt to escape from battle."""
        if not self.is_wild:
            self.add_message("Can't escape from trainer battles!")
            return

        self.escape_attempts += 1

        # Escape formula
        player_speed = self.player_active.get_modified_stat("speed")
        opponent_speed = self.opponent_active.get_modified_stat("speed")

        escape_chance = (player_speed * 128 / opponent_speed) + 30 * self.escape_attempts
        escape_chance = min(255, escape_chance)

        if random.randint(0, 255) < escape_chance:
            self.add_message("Got away safely!")
            self.result = BattleResult.ESCAPE
        else:
            self.add_message("Can't escape!")

    def handle_faints(self):
        """Handle fainted monsters and force switches."""
        # Check player monster
        if self.player_active and self.player_active.is_fainted():
            if self.player.has_healthy_monsters():
                self.add_message("Send out another monster?", "prompt")
            else:
                self.result = BattleResult.DEFEAT

        # Check opponent monster
        if self.opponent_active and self.opponent_active.is_fainted():
            if self.opponent.has_healthy_monsters():
                # AI switches
                for i, monster in enumerate(self.opponent.team):
                    if monster.can_battle():
                        self.execute_switch(self.opponent, i)
                        break
            else:
                self.result = BattleResult.VICTORY

    def check_battle_end(self):
        """Check if battle has ended."""
        if not self.player.has_healthy_monsters():
            self.result = BattleResult.DEFEAT
        elif not self.opponent.has_healthy_monsters():
            self.result = BattleResult.VICTORY

    def ai_choose_action(self) -> Tuple[str, any]:
        """AI decides what action to take."""
        # Simple AI: attack with most damaging move
        if not self.opponent_active or self.opponent_active.is_fainted():
            return (BattleAction.SWITCH, 0)

        best_move_idx = 0
        best_damage = 0

        for i, move in enumerate(self.opponent_active.moves):
            if move.pp <= 0:
                continue
            damage = self.calculate_damage(self.opponent_active, self.player_active, move)
            if damage > best_damage:
                best_damage = damage
                best_move_idx = i

        return (BattleAction.FIGHT, best_move_idx)

    def get_reward_exp(self) -> int:
        """Calculate experience reward for winning."""
        if not self.opponent_active:
            return 0

        # Base exp formula - different tiers for different monsters
        base_experience = {
            "ratling": 50, "ratclaw": 145,
            "buzzling": 45, "flutterwing": 178,
            "pebblet": 60, "bouldron": 223,
            "zaprat": 60, "voltiger": 165,
            "spookling": 50, "phantasm": 230,
            "flarion": 62, "pyrethon": 142, "infernoth": 240,
            "aquan": 63, "marinaqua": 142, "leviathan": 239,
            "leaflet": 64, "chloros": 141, "verdanos": 236,
            "drakelet": 102, "drakona": 218, "dragoloth": 306,
        }
        base_exp = base_experience.get(self.opponent_active.id, 100)
        exp = (base_exp * self.opponent_active.level) / 5

        # Multipliers
        if self.is_wild:
            exp *= 1.0
        else:
            exp *= 1.5

        return int(exp)

    def get_reward_money(self) -> int:
        """Calculate money reward."""
        if isinstance(self.opponent, Trainer):
            return self.opponent.prize_money if hasattr(self.opponent, "prize_money") else 0
        return 0
