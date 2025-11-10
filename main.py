#!/usr/bin/env python3
"""
Void Dominion - A Complex Text-Based Sci-Fi Strategy Game
Main entry point
"""

import sys
from game_engine import GameEngine
from ui import GameUI
from save_system import save_exists
from config import GAME_NAME, VERSION


def print_title():
    """Print game title"""
    title = f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                      VOID DOMINION                           ║
║                                                              ║
║              Navigate. Trade. Conquer. Survive.              ║
║                                                              ║
║                       Version {VERSION:<10}                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(title)


def main_menu() -> str:
    """Show main menu and get choice"""
    print("\n=== MAIN MENU ===\n")

    has_save = save_exists()

    if has_save:
        print("1. Continue Game")
        print("2. New Game")
        print("3. Exit")
        choice = input("\nSelect option: ").strip()
        return choice
    else:
        print("1. New Game")
        print("2. Exit")
        choice = input("\nSelect option: ").strip()
        if choice == "1":
            return "2"  # Map to new game
        elif choice == "2":
            return "3"  # Map to exit
        return choice


def game_loop(engine: GameEngine, ui: GameUI):
    """Main game loop"""
    print("\nType 'help' for a list of commands.\n")

    while ui.running:
        try:
            # Update game state
            engine.update_game_state()

            # Get user input
            if engine.current_combat and engine.current_combat.is_active:
                prompt = "[COMBAT] > "
            else:
                prompt = f"[{engine.player.name}] > "

            user_input = input(prompt).strip()

            if user_input:
                ui.parse_command(user_input)

        except KeyboardInterrupt:
            print("\n\nInterrupted. Saving game...")
            engine.save_current_game()
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Type 'help' for available commands")


def main():
    """Main entry point"""
    print_title()

    engine = GameEngine()

    # Main menu
    choice = main_menu()

    if choice == "1":
        # Continue game
        if engine.load_saved_game():
            ui = GameUI(engine)
            game_loop(engine, ui)
        else:
            print("Failed to load save game")
            return

    elif choice == "2":
        # New game
        print("\n=== NEW GAME ===\n")
        player_name = input("Enter your commander name: ").strip()

        if not player_name:
            player_name = "Commander"

        engine.new_game(player_name)
        ui = GameUI(engine)
        game_loop(engine, ui)

    elif choice == "3":
        # Exit
        print("\nFarewell, Commander!\n")
        return

    else:
        print("Invalid choice")
        return

    print("\n" + "=" * 60)
    print("Thank you for playing Void Dominion!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)
