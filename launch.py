#!/usr/bin/env python3
"""
Void Dominion Launcher
Checks dependencies and launches the game
"""

import sys
import subprocess

def check_dependencies():
    """Check if all dependencies are installed"""
    missing = []

    # Check tkinter
    try:
        import tkinter
        print("✓ tkinter is installed")
    except ImportError:
        print("✗ tkinter is NOT installed")
        missing.append("tkinter")

    # Check yaml
    try:
        import yaml
        print("✓ PyYAML is installed")
    except ImportError:
        print("✗ PyYAML is NOT installed")
        missing.append("yaml")

    return missing

def main():
    print("=" * 50)
    print("  Void Dominion - Dependency Check")
    print("=" * 50)
    print()

    missing = check_dependencies()

    print()

    if missing:
        print("❌ Missing dependencies detected!")
        print()

        if "tkinter" in missing:
            print("To install tkinter:")
            print("  Ubuntu/Debian: sudo apt-get install python3-tk")
            print("  Fedora/RHEL:   sudo dnf install python3-tkinter")
            print("  Arch Linux:    sudo pacman -S tk")
            print()

        if "yaml" in missing:
            print("To install PyYAML:")
            print("  pip3 install pyyaml")
            print()

        print("Or run the automated installer:")
        print("  ./install.sh")
        print()

        # Offer text-based version
        if "tkinter" in missing and "yaml" not in missing:
            print("Alternative: Run text-based version (no GUI):")
            print("  python3 main.py")
            print()

            response = input("Launch text version now? (y/n): ").lower()
            if response == 'y':
                import main
                return

        sys.exit(1)

    print("✓ All dependencies satisfied!")
    print()
    print("Launching Void Dominion GUI...")
    print()

    # Launch GUI
    import gui
    gui.main()

if __name__ == "__main__":
    main()
