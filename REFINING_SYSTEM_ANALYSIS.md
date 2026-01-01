# Refining System Analysis - Void Dominion

## Overview
The refining system allows players to convert raw ores into refined resources. Currently, it only sources materials from **ship cargo** and does not access **station storage**. This analysis covers the complete implementation and identifies the changes needed to support both sources.

---

## Current Implementation

### 1. Core Refining Logic - `game_engine.py` (Lines 559-640)

**Function:** `GameEngine.refine_ore(raw_ore_id: str, quantity: int) -> tuple[bool, str]`

**Key Points:**
- Checks for refining availability (refinery service OR mothership class)
- **ONLY reads from** `self.player.inventory` (which is an alias for `self.player.ship_cargo`)
- Performs cargo capacity validation before and after refining
- Calculates random yield based on ore rarity
- Removes raw ore and adds refined resource to inventory
- Updates player stats and awards XP

**Critical Line:**
```python
if not self.player.has_item(raw_ore_id, quantity):  # Line 586 - ONLY checks ship_cargo
    current_qty = self.player.inventory.get(raw_ore_id, 0)
    return False, f"Insufficient raw ore..."
```

The `has_item()` method (player.py:115-117) explicitly checks only `ship_cargo`:
```python
def has_item(self, item_id: str, quantity: int = 1) -> bool:
    """Check if player has item in ship cargo"""
    return item_id in self.ship_cargo and self.ship_cargo[item_id] >= quantity
```

---

### 2. GUI - Refining Interface - `gui.py` (Lines 4437-4610)

#### `show_refine_view()` - Lines 4437-4528
**Purpose:** Display all available raw ores for refining

**Key Points:**
- **ONLY iterates over ship cargo** (Line 4459):
  ```python
  for item_id, quantity in self.engine.player.ship_cargo.items():
  ```
- Filters items that are in `RAW_RESOURCES`
- Creates UI buttons for each ore type
- Shows yield ranges based on rarity

#### `refine_ore_dialog(ore_id)` - Lines 4530-4610
**Purpose:** Dialog for selecting quantity to refine

**Key Points:**
- Gets max quantity from ship cargo only (Line 4539):
  ```python
  max_qty = self.engine.player.ship_cargo.get(ore_id, 0)
  ```
- Displays current availability and yield percentages
- Calls `self.engine.refine_ore()` when refining

---

### 3. Player Inventory System - `player.py`

#### Data Structure (Lines 30-35)
```python
self.ship_cargo: Dict[str, int] = {}        # Items in ship cargo hold
self.station_inventories: Dict[str, Dict[str, int]] = {}  # location_id: {item_id: quantity}
self.inventory = self.ship_cargo  # Backwards compatibility alias
```

#### Transfer Methods (Lines 140-186)
- `transfer_to_station()` - Moves items from ship to station
- `transfer_to_ship()` - Moves items from station to ship (requires logistics_management skill level 5+)
- `get_station_inventory(location_id)` - Retrieves station inventory dictionary
- `get_total_item_count(item_id)` - Returns item count across ship and accessible stations

#### Station Access Control (Lines 125-138)
```python
def can_access_remote_stations(self) -> bool:
    return self.get_skill_level("logistics_management") >= 5

def get_accessible_stations(self) -> List[str]:
    accessible = [self.location]  # Current location always accessible
    if self.can_access_remote_stations():
        accessible.extend([loc for loc in self.station_inventories.keys() if loc != self.location])
    return accessible
```

---

## Refining Yield Data - `data.py`

### Yield Ranges (Lines 6-15)
```python
REFINING_YIELD_RANGES = {
    "common": (0.80, 0.95),       # 80-95% yield
    "uncommon": (0.70, 0.85),     # 70-85% yield
    "rare": (0.60, 0.75),         # 60-75% yield
    "very_rare": (0.55, 0.65),    # 55-65% yield
    "legendary": (0.50, 0.60)     # 50-60% yield
}
```

### Raw Resources Example (Lines 18-99)
Each raw resource specifies:
- `name`: Display name
- `rarity`: Determines yield percentage
- `refines_to`: Target refined resource ID
- `volume`: Size for cargo calculations

Example:
```python
"raw_voltium": {
    "name": "Raw Voltium Ore",
    "rarity": "common",
    "refines_to": "voltium",
    "volume": 1.0,
}
```

