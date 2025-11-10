"""
Recycling System
Break down components and ships for materials
"""

import random
from typing import Dict, Tuple
from data import SHIP_COMPONENTS, COMPONENT_RECIPES, SHIP_RECIPES, VESSEL_CLASSES, RESOURCES


class RecyclingSystem:
    """Handles recycling of components and ships into materials"""

    def __init__(self):
        self.recovery_rate = 0.80  # Return 80% of materials

    def recycle_component(self, comp_id: str) -> Tuple[bool, str, Dict[str, int]]:
        """
        Recycle a component into materials
        Returns: (success, message, materials_dict)
        """
        if comp_id not in SHIP_COMPONENTS:
            return False, "Invalid component", {}

        if comp_id not in COMPONENT_RECIPES:
            return False, "Component cannot be recycled", {}

        recipe = COMPONENT_RECIPES[comp_id]
        materials_required = recipe.get("materials", {})

        if not materials_required:
            return False, "Component has no materials to recover", {}

        # Calculate total material value
        total_materials = sum(materials_required.values())
        recovered_total = int(total_materials * self.recovery_rate)

        # Distribute recovered materials randomly among the recipe materials
        recovered_materials = self._distribute_materials_randomly(
            materials_required,
            recovered_total
        )

        comp_name = SHIP_COMPONENTS[comp_id]["name"]
        material_list = ", ".join([f"{qty}x {mat}" for mat, qty in recovered_materials.items()])

        return True, f"Recycled {comp_name}. Recovered: {material_list}", recovered_materials

    def recycle_ship(self, ship_id: str) -> Tuple[bool, str, Dict[str, int]]:
        """
        Recycle a ship into materials (from its components)
        Returns: (success, message, materials_dict)
        """
        if ship_id not in VESSEL_CLASSES:
            return False, "Invalid ship", {}

        if ship_id not in SHIP_RECIPES:
            return False, "Ship cannot be recycled", {}

        ship_recipe = SHIP_RECIPES[ship_id]
        required_components = ship_recipe.get("components", {})

        if not required_components:
            return False, "Ship has no components to recover", {}

        # Collect all materials from all components
        all_materials = {}

        for comp_id, quantity in required_components.items():
            if comp_id in COMPONENT_RECIPES:
                comp_recipe = COMPONENT_RECIPES[comp_id]
                comp_materials = comp_recipe.get("materials", {})

                for mat, mat_qty in comp_materials.items():
                    all_materials[mat] = all_materials.get(mat, 0) + (mat_qty * quantity)

        if not all_materials:
            return False, "Ship has no materials to recover", {}

        # Calculate total material value
        total_materials = sum(all_materials.values())
        recovered_total = int(total_materials * self.recovery_rate)

        # Distribute recovered materials randomly
        recovered_materials = self._distribute_materials_randomly(
            all_materials,
            recovered_total
        )

        ship_name = VESSEL_CLASSES[ship_id]["name"]
        material_list = ", ".join([f"{qty}x {mat}" for mat, qty in recovered_materials.items()])

        return True, f"Recycled {ship_name}. Recovered: {material_list}", recovered_materials

    def _distribute_materials_randomly(
        self,
        material_types: Dict[str, int],
        total_to_distribute: int
    ) -> Dict[str, int]:
        """
        Distribute a total amount randomly among material types
        Each material type from the recipe has a chance to receive materials
        """
        if not material_types or total_to_distribute <= 0:
            return {}

        available_materials = list(material_types.keys())
        distributed = {}
        remaining = total_to_distribute

        # Randomly distribute materials
        for material in available_materials[:-1]:  # All but last
            if remaining <= 0:
                break

            # Random amount (0 to remaining, weighted by original recipe)
            original_weight = material_types[material]
            total_weight = sum(material_types.values())
            expected_share = int((original_weight / total_weight) * total_to_distribute)

            # Add randomness: ±30% of expected share
            min_amount = max(0, int(expected_share * 0.7))
            max_amount = min(remaining, int(expected_share * 1.3))

            if max_amount > 0:
                amount = random.randint(min_amount, max_amount)
                if amount > 0:
                    distributed[material] = amount
                    remaining -= amount

        # Give remaining to last material (if any materials left)
        if remaining > 0 and available_materials:
            last_material = available_materials[-1]
            distributed[last_material] = distributed.get(last_material, 0) + remaining

        return distributed

    def get_recyclable_items(self, inventory: Dict[str, int]) -> Dict[str, list]:
        """
        Get list of recyclable items from player inventory
        Returns: {"components": [...], "ships": [...]}
        """
        recyclable = {"components": [], "ships": []}

        for item_id, quantity in inventory.items():
            if quantity > 0:
                if item_id in SHIP_COMPONENTS:
                    recyclable["components"].append({
                        "id": item_id,
                        "name": SHIP_COMPONENTS[item_id]["name"],
                        "quantity": quantity
                    })
                elif item_id in VESSEL_CLASSES:
                    recyclable["ships"].append({
                        "id": item_id,
                        "name": VESSEL_CLASSES[item_id]["name"],
                        "quantity": quantity
                    })

        return recyclable

    def preview_recycle_component(self, comp_id: str) -> Dict[str, int]:
        """Preview what materials would be recovered from recycling a component"""
        if comp_id not in COMPONENT_RECIPES:
            return {}

        recipe = COMPONENT_RECIPES[comp_id]
        materials_required = recipe.get("materials", {})

        # Show expected recovery (not random)
        recovered = {}
        for mat, qty in materials_required.items():
            recovered[mat] = int(qty * self.recovery_rate)

        return recovered

    def preview_recycle_ship(self, ship_id: str) -> Dict[str, int]:
        """Preview what materials would be recovered from recycling a ship"""
        if ship_id not in SHIP_RECIPES:
            return {}

        ship_recipe = SHIP_RECIPES[ship_id]
        required_components = ship_recipe.get("components", {})

        all_materials = {}
        for comp_id, quantity in required_components.items():
            if comp_id in COMPONENT_RECIPES:
                comp_materials = COMPONENT_RECIPES[comp_id].get("materials", {})
                for mat, mat_qty in comp_materials.items():
                    all_materials[mat] = all_materials.get(mat, 0) + (mat_qty * quantity)

        # Show expected recovery
        recovered = {}
        for mat, qty in all_materials.items():
            recovered[mat] = int(qty * self.recovery_rate)

        return recovered
