"""
Shipyard System
Handles buying, selling, and upgrading ships
"""

from typing import Dict, List, Optional, Tuple
from data import VESSEL_CLASSES


class Shipyard:
    """Manages ship purchases and sales"""

    def __init__(self):
        self.trade_in_value_multiplier = 0.70  # Get 70% of base cost when selling

    def get_available_ships(self, player_level: int, location_services: List[str]) -> List[Dict]:
        """Get list of ships available for purchase at current location"""
        if "shipyard" not in location_services:
            return []

        available = []

        for ship_id, ship_data in VESSEL_CLASSES.items():
            # Check level requirement
            level_req = ship_data.get("level_requirement", 1)
            if player_level >= level_req:
                available.append({
                    "id": ship_id,
                    "name": ship_data["name"],
                    "type": ship_data["type"],
                    "tier": ship_data.get("tier", 1),
                    "cost": ship_data["cost"],
                    "level_req": level_req,
                    "stats": {
                        "hull_hp": ship_data["hull_hp"],
                        "shield_capacity": ship_data["base_shield_capacity"],
                        "armor": ship_data["armor_rating"],
                        "speed": ship_data["speed"],
                        "cargo": ship_data["cargo_capacity"]
                    }
                })

        # Sort by tier then cost
        available.sort(key=lambda x: (x["tier"], x["cost"]))

        return available

    def get_ship_info(self, ship_id: str) -> Optional[Dict]:
        """Get detailed information about a specific ship"""
        if ship_id not in VESSEL_CLASSES:
            return None

        ship_data = VESSEL_CLASSES[ship_id]

        return {
            "id": ship_id,
            "name": ship_data["name"],
            "type": ship_data["type"],
            "tier": ship_data.get("tier", 1),
            "cost": ship_data["cost"],
            "level_req": ship_data.get("level_requirement", 1),
            "description": f"{ship_data['type'].title()} class vessel - Tier {ship_data.get('tier', 1)}",
            "stats": {
                "hull_hp": ship_data["hull_hp"],
                "shield_capacity": ship_data["base_shield_capacity"],
                "armor": ship_data["armor_rating"],
                "speed": ship_data["speed"],
                "cargo": ship_data["cargo_capacity"]
            },
            "module_slots": ship_data["module_slots"]
        }

    def calculate_trade_in_value(self, current_ship_id: str) -> int:
        """Calculate trade-in value for current ship"""
        if current_ship_id not in VESSEL_CLASSES:
            return 0

        base_cost = VESSEL_CLASSES[current_ship_id]["cost"]
        return int(base_cost * self.trade_in_value_multiplier)

    def can_afford_ship(self, ship_id: str, player_credits: int, trade_in_value: int = 0) -> bool:
        """Check if player can afford a ship"""
        if ship_id not in VESSEL_CLASSES:
            return False

        cost = VESSEL_CLASSES[ship_id]["cost"]
        final_cost = cost - trade_in_value

        return player_credits >= final_cost

    def purchase_ship(
        self,
        ship_id: str,
        player_credits: int,
        player_level: int,
        current_ship_id: str = None,
        trade_in: bool = False
    ) -> Tuple[bool, str, int]:
        """
        Purchase a ship
        Returns: (success, message, cost)
        """
        if ship_id not in VESSEL_CLASSES:
            return False, "Invalid ship selection", 0

        ship_data = VESSEL_CLASSES[ship_id]

        # Check level requirement
        level_req = ship_data.get("level_requirement", 1)
        if player_level < level_req:
            return False, f"Requires level {level_req}", 0

        # Calculate cost
        base_cost = ship_data["cost"]
        trade_in_value = 0

        if trade_in and current_ship_id:
            trade_in_value = self.calculate_trade_in_value(current_ship_id)

        final_cost = base_cost - trade_in_value

        # Check funds
        if player_credits < final_cost:
            return False, f"Insufficient credits. Need {final_cost:,} CR", 0

        message = f"Purchased {ship_data['name']} for {final_cost:,} CR"
        if trade_in_value > 0:
            message += f" (with {trade_in_value:,} CR trade-in)"

        return True, message, final_cost

    def sell_ship(self, ship_id: str) -> Tuple[bool, str, int]:
        """
        Sell a ship for its trade-in value
        Returns: (success, message, value)
        """
        if ship_id not in VESSEL_CLASSES:
            return False, "Invalid ship", 0

        value = self.calculate_trade_in_value(ship_id)
        ship_name = VESSEL_CLASSES[ship_id]["name"]

        return True, f"Sold {ship_name} for {value:,} CR", value

    def get_ships_by_type(self, ship_type: str, player_level: int) -> List[Dict]:
        """Get all ships of a specific type that player can access"""
        ships = []

        for ship_id, ship_data in VESSEL_CLASSES.items():
            if ship_data["type"] == ship_type:
                level_req = ship_data.get("level_requirement", 1)
                if player_level >= level_req:
                    ships.append({
                        "id": ship_id,
                        "name": ship_data["name"],
                        "tier": ship_data.get("tier", 1),
                        "cost": ship_data["cost"],
                        "level_req": level_req
                    })

        ships.sort(key=lambda x: x["tier"])
        return ships

    def get_upgrade_path(self, current_ship_id: str, player_level: int) -> List[Dict]:
        """Get possible upgrade ships from current vessel"""
        if current_ship_id not in VESSEL_CLASSES:
            return []

        current_ship = VESSEL_CLASSES[current_ship_id]
        current_type = current_ship["type"]
        current_tier = current_ship.get("tier", 1)

        upgrades = []

        for ship_id, ship_data in VESSEL_CLASSES.items():
            # Same type, higher tier
            if ship_data["type"] == current_type and ship_data.get("tier", 1) > current_tier:
                level_req = ship_data.get("level_requirement", 1)
                if player_level >= level_req:
                    upgrades.append({
                        "id": ship_id,
                        "name": ship_data["name"],
                        "tier": ship_data.get("tier", 1),
                        "cost": ship_data["cost"],
                        "level_req": level_req,
                        "cost_with_trade_in": ship_data["cost"] - self.calculate_trade_in_value(current_ship_id)
                    })

        upgrades.sort(key=lambda x: x["tier"])
        return upgrades
