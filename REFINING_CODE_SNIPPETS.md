# Refining System - Ready-to-Use Code Snippets

## 1. New Helper Method for player.py (Insert after line 196)

```python
def get_total_accessible_quantity(self, item_id: str) -> tuple[Dict[str, int], int]:
    """
    Get quantity of item across all accessible inventories.
    Used for multi-source refining and crafting.
    
    Returns: (location_quantities_dict, total_quantity)
    
    Example:
        location_breakdown, total = player.get_total_accessible_quantity('raw_voltium')
        # location_breakdown = {'ship': 50, 'nexus_prime': 30}
        # total = 80
    """
    location_quantities = {}
    
    # Add ship cargo
    location_quantities['ship'] = self.ship_cargo.get(item_id, 0)
    
    # Add accessible station inventories
    for location_id in self.get_accessible_stations():
        if location_id != 'ship':  # Skip duplicating ship
            station_inv = self.get_station_inventory(location_id)
            qty = station_inv.get(item_id, 0)
            if qty > 0:  # Only include non-zero quantities
                location_quantities[location_id] = qty
    
    total = sum(location_quantities.values())
    return location_quantities, total
```

---

## 2. Modified refine_ore() Method for game_engine.py

Replace the entire method from lines 559-640 with:

```python
def refine_ore(self, raw_ore_id: str, quantity: int) -> tuple[bool, str]:
    """
    Refine raw ore into refined resources
    Yield is RNG-based depending on ore rarity (50-95%)
    Less rare = more refined, More rare = less refined
    Refines the ENTIRE requested quantity - fails if cargo can't hold output
    
    Sources ore from both ship cargo and station storage (multi-source support)
    """
    # Check if refining is available (at refinery or on mothership)
    location_data = LOCATIONS[self.player.location]
    has_refinery_service = "refinery" in location_data.get("services", [])

    # Check if ship has refining capability (mothership)
    has_ship_refinery = False
    if self.vessel:
        ship_class_type = self.vessel.class_type
        has_ship_refinery = ship_class_type == "mothership"

    if not has_refinery_service and not has_ship_refinery:
        return False, "Refining requires a refinery facility or a mothership"

    # Check if the ore exists and is a raw resource
    if raw_ore_id not in RAW_RESOURCES:
        return False, "This is not a raw ore resource"

    raw_ore_data = RAW_RESOURCES[raw_ore_id]

    # ===== MULTI-SOURCE CHECK =====
    # Check total available across all accessible inventories
    location_breakdown, total_available = self.player.get_total_accessible_quantity(raw_ore_id)
    
    if total_available < quantity:
        return False, f"Insufficient raw ore. You have {total_available}x {raw_ore_data['name']} across all inventories"

    # Get the refined resource info
    refined_id = raw_ore_data.get("refines_to")
    if not refined_id:
        return False, f"{raw_ore_data['name']} cannot be refined"

    refined_data = RESOURCES[refined_id]

    # Get rarity and calculate RNG yield
    rarity = raw_ore_data.get("rarity", "common")
    min_yield, max_yield = REFINING_YIELD_RANGES.get(rarity, (0.7, 0.9))

    # Calculate random yield percentage for the ENTIRE batch
    yield_percent = random.uniform(min_yield, max_yield)
    refined_quantity = max(1, int(quantity * yield_percent))

    # Calculate the NET volume change (refined ore is smaller than raw ore)
    # We REMOVE raw ore and ADD refined ore, so check the net change
    cargo_capacity = self.vessel.cargo_capacity
    current_volume = self.player.get_cargo_volume()

    raw_volume_to_remove = quantity * raw_ore_data["volume"]
    refined_volume_to_add = refined_quantity * refined_data["volume"]
    net_volume_change = refined_volume_to_add - raw_volume_to_remove
    final_volume = current_volume + net_volume_change

    # Check if the final volume (after removing raw and adding refined) fits
    if final_volume > cargo_capacity:
        space_needed = final_volume - cargo_capacity
        return False, f"Insufficient cargo space! Refining {quantity}x {raw_ore_data['name']} → {refined_quantity}x {refined_data['name']} would result in {final_volume:.1f}/{cargo_capacity} cargo (over by {space_needed:.1f}). Current: {current_volume:.1f}/{cargo_capacity}"

    # ===== MULTI-SOURCE REMOVAL =====
    # Remove ore from inventories (ship first, then station at current location)
    remaining = quantity
    
    # Take from ship cargo first
    from_ship = min(remaining, self.player.ship_cargo.get(raw_ore_id, 0))
    self.player.ship_cargo[raw_ore_id] -= from_ship
    if self.player.ship_cargo[raw_ore_id] == 0:
        del self.player.ship_cargo[raw_ore_id]
    remaining -= from_ship
    
    # If still need more, take from current station
    if remaining > 0:
        station_inv = self.player.get_station_inventory(self.player.location)
        from_station = min(remaining, station_inv.get(raw_ore_id, 0))
        station_inv[raw_ore_id] -= from_station
        if station_inv[raw_ore_id] == 0:
            del station_inv[raw_ore_id]
        remaining -= from_station
    
    # Safety check (should never happen if our inventory check passed)
    if remaining > 0:
        # Refund what we took
        self.player.add_item(raw_ore_id, from_ship)
        if 'from_station' in locals() and from_station > 0:
            station_inv = self.player.get_station_inventory(self.player.location)
            if raw_ore_id in station_inv:
                station_inv[raw_ore_id] += from_station
            else:
                station_inv[raw_ore_id] = from_station
        return False, "Error sourcing ore from inventories"

    # Add ALL refined resource to ship cargo
    success, message = self.player.add_item(refined_id, refined_quantity, cargo_capacity)
    if not success:
        # Refund the raw ore if adding refined fails (should not happen since we checked)
        self.player.add_item(raw_ore_id, quantity, cargo_capacity)
        return False, f"Failed to add refined resource: {message}"

    # Update stats
    self.player.stats["resources_refined"] += refined_quantity

    # Award XP for refining
    xp_reward = refined_quantity // 10 + 1
    self.player.add_experience(xp_reward)

    # Create result message
    yield_pct = (refined_quantity / quantity) * 100
    
    # Show source breakdown in message if multi-source
    if from_ship > 0 and remaining > 0:
        return True, f"Refined {quantity}x {raw_ore_data['name']} ({from_ship} ship, {quantity-from_ship} station) → {refined_quantity}x {refined_data['name']} ({yield_pct:.1f}% yield) (+{xp_reward} XP)"
    else:
        return True, f"Refined {quantity}x {raw_ore_data['name']} → {refined_quantity}x {refined_data['name']} ({yield_pct:.1f}% yield) (+{xp_reward} XP)"
```