---

## Station Storage System

### Existing Transfer Capabilities
The game already has station storage transfers implemented in `player.py`:

1. **Transfer from ship to station** (requires being at location)
2. **Transfer from station to ship** (requires being at location OR logistics_management skill ≥5)
3. **Total item counting** across all accessible locations

**Example Usage in game:**
```python
# Death respawn logic (game_engine.py:256-274)
# When player dies, station storage is preserved
station_inventory = self.player.get_station_inventory(closest_station)
for ship_id, quantity in station_inventory.items():
    # Ships in station storage survive death
```

---

## What Needs to Change

To enable refining from **both ship cargo AND station storage**, modify:

### 1. **game_engine.py - `refine_ore()` method (Lines 559-640)**

**Changes needed:**
- Replace `self.player.has_item()` check with broader inventory check
- Create method that sums ore from both ship and station storage
- Support taking ore from either source (or priority-based)
- Update cargo capacity checks to account for both sources

**New logic flow:**
```
1. Check total ore available (ship + station)
2. Determine which inventory to draw from (ship first, then station)
3. Remove ore from that source
4. Add refined to ship cargo (or allow destination selection)
5. Handle cargo capacity accordingly
```

### 2. **gui.py - `show_refine_view()` (Lines 4437-4528)**

**Changes needed:**
- Instead of iterating only ship_cargo, iterate all accessible inventories
- Show sources in UI (e.g., "x50 in ship, x30 in station")
- Display total available for each ore type

### 3. **gui.py - `refine_ore_dialog()` (Lines 4530-4610)**

**Changes needed:**
- Calculate `max_qty` from both sources
- Add selection for which source to refine from
- Display breakdown of available ore by location

---

## Implementation Approach

### Option A: Draw from multiple sources automatically
- Check ship cargo first (up to requested quantity)
- If insufficient, draw remainder from station (current location only)
- Refined output always goes to ship cargo

### Option B: Player selects source
- Show ore available in each location
- Let player choose which inventory to draw from
- Support combining ores from multiple locations

### Option C: Refine in-place by location
- Allow refining items directly in station storage
- Output stays in station storage
- Requires visiting refinery at each location

---

## Key Files to Modify

| File | Function/Class | Lines | Purpose |
|------|---|---|---|
| `/home/daren/Space_Frontier/game_engine.py` | `GameEngine.refine_ore()` | 559-640 | Core refining logic |
| `/home/daren/Space_Frontier/gui.py` | `GUIManager.show_refine_view()` | 4437-4528 | Ore listing UI |
| `/home/daren/Space_Frontier/gui.py` | `GUIManager.refine_ore_dialog()` | 4530-4610 | Refining dialog |
| `/home/daren/Space_Frontier/player.py` | Player class methods | 83-196 | Inventory management |
| `/home/daren/Space_Frontier/data.py` | `RAW_RESOURCES` | 18-99 | Raw ore definitions |

---

## Helper Methods Already Available in Player

The following methods support the new functionality:

1. `get_station_inventory(location_id)` - Get inventory at location
2. `get_accessible_stations()` - Get all accessible locations
3. `transfer_to_station()` - Move items to station
4. `transfer_to_ship()` - Move items from station
5. `get_total_item_count(item_id)` - Count item across all locations

---

## Inventory Data Structure Flow

```
Player Object
├── ship_cargo: {item_id: quantity}          # Direct access
├── station_inventories: {
│   └── location_id: {item_id: quantity}     # Nested by location
└── Accessible via:
    ├── player.inventory (alias to ship_cargo)
    ├── player.get_station_inventory(location_id)
    └── player.get_total_item_count(item_id)
```

---

## References to Cargo/Inventory in Refining Context

- Line 608 (game_engine.py): `current_volume = self.player.get_cargo_volume()` - Gets ship cargo volume
- Line 607 (game_engine.py): `cargo_capacity = self.vessel.cargo_capacity` - Ship's total capacity
- Line 4539 (gui.py): `max_qty = self.engine.player.ship_cargo.get(ore_id, 0)` - Gets qty from ship only
- Line 4459 (gui.py): `for item_id, quantity in self.engine.player.ship_cargo.items()` - Iterates ship only
