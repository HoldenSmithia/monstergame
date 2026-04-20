"""Game entities - monsters, player, trainers."""

import random
import math
from dataclasses import dataclass, field
from typing import List, Dict, Optional

try:
    from .constants import exp_for_level, get_type_multiplier
    from .data.monsters import get_monster_data
    from .data.moves import get_move_data
    from .data.items import get_item_data
except ImportError:
    from constants import exp_for_level, get_type_multiplier
    from data.monsters import get_monster_data
    from data.moves import get_move_data
    from data.items import get_item_data

@dataclass
class Stats:
    """Monster stats."""
    hp: int = 0
    attack: int = 0
    defense: int = 0
    speed: int = 0
    special: int = 0

    def copy(self):
        return Stats(self.hp, self.attack, self.defense, self.speed, self.special)

class Move:
    """A move that a monster can learn."""
    def __init__(self, move_id: str):
        data = get_move_data(move_id)
        if not data:
            raise ValueError(f"Unknown move: {move_id}")

        self.id = move_id
        self.name = data["name"]
        self.type = data["type"]
        self.power = data["power"]
        self.accuracy = data["accuracy"]
        self.category = data["category"]  # physical, special, status
        self.pp = data["pp"]
        self.max_pp = data["pp"]
        self.description = data.get("description", "")
        self.priority = data.get("priority", 0)
        self.effect = data.get("effect", None)

    def use(self):
        """Use the move, consuming PP."""
        if self.pp > 0:
            self.pp -= 1
            return True
        return False

    def restore_pp(self, amount=None):
        """Restore PP. If amount is None, restore to max."""
        if amount is None:
            self.pp = self.max_pp
        else:
            self.pp = min(self.max_pp, self.pp + amount)

