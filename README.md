# 🚀 Void Dominion

**A vast sci-fi exploration and trading game with strategic combat, deep crafting systems, and factional warfare**

**Version**: 0.1.8 | **Status**: Alpha Development | **Platform**: Windows, macOS, Linux

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## 🌌 Overview

**Void Dominion** is a comprehensive space trading and combat simulator featuring a massive procedurally-enhanced universe with **56 locations** across **5 faction territories**. Build your trading empire, master complex manufacturing chains, engage in tactical combat, and navigate the dangerous politics of factional warfare.

### Key Features At A Glance

- 🗺️ **56 Locations** spanning neutral zones to deadly pirate territories
- 🏴 **Faction Loyalty System** with 7 reputation tiers
- 🚀 **Cinematic Warp Travel** with full-motion video animation
- ⚔️ **Tactical Turn-Based Combat** with advanced damage systems
- 🏭 **Deep Manufacturing** - craft ships, modules, and components
- 💎 **Faction-Specific Loot** - uncraftable legendary items
- 📊 **Dynamic Economy** with supply/demand pricing
- 🎯 **Contract System** - mining, combat, transport, and research missions
- 🛰️ **Multi-Ship Management** - own and manage multiple vessels with berth system
- ⚙️ **Module Fitting** - customize ships with weapons, defenses, and utilities
- 🎨 **Modern GUI** - Sleek sci-fi interface with orange/amber spaceship theme

---

## 🎮 Gameplay Systems

### 🌍 Universe & Exploration

**56 Unique Locations** organized into territories:
- **Neutral Zone** (4 locations) - Safe starting area for new players
- **Meridian Collective** (13 locations) - Democratic traders focused on commerce
- **Technocrat Union** (14 locations) - Scientific cabal pursuing tech supremacy  
- **Cipher Dominion** (14 locations) - Militaristic empire expanding through force
- **Void Corsairs** (11 locations) - Pirate syndicate in the lawless outer reaches

**Travel System:**
- Real distances between locations (80-800 light-seconds)
- Travel time based on ship speed and distance
- **Cinematic warp travel video** plays during journey
- Full-screen overlay with universe map and warp animation
- Automatic arrival when video completes
- Encounter system (combat & traders) on arrival

### 🏴 Faction & Loyalty System

**7 Loyalty Tiers** (-100 to +100):
- **Exalted** (90-100): +50% loot quality, +150% contract rewards
- **Revered** (60-89): +20% loot, +100% contracts
- **Honored** (30-59): -10% loot, +50% contracts
- **Friendly** (10-29): -30% loot, +20% contracts
- **Neutral** (-9 to 9): -50% loot, normal contracts
- **Hostile** (-49 to -10): No loot, -30% contracts
- **Reviled** (-100 to -50): No loot, -50% contracts, KOS

**Gain Loyalty:** Complete faction contracts (+2 to +5), Defeat faction enemies (+1), Trade at faction stations (+0.5)

**Lose Loyalty:** Attack faction members (-10), Fail faction contracts (-3), Aid rival factions (-1 to -3)

### ⚔️ Combat System

**Turn-Based Tactical Combat:**
- Dynamic initiative system
- Multiple weapon types (lasers, missiles, railguns)
- Shield penetration and armor mechanics
- Evasion based on ship speed
- Critical hits and special attacks

**Ship Classes:** Fighter, Scout, Cruiser, Hauler, Refinery, Destroyer, Carrier, Battleship, Dreadnought

### 🏭 Manufacturing & Economy

**Complex Crafting Chain:**
1. **Mine** raw resources from asteroid belts
2. **Refine** raw materials into processed resources
3. **Manufacture** components from processed resources
4. **Assemble** modules from components
5. **Build** complete ships from blueprints

**Manufacturing Categories:** Ship Components (10 types), Ship Modules (50+ variants), Complete Vessels (9 classes, 3 tiers each)

**Economic Features:** Supply/demand pricing, Station-specific inventories, Commodity trading, Black markets

### 💎 Loot & Rewards

**Faction-Specific Items** (UNCRAFTABLE - acquired through contracts & combat):
- Meridian Envoy - Enhanced cargo cruiser (+50% cargo, +30% speed)
- Cipher Destroyer - Devastating assault ship (+25% HP/shields)
- Technocrat Quantum Shield - Experimental +40% shield tech
- Corsair Stealth Thruster - Modified for evasion and speed

### 🛰️ Ship Management

**Berth System:** Own multiple ships, Store at stations, Switch ships at shipyards, Independent cargo/modules per ship

**Module Fitting:**
- 4 module types: Weapon, Defense, Utility, Engine
- Install/remove modules at shipyards
- Three inventory locations: Ship Cargo, Station Storage, Installed modules

### 🎯 Contract System

