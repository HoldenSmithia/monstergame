"""Save and load game data."""

import json
import os
from datetime import datetime
from typing import Optional

try:
    from .entities import Player, Monster
    from .constants import SAVE_DIR
except ImportError:
    from entities import Player, Monster
    from constants import SAVE_DIR

class SaveSystem:
    """Handles saving and loading game data."""

    def __init__(self):
        # Create save directory if it doesn't exist
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)

    def get_save_path(self, slot: int) -> str:
        """Get the path for a save slot."""
        return os.path.join(SAVE_DIR, f"save_{slot}.json")

    def get_save_info(self, slot: int) -> Optional[dict]:
        """Get info about a save slot without loading full data."""
        path = self.get_save_path(slot)
        if not os.path.exists(path):
            return None

        try:
            with open(path, 'r') as f:
                data = json.load(f)
                return {
                    "player_name": data.get("player", {}).get("name", "Unknown"),
                    "play_time": data.get("play_time", 0),
                    "badges": len(data.get("player", {}).get("badges", [])),
                    "timestamp": data.get("timestamp", ""),
                    "level": max((m.get("level", 1) for m in data.get("player", {}).get("team", [])), default=1),
                }
        except (json.JSONDecodeError, IOError):
            return None

    def save_exists(self, slot: int) -> bool:
        """Check if a save exists."""
        return os.path.exists(self.get_save_path(slot))

    def save_game(self, player: Player, slot: int, play_time: int = 0) -> bool:
        """Save the game to a slot."""
        try:
            data = {
                "version": "1.0",
                "timestamp": datetime.now().isoformat(),
                "play_time": play_time,
                "player": player.to_dict(),
            }

            path = self.get_save_path(slot)
            with open(path, 'w') as f:
                json.dump(data, f, indent=2)

            return True
        except IOError:
            return False

    def load_game(self, slot: int) -> Optional[Player]:
        """Load a game from a slot."""
        path = self.get_save_path(slot)
        if not os.path.exists(path):
            return None

        try:
            with open(path, 'r') as f:
                data = json.load(f)

            player_data = data.get("player")
            if not player_data:
                return None

            return Player.from_dict(player_data)
        except (json.JSONDecodeError, IOError, KeyError):
            return None

    def delete_save(self, slot: int) -> bool:
        """Delete a save slot."""
        path = self.get_save_path(slot)
        if os.path.exists(path):
            try:
                os.remove(path)
                return True
            except IOError:
                return False
        return False

    def list_saves(self) -> list:
        """List all save slots with info."""
        saves = []
        for slot in range(1, 4):  # 3 save slots
            info = self.get_save_info(slot)
            if info:
                saves.append({"slot": slot, **info})
            else:
                saves.append({"slot": slot, "empty": True})
        return saves

    def export_save(self, slot: int, export_path: str) -> bool:
        """Export a save to an external location."""
        source_path = self.get_save_path(slot)
        if not os.path.exists(source_path):
            return False

        try:
            with open(source_path, 'r') as f:
                data = json.load(f)

            with open(export_path, 'w') as f:
                json.dump(data, f, indent=2)

            return True
        except IOError:
            return False

    def import_save(self, import_path: str, slot: int) -> bool:
        """Import a save from an external location."""
        if not os.path.exists(import_path):
            return False

        try:
            with open(import_path, 'r') as f:
                data = json.load(f)

            # Validate it's a valid save
            if "player" not in data:
                return False

            dest_path = self.get_save_path(slot)
            with open(dest_path, 'w') as f:
                json.dump(data, f, indent=2)

            return True
        except (json.JSONDecodeError, IOError):
            return False
