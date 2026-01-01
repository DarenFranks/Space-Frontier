#!/bin/bash
# Void Dominion GUI Launcher Script
# USB Drive Edition

echo "================================================"
echo "       SPACE FRONTIER - USB Edition"
echo "================================================"
echo ""
echo "Starting game..."
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found!"
    echo ""
    echo "Please install Python 3.10 or higher:"
    echo "  https://www.python.org/downloads/"
    echo ""
    exit 1
fi

# Check for tkinter
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo "ERROR: tkinter is not installed!"
    echo ""
    echo "Install tkinter:"
    echo "  Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "  Fedora/RHEL:   sudo dnf install python3-tkinter"
    echo "  Arch:          sudo pacman -S tk"
    echo "  macOS:         Included with Python (no action needed)"
    echo ""
    exit 1
fi

# Run the GUI game
python3 gui.py

exit 0