**6 Contract Types:** Resource Extraction, Resource Refining, Component Manufacturing, Combat Patrol, Cargo Transport, Reconnaissance

**Faction Contracts:** Only in faction territory, Rewards scale with loyalty, Increase reputation, Unique faction loot

### 📈 Skills & Progression

**14 Skills Across 5 Categories:**
- **Combat**: Weapons Mastery, Defense Systems, Evasive Maneuvers
- **Industry**: Mining Operations, Refining, Module Manufacturing, Component Assembly
- **Exploration**: Scanning, Navigation, Trading
- **Technical**: Engineering, Power Management, Computer Systems
- **Command**: Leadership, Negotiation

---

## 🎨 Interface Features

### Modern Sci-Fi GUI
- Dark space theme with cyan accents
- Smooth animations and transitions
- Color-coded information
- Left sidebar navigation with 13 views

### Visual Universe Map
- All 56 locations visible at once
- Organized by faction territory
- Color-coded by type (station/planet/asteroid/space)
- Current location highlighted
- Connected locations clickable
- Persistent legend always visible

### Warp Travel Animation
- **Full-motion video** playback during warp travel
- Fullscreen travel overlay with split view
- Left: Universe map showing route
- Right: Cinematic warp travel video (9MB MP4)
- Automatic arrival when video completes
- Seamless integration with game flow

---

## 📦 Installation

### Requirements
- Python 3.7+
- OpenCV (opencv-python) for video playback
- ~60 MB disk space (includes 9MB warp video)
- 1400x900 minimum resolution

### Windows Installation

**Easy Method (Recommended):**
1. Download and extract the latest release
2. Double-click `install.bat` (one-time setup)
3. Double-click `play.bat` to launch the game

**Manual Method:**
```bash
pip install -r requirements.txt
python gui.py
```

### Linux/macOS Installation

```bash
git clone https://github.com/DarenFranks/VoidDominion.git
cd VoidDominion
pip3 install -r requirements.txt
python3 gui.py
```

**Note:** If you encounter issues installing opencv-python, you may need:
```bash
pip3 install --user --break-system-packages opencv-python
```


---

## 🎯 Getting Started

### First Steps
1. **Launch the game**
   - Windows: Double-click `play.bat`
   - Linux/macOS: Run `python3 gui.py`
2. **Create a character** - Click "New Game" and enter your commander name
3. **Start in Neutral Zone** - Begin at Nexus Prime with 50,000 credits
4. **Learn the interface** - Explore the left navigation menu
5. **Mine resources** - Visit Mining tab to extract resources
6. **Accept contracts** - Check Contracts tab for missions
7. **Upgrade your ship** - Use Shipyard to purchase better vessels
8. **Explore** - Travel to new locations via the Travel/Map page

### Early Game Strategy

**Phase 1: Neutral Zone (Levels 1-5)** - Mine safely, accept basic contracts, save for upgrades

**Phase 2: Faction Introduction (Levels 6-10)** - Choose a faction, complete contracts for loyalty, explore borders

**Phase 3: Specialization (Levels 11-15)** - Focus manufacturing or combat, acquire faction loot

**Phase 4: End Game (Levels 16+)** - Challenge Void Corsairs, hunt legendaries, dominate warfare

---

## 📊 Game Statistics

### Content Volume
- **Locations**: 56 (4 neutral, 52 faction)
- **Ship Classes**: 9 base classes, 27 variants (3 tiers each)
- **Modules**: 50+ across 4 categories
- **Components**: 10 types
- **Resources**: 8 raw + 8 refined
- **Factions**: 4 major factions
- **Skills**: 14 trainable abilities
- **Contract Types**: 6 mission categories

### Progression Scale
- **Level Range**: 1-20+
- **Credit Economy**: 1K to 10M+
- **Travel Distances**: 80-800 light-seconds
- **Danger Levels**: 5% to 95%

---

## 🛠️ Technical Details

### Performance
- Startup Time: <2 seconds
- Memory Usage: ~50-80 MB (+ video playback)
- CPU Usage: Low (turn-based), moderate during video playback
- Save File Size: ~50-200 KB
- Video File: 9MB (Straight_On_Warp_Travel_Video.mp4)

### Save System
- Auto-save on major actions
- Manual save via STATUS menu
- Multiple save slots
- JSON format
- Persistent universe state

---

## 🗺️ Roadmap

### Planned Features
- Additional faction territories
- Player-owned stations
- Fleet command system
- Advanced automation
- Story campaign mode

---

## 🤝 Contributing

Contributions welcome! Bug reports, feature suggestions, documentation, and code contributions all appreciated.

---

## 📜 License

MIT License - see LICENSE file for details.

---

**Built with ❤️ by Daren Franks**

*"In space, fortune favors the bold... and the well-prepared."*
