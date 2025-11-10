# Refining System Implementation Guide

## Current Flow (Ship Cargo Only)

```
User clicks "Refine" in GUI
           |
           v
gui.py: show_refine_view()
    - Iterates: player.ship_cargo.items()
    - Shows raw ores in ship only
           |
           v
gui.py: refine_ore_dialog(ore_id)
    - Gets max_qty from: player.ship_cargo.get(ore_id, 0)
    - User enters quantity
           |
           v
game_engine.py: refine_ore(ore_id, quantity)
    - Checks: player.has_item(ore_id, quantity)
           |
           +---> ONLY checks player.ship_cargo
           |
    - Validates cargo capacity for refined output
    - Removes ore from player.inventory (ship_cargo)
    - Adds refined resource to player.inventory (ship_cargo)
           |
           v
Return success/failure
```

---

## Proposed Flow (Multi-Source)

### Option A: Automatic Multi-Source (Recommended)

```
User clicks "Refine" in GUI
           |
           v
gui.py: show_refine_view()
    - Iterate all accessible inventories:
      for location in player.get_accessible_stations():
          inventory = player.get_station_inventory(location)
          for item_id, qty in inventory.items():
              if item_id in RAW_RESOURCES:
                  show in UI
    - Shows raw ores from ship AND all accessible stations
    - Display: "x50 (ship) + x30 (nexus) = 80 total"
           |
           v
gui.py: refine_ore_dialog(ore_id)
    - Gets max_qty from: player.get_total_item_count(ore_id)
    - User enters quantity (can exceed ship amount now)
           |
           v
game_engine.py: refine_ore(ore_id, quantity)
    - Check total available:
      total = player.get_total_item_count(ore_id)
    - If total >= quantity: Proceed
           |
    - Source ore (priority: ship cargo first, then station):
      remaining = quantity
      
      # Take from ship first
      from_ship = min(remaining, player.ship_cargo.get(ore_id, 0))
      player.ship_cargo[ore_id] -= from_ship
      remaining -= from_ship
      
      # If still need more, take from current station
      if remaining > 0:
          station_inv = player.get_station_inventory(player.location)
          from_station = min(remaining, station_inv.get(ore_id, 0))
          station_inv[ore_id] -= from_station
           |
    - Validate cargo capacity (refined goes to ship)
    - Add refined resource to player.ship_cargo
           |
           v
Return success/failure
```

### Option B: Player-Selected Source

```
gui.py: refine_ore_dialog(ore_id)
    - Show radio buttons for source selection:
      * Ship Cargo (x50)
      * Nexus Station (x30)
      * Combine sources
    - User selects source AND quantity
           |
           v
game_engine.py: refine_ore(ore_id, quantity, source_location=None)
    - If source_location specified: Use only that source
    - If source_location is None: Use ship only (legacy)
    - Otherwise: Use multi-source logic
```

---

## Code Changes Required

### 1. Add Helper Method to Player Class (player.py)

```python
def get_total_accessible_quantity(self, item_id: str) -> tuple[Dict[str, int], int]:
    """
    Get quantity of item across all accessible inventories
    Returns: (location_quantities, total)
    
    location_quantities = {
        'ship': 50,
        'nexus_prime': 30,
        'outer_rim_station': 15
    }
    total = 95
    """
    location_quantities = {
        'ship': self.ship_cargo.get(item_id, 0)
    }
    
    for location_id in self.get_accessible_stations():
        if location_id != self.location:  # Skip ship (already added)
            station_inv = self.get_station_inventory(location_id)
            location_quantities[location_id] = station_inv.get(item_id, 0)
    
    total = sum(location_quantities.values())
    return location_quantities, total
```

### 2. Modify game_engine.py: refine_ore() Method

**Before:**
```python
# Check if player has the raw ore (ONLY ship cargo)
if not self.player.has_item(raw_ore_id, quantity):
    current_qty = self.player.inventory.get(raw_ore_id, 0)
    return False, f"Insufficient raw ore..."
```