class Monster:
    """A creature/monster in the game."""

    def __init__(self, monster_id: str, level: int = 1, nickname: str = None):
        data = get_monster_data(monster_id)
        if not data:
            raise ValueError(f"Unknown monster: {monster_id}")

        self.id = monster_id
        self.nickname = nickname or data["name"]
        self.species_name = data["name"]
        self.types = data["types"]
        self.description = data.get("description", "")
        self.level = level

        # Calculate stats
        base_stats = data["base_stats"]
        self.base_stats = Stats(
            hp=base_stats["hp"],
            attack=base_stats["attack"],
            defense=base_stats["defense"],
            speed=base_stats["speed"],
            special=base_stats["special"]
        )

        # IVs (0-31)
        self.ivs = Stats(
            hp=random.randint(0, 31),
            attack=random.randint(0, 31),
            defense=random.randint(0, 31),
            speed=random.randint(0, 31),
            special=random.randint(0, 31)
        )

        # EVs (effort values)
        self.evs = Stats()

        # Calculate actual stats
        self.calculate_stats()

        self.current_hp = self.stats.hp
        self.experience = exp_for_level(level)
        self.experience_to_next = exp_for_level(level + 1)

        # Moves
        self.moves: List[Move] = []
        self.learn_moves_from_level()

        # Status conditions
        self.status = None  # poison, burn, freeze, sleep, paralysis
        self.status_turns = 0

        # Battle stats (temporary modifiers)
        self.stat_stages = {
            "attack": 0,
            "defense": 0,
            "speed": 0,
            "special": 0,
            "accuracy": 0,
            "evasion": 0,
        }

        # Flavor
        self.shiny = random.random() < 0.001  # 1/1000 chance

    def calculate_stats(self):
        """Calculate actual stats based on base, IVs, EVs, and level."""
        def calc_stat(base, iv, ev, is_hp=False):
            if is_hp:
                return math.floor((2 * base + iv + ev / 4) * self.level / 100) + self.level + 10
            else:
                return math.floor((2 * base + iv + ev / 4) * self.level / 100) + 5

        self.stats = Stats(
            hp=calc_stat(self.base_stats.hp, self.ivs.hp, self.evs.hp, True),
            attack=calc_stat(self.base_stats.attack, self.ivs.attack, self.evs.attack),
            defense=calc_stat(self.base_stats.defense, self.ivs.defense, self.evs.defense),
            speed=calc_stat(self.base_stats.speed, self.ivs.speed, self.evs.speed),
            special=calc_stat(self.base_stats.special, self.ivs.special, self.evs.special),
        )

    def learn_moves_from_level(self):
        """Learn moves appropriate for current level."""
        data = get_monster_data(self.id)
        moves_list = data["moves_learned"]

        # Learn up to 4 moves
        self.moves = []
        for move_id in moves_list:
            if len(self.moves) >= 4:
                break
            try:
                self.moves.append(Move(move_id))
            except ValueError:
                pass

    def gain_exp(self, amount: int) -> List[str]:
        """Gain experience. Returns list of messages about level ups and evolutions."""
        messages = []
        self.experience += amount

        while self.experience >= self.experience_to_next:
            self.level_up()
            messages.append(f"{self.nickname} grew to level {self.level}!")

            # Check evolution
            data = get_monster_data(self.id)
            if data.get("evolution") and data["evolution"]["at_level"] <= self.level:
                new_form = data["evolution"]["into"]
                messages.append(f"{self.nickname} is evolving!")
                self.evolve(new_form)
                messages.append(f"{self.nickname} evolved into {self.species_name}!")

        return messages

    def level_up(self):
        """Level up the monster."""
        self.level += 1
        old_max_hp = self.stats.hp
        self.calculate_stats()

        # Heal by the HP gained
        hp_diff = self.stats.hp - old_max_hp
        self.current_hp = min(self.stats.hp, self.current_hp + hp_diff)

        self.experience_to_next = exp_for_level(self.level + 1)

        # Learn new moves
        self.learn_moves_from_level()

    def evolve(self, new_form: str):
        """Evolve into a new form."""
        old_nickname = self.nickname

        # Create new monster data
        data = get_monster_data(new_form)
        self.id = new_form
        self.species_name = data["name"]
        if self.nickname == old_nickname:  # Only update if using default name
            self.nickname = data["name"]
        self.types = data["types"]
        self.description = data.get("description", "")

        # Recalculate stats
        base_stats = data["base_stats"]
        self.base_stats = Stats(
            hp=base_stats["hp"],
            attack=base_stats["attack"],
            defense=base_stats["defense"],
            speed=base_stats["speed"],
            special=base_stats["special"]
        )
        self.calculate_stats()
        self.current_hp = self.stats.hp

    def heal(self, amount: int = None):
        """Heal HP. If amount is None, heal to full."""
        if amount is None:
            self.current_hp = self.stats.hp
        else:
            self.current_hp = min(self.stats.hp, self.current_hp + amount)

    def take_damage(self, damage: int) -> bool:
        """Take damage. Returns True if monster fainted."""
        self.current_hp = max(0, self.current_hp - damage)
        return self.current_hp == 0

    def set_status(self, status: str):
        """Set status condition."""
        if self.status is None and status:
            self.status = status
            self.status_turns = 0

    def cure_status(self):
        """Cure all status conditions."""
        self.status = None
        self.status_turns = 0

    def get_modified_stat(self, stat_name: str) -> int:
        """Get stat with stage modifiers applied."""
        base_value = getattr(self.stats, stat_name)
        stage = self.stat_stages.get(stat_name, 0)

        # Stage multiplier table
        multipliers = {
            -6: 2/8, -5: 2/7, -4: 2/6, -3: 2/5, -2: 2/4, -1: 2/3,
            0: 2/2, 1: 3/2, 2: 4/2, 3: 5/2, 4: 6/2, 5: 7/2, 6: 8/2
        }

        return int(base_value * multipliers.get(stage, 1.0))

    def modify_stat_stage(self, stat: str, change: int):
        """Modify a stat stage."""
        current = self.stat_stages.get(stat, 0)
        self.stat_stages[stat] = max(-6, min(6, current + change))

    def reset_stat_stages(self):
        """Reset all stat stages to default."""
        for stat in self.stat_stages:
            self.stat_stages[stat] = 0

    def is_fainted(self) -> bool:
        """Check if monster has fainted."""
        return self.current_hp == 0

    def get_effective_types(self) -> List[str]:
        """Get types with effectiveness info."""
        return self.types

    def can_battle(self) -> bool:
        """Check if monster can battle."""
        return not self.is_fainted()

    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "id": self.id,
            "nickname": self.nickname,
            "level": self.level,
            "experience": self.experience,
            "current_hp": self.current_hp,
            "moves": [{"id": m.id, "pp": m.pp} for m in self.moves],
            "status": self.status,
            "ivs": {
                "hp": self.ivs.hp,
                "attack": self.ivs.attack,
                "defense": self.ivs.defense,
                "speed": self.ivs.speed,
                "special": self.ivs.special,
            },
            "evs": {
                "hp": self.evs.hp,
                "attack": self.evs.attack,
                "defense": self.evs.defense,
                "speed": self.evs.speed,
                "special": self.evs.special,
            },
            "shiny": self.shiny,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Monster":
        """Create monster from dictionary."""
        monster = cls(data["id"], data["level"], data.get("nickname"))
        monster.experience = data["experience"]
        monster.current_hp = data["current_hp"]
        monster.status = data.get("status")
        monster.shiny = data.get("shiny", False)

        # Restore IVs
        ivs = data.get("ivs", {})
        monster.ivs = Stats(
            hp=ivs.get("hp", random.randint(0, 31)),
            attack=ivs.get("attack", random.randint(0, 31)),
            defense=ivs.get("defense", random.randint(0, 31)),
            speed=ivs.get("speed", random.randint(0, 31)),
            special=ivs.get("special", random.randint(0, 31)),
        )

        # Restore EVs
        evs = data.get("evs", {})
        monster.evs = Stats(
            hp=evs.get("hp", 0),
            attack=evs.get("attack", 0),
            defense=evs.get("defense", 0),
            speed=evs.get("speed", 0),
            special=evs.get("special", 0),
        )

        # Recalculate and restore moves
        monster.calculate_stats()

        # Restore move PP
        moves_data = data.get("moves", [])
        monster.moves = []
        for move_data in moves_data:
            try:
                move = Move(move_data["id"])
                move.pp = move_data.get("pp", move.max_pp)
                monster.moves.append(move)
            except ValueError:
                pass

        return monster

