"""Main game entry point."""

import pygame
import sys
import os
import random
import math

# Import from local package
try:
    from .constants import *
    from .entities import Player, Monster, Trainer, GymLeader
    from .battle import BattleSystem, BattleAction, BattleResult
    from .save_system import SaveSystem
    from .data.monsters import MONSTERS, get_monster_data
    from .data.moves import get_move_data
    from .data.items import ITEMS, get_item_data
except ImportError:
    # Running as standalone script
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from constants import *
    from entities import Player, Monster, Trainer, GymLeader
    from battle import BattleSystem, BattleAction, BattleResult
    from save_system import SaveSystem
    from data.monsters import MONSTERS, get_monster_data
    from data.moves import get_move_data
    from data.items import ITEMS, get_item_data

# Ensure colors are defined (fallback)
try:
    YELLOW
except NameError:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    DARK_GRAY = (64, 64, 64)
    LIGHT_GRAY = (192, 192, 192)
    GREEN = (34, 139, 34)
    LIGHT_GREEN = (144, 238, 144)
    RED = (220, 20, 60)
    BLUE = (30, 144, 255)
    YELLOW = (255, 215, 0)
    ORANGE = (255, 140, 0)
    PURPLE = (147, 112, 219)
    PINK = (255, 105, 180)
    CYAN = (0, 255, 255)
    BROWN = (139, 69, 19)
    PATH_COLOR = (210, 180, 140)
    DARK_BROWN = (101, 67, 33)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Monster Chronicles: Legends of Aetheria")
clock = pygame.time.Clock()