**After:**
```python
# Check total available across all accessible inventories
_, total_available = self.player.get_total_accessible_quantity(raw_ore_id)
if total_available < quantity:
    return False, f"Insufficient raw ore. You have {total_available}x {raw_ore_data['name']}"

# Source the ore (ship first, then station)
remaining = quantity
from_ship = min(remaining, self.player.ship_cargo.get(raw_ore_id, 0))
self.player.ship_cargo[raw_ore_id] -= from_ship
remaining -= from_ship

if remaining > 0:
    # Take from station at current location
    station_inv = self.player.get_station_inventory(self.player.location)
    from_station = min(remaining, station_inv.get(raw_ore_id, 0))
    station_inv[raw_ore_id] -= from_station
    remaining -= from_station
    
    if remaining > 0:
        # This shouldn't happen if check passed, but fail safely
        # Refund what we took
        self.player.add_item(raw_ore_id, from_ship)
        station_inv[raw_ore_id] += from_station
        return False, "Error sourcing ore from inventories"
```

### 3. Modify gui.py: show_refine_view() Method

**Before:**
```python
# Get raw ores from inventory (ONLY ship cargo)
raw_ores_in_cargo = {}
for item_id, quantity in self.engine.player.ship_cargo.items():
    if item_id in RAW_RESOURCES:
        raw_ores_in_cargo[item_id] = quantity
```

**After:**
```python
# Get raw ores from all accessible inventories
raw_ores_by_location = {}
for location_id in self.engine.player.get_accessible_stations():
    inventory = self.engine.player.ship_cargo if location_id == 'ship' else \
                self.engine.player.get_station_inventory(location_id)
    for item_id, quantity in inventory.items():
        if item_id in RAW_RESOURCES:
            if item_id not in raw_ores_by_location:
                raw_ores_by_location[item_id] = {}
            location_name = 'Ship Cargo' if location_id == 'ship' else \
                           LOCATIONS[location_id]['name']
            raw_ores_by_location[item_id][location_name] = quantity

# Build aggregated list
raw_ores_in_cargo = {}
for item_id, locations in raw_ores_by_location.items():
    raw_ores_in_cargo[item_id] = sum(locations.values())
    # Store location breakdown for UI display
    raw_ores_in_cargo[f"{item_id}_breakdown"] = locations
```

### 4. Modify gui.py: refine_ore_dialog() Method

**Before:**
```python
max_qty = self.engine.player.ship_cargo.get(ore_id, 0)
```

**After:**
```python
# Get total available from all sources
_, max_qty = self.engine.player.get_total_accessible_quantity(ore_id)

# Optionally show breakdown in dialog
location_breakdown, _ = self.engine.player.get_total_accessible_quantity(ore_id)
breakdown_text = " + ".join([f"{qty}({loc})" for loc, qty in location_breakdown.items()])
```

---

## Testing Checklist

- [ ] Player can see raw ores from ship cargo
- [ ] Player can see raw ores from current station storage
- [ ] GUI shows combined quantity (ship + station)
- [ ] Refining uses ship cargo first
- [ ] Refining uses station storage when ship is insufficient
- [ ] Cargo capacity validation works with multi-source
- [ ] Refined output always goes to ship cargo
- [ ] Edge case: Ore removed from station between view and refine
- [ ] Edge case: Player moves between locations during refinement UI
- [ ] Stats and XP awards work correctly
- [ ] Backwards compatibility: Refining from ship-only still works

---

## Files Changed Summary

| File | Change Type | Lines | Impact |
|------|---|---|---|
| player.py | Add method | ~20 lines | New helper method |
| game_engine.py | Modify method | ~50 lines | Core logic change |
| gui.py | Modify method | ~30 lines | UI display change |
| gui.py | Modify method | ~20 lines | Dialog display change |

**Total Changes:** ~120 lines of code

---

## Data Flow Diagram

```
Player Object
├── ship_cargo: {ore_id: qty, ...}
├── station_inventories: {
│   ├── nexus_prime: {ore_id: qty, ...}
│   ├── outer_rim: {ore_id: qty, ...}
│   └── ...
│
└── Helper Methods:
    ├── get_total_item_count(ore_id)
    │   └── Returns: sum across all accessible locations
    │
    ├── get_total_accessible_quantity(ore_id) [NEW]
    │   └── Returns: {location: qty, ...} + total
    │
    └── get_accessible_stations()
        └── Returns: [current_location, remote_if_skilled]
```

---

## Fallback/Rollback Plan

If multi-source refining causes issues:

1. Add config flag: `ENABLE_MULTI_SOURCE_REFINING = False`
2. Wrap new logic in conditional:
   ```python
   if ENABLE_MULTI_SOURCE_REFINING:
       # Use new multi-source logic
   else:
       # Use legacy ship-cargo-only logic
   ```
3. Can quickly disable feature without removing code