class Trainer:
    """Base class for trainers (player and NPCs)."""

    def __init__(self, name: str, is_player: bool = False):
        self.name = name
        self.is_player = is_player
        self.team: List[Monster] = []
        self.active_monster: Optional[Monster] = None

    def add_monster(self, monster: Monster):
        """Add a monster to the team."""
        if len(self.team) < 6:
            self.team.append(monster)
            if self.active_monster is None and not monster.is_fainted():
                self.active_monster = monster

    def remove_monster(self, index: int) -> Optional[Monster]:
        """Remove a monster from the team."""
        if 0 <= index < len(self.team):
            monster = self.team.pop(index)
            if self.active_monster == monster:
                self.active_monster = next((m for m in self.team if not m.is_fainted()), None)
            return monster
        return None

    def switch_monster(self, index: int) -> bool:
        """Switch to a different monster."""
        if 0 <= index < len(self.team):
            new_monster = self.team[index]
            if not new_monster.is_fainted() and new_monster != self.active_monster:
                self.active_monster = new_monster
                return True
        return False

    def has_healthy_monsters(self) -> bool:
        """Check if trainer has any monsters that can battle."""
        return any(m.can_battle() for m in self.team)

    def get_next_healthy_monster(self) -> Optional[Monster]:
        """Get the next monster that can battle."""
        for monster in self.team:
            if monster.can_battle():
                return monster
        return None

    def heal_all(self):
        """Heal all monsters in the team."""
        for monster in self.team:
            monster.heal()
            monster.cure_status()
            for move in monster.moves:
                move.restore_pp()
            monster.reset_stat_stages()

    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "name": self.name,
            "team": [m.to_dict() for m in self.team],
            "active_idx": self.team.index(self.active_monster) if self.active_monster in self.team else 0,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Trainer":
        """Create trainer from dictionary."""
        trainer = cls(data["name"])
        for monster_data in data.get("team", []):
            try:
                monster = Monster.from_dict(monster_data)
                trainer.add_monster(monster)
            except (ValueError, KeyError):
                pass

        active_idx = data.get("active_idx", 0)
        if 0 <= active_idx < len(trainer.team):
            trainer.active_monster = trainer.team[active_idx]

        return trainer

