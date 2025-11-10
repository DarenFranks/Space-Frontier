#!/bin/bash
# Void Dominion Installation Script

echo "=========================================="
echo "  Void Dominion - Installation Script"
echo "=========================================="
echo ""

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected: Linux"

    # Check if running Ubuntu/Debian
    if command -v apt-get &> /dev/null; then
        echo "Installing tkinter for Ubuntu/Debian..."
        sudo apt-get update
        sudo apt-get install -y python3-tk

    # Check if running Fedora/RHEL
    elif command -v dnf &> /dev/null; then
        echo "Installing tkinter for Fedora/RHEL..."
        sudo dnf install -y python3-tkinter

    # Check if running Arch
    elif command -v pacman &> /dev/null; then
        echo "Installing tkinter for Arch..."
        sudo pacman -S tk

    else
        echo "Unknown Linux distribution."
        echo "Please install python3-tk manually for your distribution."
    fi

elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected: macOS"
    echo "tkinter should be included with Python on macOS."
    echo "If not, install Python from python.org"

else
    echo "Detected: Windows or other"
    echo "tkinter should be included with Python."
fi

echo ""
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

echo ""
echo "=========================================="
echo "  Installation Complete!"
echo "=========================================="
echo ""
echo "Run the game with:"
echo "  python3 gui.py"
echo "  or"
echo "  ./play.sh"
echo ""