---

## 3. Modified show_refine_view() for gui.py

Replace the method from lines 4437-4528 with:

```python
def show_refine_view(self):
    """Show ore refining interface with multi-source support"""
    self.clear_content()

    # Info message
    info_frame = tk.Frame(self.content_frame, bg=COLORS['bg_medium'], relief=tk.RIDGE, bd=1)
    info_frame.pack(fill=tk.X, pady=(0, 10), padx=10)

    tk.Label(
        info_frame,
        text="⚗️ Refine raw ores into refined resources. Yield is RNG-based: Common ores = 80-95%, Rare ores = 50-65%\nCan refine from ship cargo or station storage.",
        font=('Arial', 10),
        fg=COLORS['accent'],
        bg=COLORS['bg_medium']
    ).pack(pady=10, padx=10)

    # Main panel
    panel, content = self.create_panel(self.content_frame, "Refine Raw Ores")
    panel.pack(fill=tk.BOTH, expand=True)

    # Collect raw ores from all accessible inventories
    raw_ores_by_location = {}
    
    # Get from ship cargo
    for item_id, quantity in self.engine.player.ship_cargo.items():
        if item_id in RAW_RESOURCES:
            if item_id not in raw_ores_by_location:
                raw_ores_by_location[item_id] = {}
            raw_ores_by_location[item_id]['Ship'] = quantity
    
    # Get from accessible stations
    for location_id in self.engine.player.get_accessible_stations():
        if location_id != self.engine.player.location or location_id not in ['ship']:
            station_inv = self.engine.player.get_station_inventory(location_id)
            for item_id, quantity in station_inv.items():
                if item_id in RAW_RESOURCES and quantity > 0:
                    if item_id not in raw_ores_by_location:
                        raw_ores_by_location[item_id] = {}
                    location_name = LOCATIONS[location_id]['name']
                    raw_ores_by_location[item_id][location_name] = quantity

    # Aggregate totals
    raw_ores_in_cargo = {}
    for item_id, locations in raw_ores_by_location.items():
        raw_ores_in_cargo[item_id] = (sum(locations.values()), locations)

    if raw_ores_in_cargo:
        canvas = tk.Canvas(content, bg=COLORS['bg_medium'], highlightthickness=0)
        scrollbar = tk.Scrollbar(content, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['bg_medium'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        self.bind_mousewheel(canvas, scrollable_frame)

        for ore_id in sorted(raw_ores_in_cargo.keys()):
            total_quantity, location_breakdown = raw_ores_in_cargo[ore_id]
            ore_data = RAW_RESOURCES[ore_id]
            refined_id = ore_data.get("refines_to")

            if not refined_id:
                continue

            refined_data = RESOURCES[refined_id]
            rarity = ore_data.get("rarity", "common")
            min_yield, max_yield = REFINING_YIELD_RANGES.get(rarity, (0.7, 0.9))

            ore_frame = tk.Frame(scrollable_frame, bg=COLORS['bg_light'], relief=tk.RIDGE, bd=1)
            ore_frame.pack(fill=tk.X, pady=3, padx=5)

            info = tk.Frame(ore_frame, bg=COLORS['bg_light'])
            info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=8)

            tk.Label(
                info,
                text=f"{ore_data['name']} (x{total_quantity})",
                font=('Arial', 10, 'bold'),
                fg=COLORS['accent'],
                bg=COLORS['bg_light']
            ).pack(anchor='w')

            # Show location breakdown
            breakdown_str = " + ".join([f"{qty} {loc}" for loc, qty in location_breakdown.items()])
            tk.Label(
                info,
                text=f"Sources: {breakdown_str}",
                font=('Arial', 8),
                fg=COLORS['text_dim'],
                bg=COLORS['bg_light']
            ).pack(anchor='w')

            tk.Label(
                info,
                text=f"→ {refined_data['name']} | Yield: {int(min_yield*100)}-{int(max_yield*100)}% | Rarity: {rarity.replace('_', ' ').title()}",
                font=('Arial', 8),
                fg=COLORS['text_dim'],
                bg=COLORS['bg_light']
            ).pack(anchor='w')

            self.create_button(
                ore_frame,
                "Refine",
                lambda o=ore_id: self.refine_ore_dialog(o),
                width=10,
                style='success'
            ).pack(side=tk.RIGHT, padx=10)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    else:
        tk.Label(
            content,
            text="No raw ores to refine.\nGo mining to collect raw ores!",
            font=('Arial', 10),
            fg=COLORS['text_dim'],
            bg=COLORS['bg_medium'],
            justify=tk.CENTER
        ).pack(pady=50)
```

