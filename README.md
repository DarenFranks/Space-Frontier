# Void Dominion (Space Frontier)

A complex sci-fi strategy game with a **modern sci-fi GUI** set in the Nebular Expanse.

**Version**: 1.0 | **Status**: Complete | **Platform**: Windows, macOS, Linux

## Game Overview

**Void Dominion** is a standalone desktop game with a graphical interface inspired by Torn. Players navigate a vast universe filled with:

- **Vessels**: Customizable spacecraft with modular systems
- **Economy**: Complex market system with resource extraction, manufacturing, and trading
- **Factions**: Multiple competing organizations vying for control
- **Territory Control**: Claim and manage sectors of space
- **Skills**: Deep character progression system
- **Combat**: Tactical engagement system
- **Contracts**: Dynamic mission system

## Features

### Interface
- **Modern Sci-Fi GUI** - Cyan accents, dark space theme, glowing effects
- **Left Navigation Sidebar** - Easy access to all features
- **Standalone Application** - No browser required!
- **Cross-Platform** - Works on Windows, macOS, and Linux

### Gameplay
- **Complex Economy** - Mining, refining, manufacturing, trading
- **Dynamic Contracts** - 5 types: Mining, Combat, Transport, Scanning, Research
- **Skill Progression** - 14 trainable skills across 5 categories
- **Vessel Customization** - 5 ship classes with modular upgrades
- **Turn-Based Combat** - Tactical battles with shields, weapons, and evasion
- **Faction System** - 4 major factions with territory and reputation

### Content
- 8 unique resources with varying rarity
- 12 locations across the galaxy
- 50+ ship modules and components
- Persistent universe with save/load
- Procedural contract generation
- Automatic payout system

## Installation

### Requirements
- Python 3.7 or higher
- ~50 MB disk space
- 1400x900 minimum screen resolution

### Quick Install

**All Platforms:**
```bash
# 1. Install dependencies (only pyyaml needed!)
pip3 install -r requirements.txt

# 2. Launch the game
python3 gui.py
```

**USB Drive Installation:**
See [USB_INSTALL_GUIDE.md](USB_INSTALL_GUIDE.md) for complete instructions on running from a USB drive.

**Standard Installation:**
See [INSTALL.md](INSTALL.md) for platform-specific instructions.

**Note for Linux:** You may need to install python3-tk:
```bash
sudo apt install python3-tk  # Ubuntu/Debian
```

## Running the Game

**GUI Version (Recommended):**
```bash
python3 gui.py
# or
./play.sh
```

**Text Version (Legacy):**
```bash
python3 main.py
```

## GUI Features

### Modern Sci-Fi Interface
- **Left Sidebar Navigation** - All features in one organized menu
- **Top Status Bar** - Commander info, location, credits, cargo at a glance
- **Styled Panels** - Bordered containers with glowing cyan accents
- **Hover Effects** - Interactive feedback on all buttons
- **Active Highlighting** - Always know which view you're in

### Game Views
- **Status** - View commander and vessel stats
- **Travel** - Navigate between connected star systems
- **Market** - Buy and sell resources with live pricing
- **Contracts** - Accept and complete missions for rewards
- **Vessel** - Manage ship modules and equipment
- **Shipyard** - Purchase new vessels
- **Manufacturing** - Craft components and modules
- **Skills** - Train and upgrade character abilities

### Visual Theme
- Deep space black backgrounds
- Bright cyan (#00d9ff) accents and glows
- High contrast for readability
- Monospace fonts for technical aesthetic
- Color-coded status indicators (green/orange/red)
