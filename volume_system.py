"""
Volume System
Calculates volumes for all items and enforces cargo capacity
"""

from typing import Dict
from data import RESOURCES, SHIP_COMPONENTS, VESSEL_CLASSES, MODULES, COMPONENT_RECIPES


def get_item_volume(item_id: str) -> float:
    """Get the volume of a single item"""

    # Check resources (raw and refined materials)
    if item_id in RESOURCES:
        return RESOURCES[item_id].get('volume', 1.0)

    # Check components
    if item_id in SHIP_COMPONENTS:
        # If volume is set, use it
        if 'volume' in SHIP_COMPONENTS[item_id]:
            return SHIP_COMPONENTS[item_id]['volume']

        # Otherwise calculate based on materials (125% of material volume)
        if item_id in COMPONENT_RECIPES:
            recipe = COMPONENT_RECIPES[item_id]
            material_volume = 0
            for mat_id, qty in recipe.get('materials', {}).items():
                if mat_id in RESOURCES:
                    material_volume += RESOURCES[mat_id]['volume'] * qty
            return material_volume * 1.25  # Components are 125% of material volume

        return 10.0  # Default for components

    # Check ships
    if item_id in VESSEL_CLASSES:
        # Ships are HUGE - based on ship class
        ship_data = VESSEL_CLASSES[item_id]
        class_type = ship_data.get('class_type', 'scout')

        # Base volumes by ship class (in cargo units)
        class_volumes = {
            'scout': 500,
            'fighter': 600,
            'hauler': 800,
            'cruiser': 1000,
            'destroyer': 1500,
            'battleship': 2500,
            'carrier': 2000,
            'refinery': 1800
        }

        base = class_volumes.get(class_type, 500)

        # Multiply by tier
        tier_mult = ship_data.get('tier_num', 1)
        return base * tier_mult

    # Check modules
    if item_id in MODULES:
        # Modules vary by type and tier
        module_data = MODULES[item_id]
        tier = module_data.get('tier', 1)
        module_type = module_data.get('type', 'utility')

        # Base volumes by module type
        type_volumes = {
            'weapon': 15,
            'defense': 20,
            'utility': 10,
            'engine': 25
        }

        base = type_volumes.get(module_type, 10)
        return base * tier

    # Unknown item - default small volume
    return 1.0


def calculate_cargo_volume(inventory: Dict[str, int]) -> float:
    """Calculate total volume of items in inventory"""
    total = 0.0
    for item_id, quantity in inventory.items():
        total += get_item_volume(item_id) * quantity
    return total


def get_cargo_capacity(vessel_data: dict) -> float:
    """Get cargo capacity of a vessel"""
    return vessel_data.get('cargo_capacity', 500)


def can_add_item(inventory: Dict[str, int], cargo_capacity: float, item_id: str, quantity: int) -> tuple[bool, str]:
    """
    Check if items can be added to inventory
    Returns: (can_add, message)
    """
    current_volume = calculate_cargo_volume(inventory)
    item_volume = get_item_volume(item_id) * quantity
    new_volume = current_volume + item_volume

    if new_volume > cargo_capacity:
        space_needed = new_volume - cargo_capacity
        return False, f"Insufficient cargo space. Need {space_needed:.1f} more capacity."

    return True, f"Can add {quantity}x {item_id}"


def get_max_quantity_can_add(inventory: Dict[str, int], cargo_capacity: float, item_id: str) -> int:
    """Calculate maximum quantity of an item that can be added"""
    current_volume = calculate_cargo_volume(inventory)
    available_space = cargo_capacity - current_volume

    if available_space <= 0:
        return 0

    item_volume = get_item_volume(item_id)
    if item_volume <= 0:
        return 999  # No volume constraint

    return int(available_space / item_volume)