class Game:
    """Main game class."""

    def __init__(self):
        self.state = "menu"  # menu, intro, overworld, battle, dialogue, paused, save_menu
        self.running = True
        self.player = None
        self.save_system = SaveSystem()
        self.battle = None
        self.current_map = None
        self.camera_x = 0
        self.camera_y = 0
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 48)
        self.play_time = 0

        # Story
        self.story_flags = {}
        self.dialogue_queue = []
        self.current_dialogue = None

        # UI
        self.menu_selection = 0
        self.selected_menu_item = 0

        # World
        self.npcs = []
        self.wild_grass = []
        self.heal_spots = []
        self.gyms = []

        # Generate world
        self.generate_world()

    def generate_world(self):
        """Generate the game world."""
        # Create a large world map
        self.world_width = 100
        self.world_height = 100

        # Simple terrain generation
        self.terrain = [["grass" for _ in range(self.world_height)] for _ in range(self.world_width)]

        # Add roads
        for x in range(20, 80):
            self.terrain[x][50] = "road"
        for y in range(20, 80):
            self.terrain[50][y] = "road"

        # Add towns
        self.towns = [
            {"name": "Pallet Village", "x": 20, "y": 20, "gym": None},
            {"name": "Pewter City", "x": 50, "y": 20, "gym": {"type": "rock", "leader": "Brock", "badge": "Boulder"}},
            {"name": "Cerulean City", "x": 80, "y": 20, "gym": {"type": "water", "leader": "Misty", "badge": "Cascade"}},
            {"name": "Vermilion City", "x": 80, "y": 50, "gym": {"type": "electric", "leader": "Lt. Surge", "badge": "Thunder"}},
            {"name": "Celadon City", "x": 50, "y": 50, "gym": {"type": "grass", "leader": "Erika", "badge": "Rainbow"}},
            {"name": "Fuchsia City", "x": 20, "y": 50, "gym": {"type": "poison", "leader": "Koga", "badge": "Soul"}},
            {"name": "Saffron City", "x": 50, "y": 80, "gym": {"type": "psychic", "leader": "Sabrina", "badge": "Marsh"}},
            {"name": "Cinnabar Island", "x": 80, "y": 80, "gym": {"type": "fire", "leader": "Blaine", "badge": "Volcano"}},
        ]

        # Mark towns on terrain
        for town in self.towns:
            for dx in range(-3, 4):
                for dy in range(-3, 4):
                    if 0 <= town["x"] + dx < self.world_width and 0 <= town["y"] + dy < self.world_height:
                        self.terrain[town["x"] + dx][town["y"] + dy] = "town"

        # Wild grass areas
        self.wild_areas = [
            {"x": 30, "y": 30, "width": 15, "height": 10, "monsters": ["ratling", "buzzling"], "levels": (2, 5)},
            {"x": 60, "y": 30, "width": 10, "height": 10, "monsters": ["pebblet", "zaprat"], "levels": (5, 10)},
            {"x": 70, "y": 60, "width": 15, "height": 15, "monsters": ["zaprat", "flutterwing"], "levels": (10, 15)},
            {"x": 30, "y": 70, "width": 10, "height": 10, "monsters": ["spookling", "ratclaw"], "levels": (15, 25)},
        ]

        # Heal spots (Pokemon Centers)
        self.heal_spots = [(22, 22), (52, 22), (82, 22), (82, 52), (52, 52), (52, 82), (22, 52), (82, 82)]

        # Shops
        self.shops = [(24, 22), (54, 22), (84, 22), (84, 52)]

    def new_game(self, player_name: str = "Player", starter_choice: str = "flarion"):
        """Start a new game."""
        self.player = Player(player_name)

        # Give starter monster
        starter = Monster(starter_choice, level=5)
        self.player.add_monster(starter)

        # Give starting items
        self.player.add_item("monster_ball", 5)
        self.player.add_item("potion", 3)

        # Set starting position
        self.player.position = (20, 20)

        # Initialize story
        self.story_flags["game_started"] = True
        self.story_flags["starter_chosen"] = starter_choice

        self.state = "overworld"
        self.play_time = 0

    def load_game(self, slot: int):
        """Load a game."""
        player = self.save_system.load_game(slot)
        if player:
            self.player = player
            self.state = "overworld"
            return True
        return False

    def save_game(self, slot: int) -> bool:
        """Save the game."""
        if self.player:
            return self.save_system.save_game(self.player, slot, self.play_time)
        return False

    def start_battle(self, opponent: Trainer, is_wild: bool = False):
        """Start a battle."""
        self.battle = BattleSystem(self.player, opponent, is_wild)
        self.state = "battle"
        self.menu_selection = 0

    def encounter_wild_monster(self, monster_id: str, level: int):
        """Start a wild monster encounter."""
        wild_monster = Monster(monster_id, level)
        trainer = Trainer("Wild")
        trainer.add_monster(wild_monster)
        self.start_battle(trainer, is_wild=True)

    def check_wild_encounter(self) -> bool:
        """Check if a wild monster should be encountered."""
        px, py = self.player.position

        for area in self.wild_areas:
            if (area["x"] <= px < area["x"] + area["width"] and
                area["y"] <= py < area["y"] + area["height"] and
                self.terrain[px][py] == "grass"):

                # 10% encounter rate per step in grass
                if random.random() < 0.1:
                    monster_id = random.choice(area["monsters"])
                    level = random.randint(*area["levels"])
                    self.encounter_wild_monster(monster_id, level)
                    return True

        return False

    def update(self, dt: float):
        """Update game state."""
        self.play_time += dt

        if self.state == "battle":
            self.update_battle()
        elif self.state == "overworld":
            self.update_overworld()

    def update_overworld(self):
        """Update overworld state."""
        # Camera follows player
        if self.player:
            px, py = self.player.position
            self.camera_x = px * TILE_SIZE - SCREEN_WIDTH // 2
            self.camera_y = py * TILE_SIZE - SCREEN_HEIGHT // 2

    def update_battle(self):
        """Update battle state."""
        if self.battle and self.battle.result != BattleResult.IN_PROGRESS:
            # Battle ended
            if self.battle.result == BattleResult.VICTORY:
                # Award exp and money
                exp = self.battle.get_reward_exp()
                money = self.battle.get_reward_money()

                if exp > 0:
                    messages = self.player.active_monster.gain_exp(exp)
                    for msg in messages:
                        self.show_dialogue(msg)

                if money > 0:
                    self.player.add_money(money)
                    self.show_dialogue(f"Got ${money} for winning!")

                # Check gym leader
                if isinstance(self.battle.opponent, GymLeader):
                    self.battle.opponent.defeated = True
                    self.player.add_badge(self.battle.opponent.badge_name)
                    self.show_dialogue(f"Received the {self.battle.opponent.badge_name} Badge!")

            elif self.battle.result == BattleResult.DEFEAT:
                self.show_dialogue(f"{self.player.name} whited out!")
                # Heal team and return to last heal spot
                self.player.heal_all()

            self.battle = None
            self.state = "overworld"

    def draw(self):
        """Draw the game."""
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "overworld":
            self.draw_overworld()
        elif self.state == "battle":
            self.draw_battle()
        elif self.state == "dialogue":
            self.draw_overworld()
            self.draw_dialogue()
        elif self.state == "save_menu":
            self.draw_save_menu()
        elif self.state == "party":
            self.draw_party_screen()
        elif self.state == "bag":
            self.draw_bag_screen()
        elif self.state == "starter_select":
            self.draw_starter_selection()
        elif self.state == "tips":
            self.draw_tips_screen()

        pygame.display.flip()

    def draw_menu(self):
        """Draw main menu."""
        screen.fill(BLACK)

        # Title
        title = self.large_font.render("MONSTER CHRONICLES", True, YELLOW)
        subtitle = self.font.render("Legends of Aetheria", True, WHITE)

        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))
        screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 220))

        # Menu options
        options = ["New Game", "Load Game", "Quit"]
        for i, option in enumerate(options):
            color = YELLOW if i == self.menu_selection else WHITE
            text = self.font.render(option, True, color)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 350 + i * 50))

        # Instructions
        instr = self.small_font.render("UP/DOWN to select, ENTER to confirm", True, GRAY)
        screen.blit(instr, (SCREEN_WIDTH // 2 - instr.get_width() // 2, 550))

    def draw_overworld(self):
        """Draw the overworld."""
        if not self.player:
            return

        # Fill background
        screen.fill((34, 139, 34))  # Grass green

        # Calculate visible tiles
        start_x = max(0, self.camera_x // TILE_SIZE)
        end_x = min(self.world_width, (self.camera_x + SCREEN_WIDTH) // TILE_SIZE + 1)
        start_y = max(0, self.camera_y // TILE_SIZE)
        end_y = min(self.world_height, (self.camera_y + SCREEN_HEIGHT) // TILE_SIZE + 1)

        # Draw tiles
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                tile_x = x * TILE_SIZE - self.camera_x
                tile_y = y * TILE_SIZE - self.camera_y

                terrain = self.terrain[x][y]

                if terrain == "grass":
                    pygame.draw.rect(screen, (34, 139, 34), (tile_x, tile_y, TILE_SIZE, TILE_SIZE))
                    # Add grass details
                    pygame.draw.circle(screen, (50, 160, 50), (tile_x + 8, tile_y + 20), 3)
                    pygame.draw.circle(screen, (50, 160, 50), (tile_x + 20, tile_y + 15), 3)
                elif terrain == "road":
                    pygame.draw.rect(screen, (139, 69, 19), (tile_x, tile_y, TILE_SIZE, TILE_SIZE))
                elif terrain == "town":
                    pygame.draw.rect(screen, (210, 180, 140), (tile_x, tile_y, TILE_SIZE, TILE_SIZE))

        # Draw towns
        for town in self.towns:
            tx = town["x"] * TILE_SIZE - self.camera_x
            ty = town["y"] * TILE_SIZE - self.camera_y
            pygame.draw.rect(screen, (100, 100, 100), (tx - 32, ty - 32, 96, 96))
            pygame.draw.rect(screen, (70, 70, 70), (tx - 32, ty - 32, 96, 96), 2)
            name_text = self.small_font.render(town["name"], True, WHITE)
            screen.blit(name_text, (tx - 30, ty - 50))

        # Draw heal spots
        for hx, hy in self.heal_spots:
            hpx = hx * TILE_SIZE - self.camera_x
            hpy = hy * TILE_SIZE - self.camera_y
            pygame.draw.rect(screen, (255, 0, 0), (hpx, hpy, TILE_SIZE, TILE_SIZE))
            pygame.draw.circle(screen, WHITE, (hpx + 16, hpy + 16), 10)

        # Draw player
        px = self.player.position[0] * TILE_SIZE - self.camera_x
        py = self.player.position[1] * TILE_SIZE - self.camera_y
        pygame.draw.rect(screen, BLUE, (px + 8, py + 8, 16, 16))
        pygame.draw.rect(screen, WHITE, (px + 8, py + 8, 16, 16), 2)

        # Draw UI overlay
        pygame.draw.rect(screen, (0, 0, 0, 128), (0, 0, SCREEN_WIDTH, 60))

        name_text = self.font.render(f"{self.player.name}", True, WHITE)
        money_text = self.font.render(f"${self.player.money}", True, YELLOW)
        badges_text = self.font.render(f"Badges: {len(self.player.badges)}", True, ORANGE)

        screen.blit(name_text, (10, 10))
        screen.blit(money_text, (200, 10))
        screen.blit(badges_text, (350, 10))

        # Controls hint
        hint = self.small_font.render("WASD/Arrows: Move | SPACE: Menu | ENTER: Interact", True, GRAY)
        screen.blit(hint, (10, SCREEN_HEIGHT - 30))

    def draw_battle(self):
        """Draw battle screen."""
        if not self.battle:
            return

        # Background based on terrain
        screen.fill((100, 100, 150))  # Simple gradient placeholder

        # Draw opponent monster
        if self.battle.opponent_active:
            opp = self.battle.opponent_active
            opp_x = SCREEN_WIDTH - 200
            opp_y = 100

            # Monster sprite (placeholder)
            color = TYPE_COLORS.get(opp.types[0], GRAY)
            pygame.draw.circle(screen, color, (opp_x, opp_y), 60)
            pygame.draw.circle(screen, BLACK, (opp_x, opp_y), 60, 3)

            # Name and HP bar
            name = f"{opp.nickname}"
            if opp != self.battle.opponent.team[0]:  # Show if not first
                name = f"Enemy {name}"

            name_text = self.font.render(name, True, WHITE)
            level_text = self.small_font.render(f"Lv{opp.level}", True, WHITE)
            screen.blit(name_text, (opp_x - 80, opp_y - 100))
            screen.blit(level_text, (opp_x + 20, opp_y - 100))

            # HP bar
            hp_pct = opp.current_hp / opp.stats.hp
            bar_color = GREEN if hp_pct > 0.5 else YELLOW if hp_pct > 0.2 else RED
            pygame.draw.rect(screen, GRAY, (opp_x - 80, opp_y - 80, 160, 15))
            pygame.draw.rect(screen, bar_color, (opp_x - 80, opp_y - 80, int(160 * hp_pct), 15))
            pygame.draw.rect(screen, WHITE, (opp_x - 80, opp_y - 80, 160, 15), 2)

        # Draw player monster
        if self.battle.player_active:
            player_mon = self.battle.player_active
            pm_x = 200
            pm_y = SCREEN_HEIGHT - 250

            color = TYPE_COLORS.get(player_mon.types[0], GRAY)
            pygame.draw.circle(screen, color, (pm_x, pm_y), 60)
            pygame.draw.circle(screen, BLACK, (pm_x, pm_y), 60, 3)

            # Name and HP bar
            name_text = self.font.render(f"{player_mon.nickname}", True, WHITE)
            level_text = self.small_font.render(f"Lv{player_mon.level}", True, WHITE)
            screen.blit(name_text, (pm_x - 80, pm_y + 80))
            screen.blit(level_text, (pm_x + 20, pm_y + 80))

            # HP bar
            hp_pct = player_mon.current_hp / player_mon.stats.hp
            bar_color = GREEN if hp_pct > 0.5 else YELLOW if hp_pct > 0.2 else RED
            pygame.draw.rect(screen, GRAY, (pm_x - 80, pm_y + 110, 160, 15))
            pygame.draw.rect(screen, bar_color, (pm_x - 80, pm_y + 110, int(160 * hp_pct), 15))
            pygame.draw.rect(screen, WHITE, (pm_x - 80, pm_y + 110, 160, 15), 2)

            # HP text
            hp_text = self.small_font.render(f"{player_mon.current_hp}/{player_mon.stats.hp}", True, WHITE)
            screen.blit(hp_text, (pm_x - 80, pm_y + 130))

            # XP bar
            if player_mon.level < 100:
                exp_pct = (player_mon.experience - exp_for_level(player_mon.level)) / (player_mon.experience_to_next - exp_for_level(player_mon.level))
                pygame.draw.rect(screen, DARK_GRAY, (pm_x - 80, pm_y + 150, 160, 8))
                pygame.draw.rect(screen, CYAN, (pm_x - 80, pm_y + 150, int(160 * exp_pct), 8))

        # Battle menu
        menu_rect = pygame.Rect(50, SCREEN_HEIGHT - 200, SCREEN_WIDTH - 100, 180)
        pygame.draw.rect(screen, (30, 30, 50), menu_rect)
        pygame.draw.rect(screen, WHITE, menu_rect, 3)

        # Menu options
        options = ["FIGHT", "BAG", "MONSTERS", "RUN"]
        for i, option in enumerate(options):
            color = YELLOW if i == self.menu_selection else WHITE
            text = self.font.render(option, True, color)
            x = 100 + (i % 2) * 300
            y = SCREEN_HEIGHT - 170 + (i // 2) * 60
            screen.blit(text, (x, y))

        # Show moves if in fight mode
        if hasattr(self, 'show_moves') and self.show_moves and self.battle.player_active:
            moves = self.battle.player_active.moves
            for i, move in enumerate(moves):
                color = YELLOW if i == self.selected_menu_item else WHITE
                move_text = self.font.render(f"{move.name} ({move.pp}/{move.max_pp})", True, color)
                type_text = self.small_font.render(f"Type: {move.type}", True, LIGHT_GRAY)
                x = 80 + i * 180
                y = SCREEN_HEIGHT - 280
                pygame.draw.rect(screen, (50, 50, 70), (x, y, 170, 60))
                screen.blit(move_text, (x + 10, y + 10))
                screen.blit(type_text, (x + 10, y + 40))

    def draw_dialogue(self):
        """Draw dialogue box."""
        if not self.current_dialogue:
            return

        # Dialogue box
        box_rect = pygame.Rect(50, SCREEN_HEIGHT - 180, SCREEN_WIDTH - 100, 150)
        pygame.draw.rect(screen, (20, 20, 40), box_rect)
        pygame.draw.rect(screen, WHITE, box_rect, 3)

        # Text
        text = self.font.render(self.current_dialogue, True, WHITE)
        screen.blit(text, (70, SCREEN_HEIGHT - 150))

        # Continue indicator
        if pygame.time.get_ticks() % 1000 < 500:
            pygame.draw.polygon(screen, YELLOW, [
                (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 50),
                (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 60),
                (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 70)
            ])

    def draw_save_menu(self):
        """Draw save/load menu."""
        screen.fill(BLACK)

        title = self.large_font.render("SAVE / LOAD", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        saves = self.save_system.list_saves()
        for i, save in enumerate(saves):
            y = 150 + i * 150

            if save.get("empty"):
                text = self.font.render(f"Slot {save['slot']}: Empty", True, GRAY)
                screen.blit(text, (100, y))
            else:
                pygame.draw.rect(screen, (50, 50, 50), (80, y - 10, 640, 130))
                pygame.draw.rect(screen, WHITE, (80, y - 10, 640, 130), 2)

                name_text = self.font.render(f"{save['player_name']}", True, YELLOW)
                level_text = self.small_font.render(f"Level: {save['level']}", True, WHITE)
                badges_text = self.small_font.render(f"Badges: {save['badges']}", True, ORANGE)
                time_text = self.small_font.render(f"Time: {save['play_time'] // 60}m", True, GRAY)

                screen.blit(name_text, (100, y))
                screen.blit(level_text, (100, y + 35))
                screen.blit(badges_text, (250, y + 35))
                screen.blit(time_text, (400, y + 35))

            # Highlight selection
            if i == self.menu_selection:
                pygame.draw.rect(screen, YELLOW, (80, y - 10, 640, 130), 4)

        # Instructions
        instr = self.small_font.render("UP/DOWN: Select | ENTER: Load | S: Save | ESC: Back", True, GRAY)
        screen.blit(instr, (SCREEN_WIDTH // 2 - instr.get_width() // 2, SCREEN_HEIGHT - 50))

    def draw_party_screen(self):
        """Draw party management screen."""
        screen.fill((40, 40, 60))

        title = self.large_font.render("PARTY", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))

        if self.player:
            for i, monster in enumerate(self.player.team):
                y = 100 + i * 90

                color = (60, 60, 80) if i == self.menu_selection else (40, 40, 60)
                pygame.draw.rect(screen, color, (50, y, 700, 80))
                pygame.draw.rect(screen, WHITE, (50, y, 700, 80), 2)

                # Monster info
                name_text = self.font.render(f"{monster.nickname}", True, WHITE)
                level_text = self.small_font.render(f"Lv{monster.level}", True, GRAY)

                # HP bar
                hp_pct = monster.current_hp / monster.stats.hp
                bar_color = GREEN if hp_pct > 0.5 else YELLOW if hp_pct > 0.2 else RED
                pygame.draw.rect(screen, DARK_GRAY, (200, y + 40, 200, 15))
                pygame.draw.rect(screen, bar_color, (200, y + 40, int(200 * hp_pct), 15))

                status = monster.status if monster.status else "OK"
                status_text = self.small_font.render(status.upper(), True, RED if status != "OK" else GREEN)

                screen.blit(name_text, (70, y + 15))
                screen.blit(level_text, (70, y + 45))
                screen.blit(status_text, (420, y + 40))

        instr = self.small_font.render("UP/DOWN: Select | ENTER: Switch | ESC: Back", True, GRAY)
        screen.blit(instr, (SCREEN_WIDTH // 2 - instr.get_width() // 2, SCREEN_HEIGHT - 30))

    def draw_bag_screen(self):
        """Draw bag/item screen."""
        screen.fill((40, 60, 40))

        title = self.large_font.render("BAG", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))

        if self.player:
            items = self.player.get_inventory_list()
            categories = {"healing": [], "status": [], "battle": [], "key": [], "other": []}

            for item_id, qty in items:
                item_data = get_item_data(item_id)
                if item_data:
                    cat = item_data.get("category", "other")
                    categories[cat].append((item_id, item_data, qty))

            y = 100
            for cat, cat_items in categories.items():
                if not cat_items:
                    continue

                cat_text = self.font.render(cat.upper(), True, YELLOW)
                screen.blit(cat_text, (50, y))
                y += 40

                for item_id, item_data, qty in cat_items:
                    color = WHITE if y != 100 + self.menu_selection * 35 else YELLOW
                    text = self.small_font.render(f"{item_data['name']} x{qty}", True, color)
                    screen.blit(text, (80, y))
                    y += 35

        instr = self.small_font.render("UP/DOWN: Select | ENTER: Use | ESC: Back", True, GRAY)
        screen.blit(instr, (SCREEN_WIDTH // 2 - instr.get_width() // 2, SCREEN_HEIGHT - 30))

    def handle_input(self, event):
        """Handle input events."""
        if event.type == pygame.QUIT:
            self.running = False

        elif event.type == pygame.KEYDOWN:
            if self.state == "menu":
                self.handle_menu_input(event)
            elif self.state == "overworld":
                self.handle_overworld_input(event)
            elif self.state == "battle":
                self.handle_battle_input(event)
            elif self.state == "dialogue":
                self.handle_dialogue_input(event)
            elif self.state == "save_menu":
                self.handle_save_input(event)
            elif self.state == "party":
                self.handle_party_input(event)
            elif self.state == "bag":
                self.handle_bag_input(event)

    def handle_menu_input(self, event):
        """Handle menu input."""
        if event.key == pygame.K_UP:
            self.menu_selection = max(0, self.menu_selection - 1)
        elif event.key == pygame.K_DOWN:
            self.menu_selection = min(2, self.menu_selection + 1)
        elif event.key == pygame.K_RETURN:
            if self.menu_selection == 0:  # New Game
                self.show_starter_selection()
            elif self.menu_selection == 1:  # Load Game
                self.state = "save_menu"
                self.menu_selection = 0
            elif self.menu_selection == 2:  # Quit
                self.running = False

    def show_starter_selection(self):
        """Show starter selection screen."""
        self.state = "starter_select"
        self.starter_choice = 0
        self.starter_options = [
            {"id": "flarion", "name": "Flarion", "type": "fire", "desc": "The Fire starter. Strong against Grass, weak to Water."},
            {"id": "aquan", "name": "Aquan", "type": "water", "desc": "The Water starter. Strong against Fire, weak to Grass."},
            {"id": "leaflet", "name": "Leaflet", "type": "grass", "desc": "The Grass starter. Strong against Water, weak to Fire."},
        ]

    def handle_overworld_input(self, event):
        """Handle overworld input."""
        if not self.player:
            return

        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.move_player(0, -1)
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.move_player(0, 1)
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.move_player(-1, 0)
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.move_player(1, 0)
        elif event.key == pygame.K_SPACE:
            self.state = "paused"
        elif event.key == pygame.K_RETURN:
            self.interact()
        elif event.key == pygame.K_TAB:
            self.state = "party"
            self.menu_selection = 0
        elif event.key == pygame.K_b:
            self.state = "bag"
            self.menu_selection = 0

    def move_player(self, dx, dy):
        """Move the player."""
        if not self.player:
            return

        new_x = self.player.position[0] + dx
        new_y = self.player.position[1] + dy

        # Check bounds
        if 0 <= new_x < self.world_width and 0 <= new_y < self.world_height:
            # Check if walkable
            terrain = self.terrain[new_x][new_y]
            if terrain not in ["water", "mountain"]:
                self.player.position = (new_x, new_y)

                # Check for wild encounter
                if not self.check_wild_encounter():
                    # Check heal spots
                    if (new_x, new_y) in self.heal_spots:
                        self.player.heal_all()
                        self.show_dialogue("Your team has been healed!")

    def interact(self):
        """Interact with the world."""
        if not self.player:
            return

        px, py = self.player.position

        # Check for NPCs, signs, etc.
        for town in self.towns:
            if abs(town["x"] - px) <= 3 and abs(town["y"] - py) <= 3:
                if town["gym"] and not self.player.has_badge(town["gym"]["badge"]):
                    # Challenge gym leader
                    self.challenge_gym(town["gym"])
                else:
                    self.show_dialogue(f"Welcome to {town['name']}!")
                return

        self.show_dialogue("There's nothing interesting here.")

    def challenge_gym(self, gym_data):
        """Challenge a gym leader."""
        self.show_dialogue(f"Gym Leader {gym_data['leader']} challenges you!")

        # Create gym leader
        leader = GymLeader(gym_data['leader'], gym_data['type'], gym_data['badge'], 1500)

        # Generate team based on player's strongest
        player_max = max(m.level for m in self.player.team)

        if gym_data['type'] == "rock":
            leader.add_monster(Monster("pebblet", level=min(14, player_max)))
            leader.add_monster(Monster("bouldron", level=min(18, player_max + 2)))
        elif gym_data['type'] == "water":
            leader.add_monster(Monster("aquan", level=min(18, player_max)))
            leader.add_monster(Monster("marinaqua", level=min(21, player_max + 2)))
        elif gym_data['type'] == "electric":
            leader.add_monster(Monster("zaprat", level=min(21, player_max)))
            leader.add_monster(Monster("voltiger", level=min(24, player_max + 2)))
        elif gym_data['type'] == "grass":
            leader.add_monster(Monster("leaflet", level=min(29, player_max)))
            leader.add_monster(Monster("chloros", level=min(33, player_max + 2)))

        self.start_battle(leader, is_wild=False)

    def handle_battle_input(self, event):
        """Handle battle input."""
        if not self.battle:
            return

        if hasattr(self, 'show_moves') and self.show_moves:
            # Move selection
            if event.key == pygame.K_LEFT:
                self.selected_menu_item = max(0, self.selected_menu_item - 1)
            elif event.key == pygame.K_RIGHT:
                self.selected_menu_item = min(len(self.battle.player_active.moves) - 1, self.selected_menu_item + 1)
            elif event.key == pygame.K_RETURN:
                action = (BattleAction.FIGHT, self.selected_menu_item)
                self.battle.process_turn(action)
                self.show_moves = False
            elif event.key == pygame.K_ESCAPE:
                self.show_moves = False
        else:
            # Main battle menu
            if event.key == pygame.K_LEFT:
                self.menu_selection = max(0, self.menu_selection - 1)
            elif event.key == pygame.K_RIGHT:
                self.menu_selection = min(3, self.menu_selection + 1)
            elif event.key == pygame.K_UP:
                self.menu_selection = max(0, self.menu_selection - 2)
            elif event.key == pygame.K_DOWN:
                self.menu_selection = min(3, self.menu_selection + 2)
            elif event.key == pygame.K_RETURN:
                if self.menu_selection == 0:  # Fight
                    self.show_moves = True
                    self.selected_menu_item = 0
                elif self.menu_selection == 1:  # Bag
                    self.state = "bag"
                elif self.menu_selection == 2:  # Switch
                    self.state = "party"
                elif self.menu_selection == 3:  # Run
                    action = (BattleAction.RUN, None)
                    self.battle.process_turn(action)

    def handle_dialogue_input(self, event):
        """Handle dialogue input."""
        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            self.advance_dialogue()

    def advance_dialogue(self):
        """Advance to next dialogue."""
        if self.dialogue_queue:
            self.current_dialogue = self.dialogue_queue.pop(0)
        else:
            self.current_dialogue = None
            self.state = "overworld"

    def show_dialogue(self, text: str):
        """Show a dialogue message."""
        self.dialogue_queue.append(text)
        if self.state != "dialogue":
            self.current_dialogue = self.dialogue_queue.pop(0)
            self.state = "dialogue"

    def handle_save_input(self, event):
        """Handle save menu input."""
        if event.key == pygame.K_UP:
            self.menu_selection = max(0, self.menu_selection - 1)
        elif event.key == pygame.K_DOWN:
            self.menu_selection = min(2, self.menu_selection + 1)
        elif event.key == pygame.K_RETURN:
            # Load selected slot
            slot = self.menu_selection + 1
            if self.load_game(slot):
                self.state = "overworld"
            else:
                self.show_dialogue("No save data found!")
        elif event.key == pygame.K_s:
            # Save to selected slot
            if self.player:
                slot = self.menu_selection + 1
                if self.save_game(slot):
                    self.show_dialogue("Game saved!")
                else:
                    self.show_dialogue("Failed to save game.")
        elif event.key == pygame.K_ESCAPE:
            self.state = "overworld"

    def handle_party_input(self, event):
        """Handle party screen input."""
        if event.key == pygame.K_UP:
            self.menu_selection = max(0, self.menu_selection - 1)
        elif event.key == pygame.K_DOWN:
            self.menu_selection = min(len(self.player.team) - 1, self.menu_selection + 1)
        elif event.key == pygame.K_RETURN:
            # Switch to selected monster
            if self.battle and self.state == "battle":
                action = (BattleAction.SWITCH, self.menu_selection)
                self.battle.process_turn(action)
                self.state = "battle"
            else:
                # Summary view would go here
                pass
        elif event.key == pygame.K_ESCAPE:
            if self.battle and self.state == "battle":
                self.state = "battle"
            else:
                self.state = "overworld"

    def handle_bag_input(self, event):
        """Handle bag screen input."""
        if event.key == pygame.K_UP:
            self.menu_selection = max(0, self.menu_selection - 1)
        elif event.key == pygame.K_DOWN:
            total_items = sum(len(v) for v in self.get_categorized_items().values())
            self.menu_selection = min(total_items - 1, self.menu_selection + 1)
        elif event.key == pygame.K_RETURN:
            # Use item
            if self.state == "battle" and self.battle:
                # Get item
                items = []
                for cat_items in self.get_categorized_items().values():
                    items.extend(cat_items)

                if self.menu_selection < len(items):
                    item_id, item_data, qty = items[self.menu_selection]
                    # Use on active monster
                    action = (BattleAction.ITEM, (item_id, 0))
                    self.battle.process_turn(action)
                    self.state = "battle"
        elif event.key == pygame.K_ESCAPE:
            if self.state == "battle" and self.battle:
                self.state = "battle"
            else:
                self.state = "overworld"

    def get_categorized_items(self):
        """Get items organized by category."""
        if not self.player:
            return {}

        categories = {"healing": [], "status": [], "battle": [], "key": [], "other": []}
        for item_id, qty in self.player.get_inventory_list():
            item_data = get_item_data(item_id)
            if item_data:
                cat = item_data.get("category", "other")
                categories[cat].append((item_id, item_data, qty))
        return categories

    def run(self):
        """Main game loop."""
        while self.running:
            dt = clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                self.handle_input(event)

            self.update(dt)
            self.draw()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