---

## 4. Modified refine_ore_dialog() for gui.py

Replace the method from lines 4530-4610 with:

```python
def refine_ore_dialog(self, ore_id):
    """Show dialog to refine ore (multi-source aware)"""
    dialog = tk.Toplevel(self.root)
    dialog.title("Refine Ore")
    dialog.geometry("400x250")
    dialog.configure(bg=COLORS['bg_medium'])

    ore_data = RAW_RESOURCES[ore_id]
    refined_data = RESOURCES[ore_data.get("refines_to")]
    
    # Get total available from all sources
    location_breakdown, max_qty = self.engine.player.get_total_accessible_quantity(ore_id)
    rarity = ore_data.get("rarity", "common")
    min_yield, max_yield = REFINING_YIELD_RANGES.get(rarity, (0.7, 0.9))

    tk.Label(
        dialog,
        text=f"Refine {ore_data['name']}",
        font=('Arial', 12, 'bold'),
        fg=COLORS['accent'],
        bg=COLORS['bg_medium']
    ).pack(pady=10)

    # Show availability by source
    availability_text = f"Available: {max_qty} units\n"
    for location, qty in location_breakdown.items():
        availability_text += f"  {location}: {qty}x\n"
    availability_text += f"Yield: {int(min_yield*100)}-{int(max_yield*100)}% → {refined_data['name']}"

    tk.Label(
        dialog,
        text=availability_text,
        font=('Arial', 9),
        fg=COLORS['text'],
        bg=COLORS['bg_medium']
    ).pack(pady=5, padx=10)

    qty_frame = tk.Frame(dialog, bg=COLORS['bg_medium'])
    qty_frame.pack(pady=10)

    tk.Label(
        qty_frame,
        text="Quantity:",
        font=('Arial', 10),
        fg=COLORS['text'],
        bg=COLORS['bg_medium']
    ).pack(side=tk.LEFT, padx=5)

    qty_entry = tk.Entry(qty_frame, width=10, font=('Arial', 10))
    qty_entry.pack(side=tk.LEFT, padx=5)
    qty_entry.insert(0, str(max_qty))

    def do_refine():
        try:
            quantity = int(qty_entry.get())
            if quantity <= 0:
                messagebox.showerror("Invalid Quantity", "Quantity must be greater than 0")
                return

            success, message = self.engine.refine_ore(ore_id, quantity)

            if success:
                messagebox.showinfo("Refining Complete", message)
                self.update_top_bar()
                dialog.destroy()
                self.show_refine_view()
            else:
                messagebox.showerror("Refining Failed", message)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number")

    button_frame = tk.Frame(dialog, bg=COLORS['bg_medium'])
    button_frame.pack(pady=10)

    self.create_button(
        button_frame,
        "Refine",
        do_refine,
        width=10,
        style='success'
    ).pack(side=tk.LEFT, padx=5)

    self.create_button(
        button_frame,
        "Cancel",
        dialog.destroy,
        width=10,
        style='danger'
    ).pack(side=tk.LEFT, padx=5)
```

---

## Implementation Order

1. Add helper method to `player.py` (ensures dependency is available)
2. Update `game_engine.py` refine_ore() method (core logic)
3. Update `gui.py` show_refine_view() method (UI display)
4. Update `gui.py` refine_ore_dialog() method (dialog display)
5. Test thoroughly

---

## Quick Reference: What Changed

| Component | Original | Updated |
|-----------|----------|---------|
| Inventory source | `ship_cargo` only | `ship_cargo + station_inventories` |
| Availability check | `has_item()` | `get_total_accessible_quantity()` |
| UI display | Single location | Multi-location with breakdown |
| Refining source | Ship only | Ship first, then station |
| Output location | Always ship | Always ship (refined is compact) |