class Player(Trainer):
    """The player character."""

    def __init__(self, name: str = "Player"):
        super().__init__(name, True)
        self.money = 3000
        self.inventory: Dict[str, int] = {}  # item_id: quantity
        self.badges: List[str] = []
        self.pokedex: Dict[str, bool] = {}  # monster_id: seen/caught
        self.position = (0, 0)
        self.facing = "down"

        # Progress tracking
        self.flags: Dict[str, any] = {}  # For story events

    def add_item(self, item_id: str, quantity: int = 1):
        """Add an item to inventory."""
        if item_id in self.inventory:
            self.inventory[item_id] += quantity
        else:
            self.inventory[item_id] = quantity

    def remove_item(self, item_id: str, quantity: int = 1) -> bool:
        """Remove an item from inventory."""
        if item_id in self.inventory and self.inventory[item_id] >= quantity:
            self.inventory[item_id] -= quantity
            if self.inventory[item_id] == 0:
                del self.inventory[item_id]
            return True
        return False

    def has_item(self, item_id: str, quantity: int = 1) -> bool:
        """Check if player has an item."""
        return self.inventory.get(item_id, 0) >= quantity

    def get_inventory_list(self) -> List[tuple]:
        """Get list of (item_id, quantity) tuples."""
        return list(self.inventory.items())

    def add_money(self, amount: int):
        """Add money."""
        self.money = max(0, self.money + amount)

    def can_afford(self, amount: int) -> bool:
        """Check if player can afford something."""
        return self.money >= amount

    def add_badge(self, badge_name: str):
        """Add a gym badge."""
        if badge_name not in self.badges:
            self.badges.append(badge_name)

    def has_badge(self, badge_name: str) -> bool:
        """Check if player has a badge."""
        return badge_name in self.badges

    def register_monster(self, monster_id: str, caught: bool = False):
        """Register a monster in the Pokedex."""
        if monster_id not in self.pokedex:
            self.pokedex[monster_id] = caught
        elif caught and not self.pokedex[monster_id]:
            self.pokedex[monster_id] = True

    def has_seen(self, monster_id: str) -> bool:
        """Check if player has seen a monster."""
        return monster_id in self.pokedex

    def has_caught(self, monster_id: str) -> bool:
        """Check if player has caught a monster."""
        return self.pokedex.get(monster_id, False)

    def get_pokedex_count(self) -> tuple:
        """Get (seen, caught) counts."""
        seen = len(self.pokedex)
        caught = sum(1 for v in self.pokedex.values() if v)
        return seen, caught

    def set_flag(self, flag: str, value: any = True):
        """Set a story flag."""
        self.flags[flag] = value

    def get_flag(self, flag: str, default: any = False) -> any:
        """Get a story flag value."""
        return self.flags.get(flag, default)

    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        data = super().to_dict()
        data.update({
            "money": self.money,
            "inventory": self.inventory,
            "badges": self.badges,
            "pokedex": self.pokedex,
            "position": self.position,
            "facing": self.facing,
            "flags": self.flags,
        })
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        """Create player from dictionary."""
        player = cls(data["name"])

        # Load team
        for monster_data in data.get("team", []):
            try:
                monster = Monster.from_dict(monster_data)
                player.add_monster(monster)
            except (ValueError, KeyError):
                pass

        active_idx = data.get("active_idx", 0)
        if 0 <= active_idx < len(player.team):
            player.active_monster = player.team[active_idx]

        player.money = data.get("money", 3000)
        player.inventory = data.get("inventory", {})
        player.badges = data.get("badges", [])
        player.pokedex = data.get("pokedex", {})
        player.position = tuple(data.get("position", (0, 0)))
        player.facing = data.get("facing", "down")
        player.flags = data.get("flags", {})

        return player

class GymLeader(Trainer):
    """A gym leader trainer."""

    def __init__(self, name: str, gym_type: str, badge_name: str, prize_money: int):
        super().__init__(name, False)
        self.gym_type = gym_type
        self.badge_name = badge_name
        self.prize_money = prize_money
        self.defeated = False

    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        data = super().to_dict()
        data.update({
            "gym_type": self.gym_type,
            "badge_name": self.badge_name,
            "prize_money": self.prize_money,
            "defeated": self.defeated,
        })
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "GymLeader":
        """Create gym leader from dictionary."""
        leader = cls(data["name"], data["gym_type"], data["badge_name"], data["prize_money"])
        leader.defeated = data.get("defeated", False)

        # Load team
        for monster_data in data.get("team", []):
            try:
                monster = Monster.from_dict(monster_data)
                leader.add_monster(monster)
            except (ValueError, KeyError):
                pass

        return leader
