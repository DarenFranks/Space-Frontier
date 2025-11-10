"""
Save and Load System
Handles game state persistence
"""

import yaml
import os
from typing import Optional
from config import SAVE_FILE


def save_game(game_state: dict, filename: str = SAVE_FILE) -> bool:
    """
    Save game state to file.
    Returns True if successful.
    """
    try:
        with open(filename, 'w') as f:
            yaml.dump(game_state, f, default_flow_style=False, sort_keys=False)
        return True
    except Exception as e:
        print(f"Error saving game: {e}")
        return False


def load_game(filename: str = SAVE_FILE) -> Optional[dict]:
    """
    Load game state from file.
    Returns game state dict if successful, None otherwise.
    """
    if not os.path.exists(filename):
        return None

    try:
        with open(filename, 'r') as f:
            game_state = yaml.safe_load(f)
        return game_state
    except Exception as e:
        print(f"Error loading game: {e}")
        return None


def save_exists(filename: str = SAVE_FILE) -> bool:
    """Check if save file exists"""
    return os.path.exists(filename)


def delete_save(filename: str = SAVE_FILE) -> bool:
    """Delete save file"""
    try:
        if os.path.exists(filename):
            os.remove(filename)
        return True
    except Exception as e:
        print(f"Error deleting save: {e}")
        return False
