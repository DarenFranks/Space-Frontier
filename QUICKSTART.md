# Void Dominion - Quick Start Guide

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the game:
```bash
python main.py
```

## Getting Started

### Your First Steps

1. **Start a new game** and choose your commander name
2. You begin at **Nexus Prime** with 50,000 credits and a basic Harbinger-class Scout vessel
3. Type `status` to see your current state
4. Type `help` to see all available commands

### Essential Commands

- `status` - View your character and vessel status
- `map` - See connected locations
- `scan` - Scan your current area for resources and info
- `help` - Show all commands

### How to Make Money

#### 1. Mining Resources
```
mine              # Mine resources at current location
inventory         # Check what you mined
market            # View market prices
sell voltium 50   # Sell resources at market
```

#### 2. Trading
- Buy low at one location, sell high at another
- Use `market` command to compare prices
- Resources are cheaper where they're produced

#### 3. Contracts
```
contracts         # View available missions
accept 1          # Accept first contract
active            # Check active contract progress
```

### Combat

When you encounter enemies:
- `attack` - Attack the enemy
- `retreat` - Try to escape

Your weapon damage and shield strength depend on installed modules.

### Progression

#### Skills
Train skills to improve your abilities:
```
skills            # View all skills
train weapons mastery    # Start training a skill
```

Skills train over time (even when offline).

#### Upgrading Your Vessel
1. Earn credits through trading, mining, or contracts
2. Travel to locations with `shipyard` service
3. Purchase better vessels or modules

### Key Locations

- **Nexus Prime** - Starting location, main trade hub
- **Outer Traverse** - Good for mining rare resources
- **Synthesis Hub** - Research and advanced tech
- **Cipher Core** - Militarized, potentially hostile

### Factions

Four major factions control territory:
- **Meridian Collective** - Trade-focused democracy (Friendly)
- **Cipher Dominion** - Military empire (Hostile)
- **Technocrat Union** - Scientific cabal (Friendly)
- **Void Corsairs** - Pirate syndicate (Hostile)

Your standing with factions affects:
- Market prices
- Access to locations
- Random encounters

### Tips

1. **Save often** - Use the `save` command
2. **Check contracts** - Easy source of income
3. **Upgrade your vessel** - Better modules = better survivability
4. **Train skills** - Passive progression
5. **Watch danger levels** - Higher danger = more enemy encounters
6. **Scan before mining** - See what resources are available
7. **Diversify income** - Combine trading, mining, and contracts

### Game Features

#### Complex Systems
- **14 skills** across 5 categories
- **8 unique resources** with varying rarity
- **5 vessel classes** from scout to battleship
- **10+ modules** for customization
- **12 locations** across the Nebular Expanse
- **4 factions** with dynamic relations
- **5 contract types** with procedural generation

#### Economy
- Dynamic market prices that fluctuate
- Supply and demand simulation
- Trade routes between locations
- Tax system affected by skills

#### Combat
- Turn-based tactical combat
- Shield and armor mechanics
- Critical hits and evasion
- Multiple weapon types

#### Territory Control
- Factions compete for control
- Player standing affects access
- Bonuses in friendly territory

## Advanced Gameplay

### Optimal Trade Routes

Use the market system to find profitable routes:
1. Check market prices at multiple locations
2. Buy resources where they're produced (cheaper)
3. Sell where they're scarce (higher prices)
4. Factor in travel time and danger

### Skill Builds

**Combat Build:**
- Weapons Mastery
- Tactical Warfare
- Shield Operations

**Industrial Build:**
- Mining Operations
- Manufacturing
- Salvaging

**Trading Build:**
- Trade Proficiency
- Market Analysis
- Navigation

### Contract Strategy

- Easy contracts: Mining and transport
- Medium contracts: Reconnaissance
- Hard contracts: Combat patrol
- Very hard: Research data collection

Complete contracts before time expires for rewards.

## Troubleshooting

**Game won't start:**
- Make sure you installed requirements: `pip install -r requirements.txt`
- Check Python version (3.7+)

**Can't find location:**
- Use exact location names from `map` command
- Locations must be directly connected

**Combat too hard:**
- Upgrade weapons and shields
- Train combat skills
- Choose easier routes (lower danger level)

**Running out of money:**
- Focus on mining and selling resources
- Accept and complete contracts
- Trade proficiency skill reduces costs

## Command Reference

See in-game `help` command for full command list.

Key shortcuts:
- `Ctrl+C` - Save and exit
- Commands are case-insensitive
- You can abbreviate resource/location names

---

**Have fun exploring the Void!**

For bugs or feedback, check the project repository.
