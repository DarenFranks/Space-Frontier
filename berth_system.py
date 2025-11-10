"""
Shipyard Berth System
Manages ship storage slots at different locations
"""

from typing import Dict, List, Optional, Tuple


class BerthManager:
    """Manages shipyard berths for storing multiple ships"""

    # Berth pricing by location type
    BERTH_PRICES = {
        "major_station": 50000,    # Major hubs like Nexus Prime
        "standard_station": 35000,  # Regular stations
        "outpost": 25000,          # Remote outposts
        "planet": 40000,           # Planet-side shipyards
    }

    def __init__(self):
        # Structure: {location_id: {"berths": [ship_id or None, ...], "max_berths": int}}
        self.shipyards: Dict[str, Dict] = {}

    def initialize_shipyard(self, location_id: str, location_type: str = "standard_station", starting_berths: int = 1):
        """Initialize a shipyard at a location"""
        if location_id not in self.shipyards:
            self.shipyards[location_id] = {
                "berths": [None] * starting_berths,  # Start with 1 free berth
                "max_berths": 10,  # Maximum berths that can be purchased
                "location_type": location_type,
            }

    def get_berth_price(self, location_id: str) -> int:
        """Get cost of purchasing a new berth at this location"""
        if location_id not in self.shipyards:
            return self.BERTH_PRICES["standard_station"]

        location_type = self.shipyards[location_id].get("location_type", "standard_station")
        base_price = self.BERTH_PRICES.get(location_type, 35000)

        # Price increases with number of berths owned
        current_berths = len(self.shipyards[location_id]["berths"])
        multiplier = 1.0 + (current_berths * 0.2)  # 20% more per berth

        return int(base_price * multiplier)

    def has_empty_berth(self, location_id: str) -> bool:
        """Check if location has an empty berth"""
        if location_id not in self.shipyards:
            return False

        return None in self.shipyards[location_id]["berths"]

    def get_empty_berth_index(self, location_id: str) -> Optional[int]:
        """Get index of first empty berth"""
        if location_id not in self.shipyards:
            return None

        berths = self.shipyards[location_id]["berths"]
        try:
            return berths.index(None)
        except ValueError:
            return None

    def get_berth_count(self, location_id: str) -> Tuple[int, int]:
        """Get (used_berths, total_berths) at location"""
        if location_id not in self.shipyards:
            return (0, 0)

        berths = self.shipyards[location_id]["berths"]
        used = sum(1 for b in berths if b is not None)
        return (used, len(berths))

    def can_purchase_berth(self, location_id: str) -> bool:
        """Check if player can buy another berth at this location"""
        if location_id not in self.shipyards:
            return False

        current_count = len(self.shipyards[location_id]["berths"])
        max_berths = self.shipyards[location_id]["max_berths"]

        return current_count < max_berths

    def purchase_berth(self, location_id: str, player_credits: int) -> Tuple[bool, str, int]:
        """
        Purchase a new berth at location
        Returns: (success, message, cost)
        """
        if location_id not in self.shipyards:
            return False, "No shipyard at this location", 0

        if not self.can_purchase_berth(location_id):
            max_berths = self.shipyards[location_id]["max_berths"]
            return False, f"Maximum berths ({max_berths}) already owned at this location", 0

        cost = self.get_berth_price(location_id)

        if player_credits < cost:
            return False, f"Insufficient credits. Berth costs {cost:,} CR", 0

        # Add new berth
        self.shipyards[location_id]["berths"].append(None)

        return True, f"Purchased berth for {cost:,} CR", cost

    def store_ship(self, location_id: str, ship_id: str, berth_index: Optional[int] = None) -> Tuple[bool, str]:
        """
        Store a ship in a berth
        Returns: (success, message)
        """
        if location_id not in self.shipyards:
            return False, "No shipyard at this location"

        if berth_index is None:
            berth_index = self.get_empty_berth_index(location_id)

        if berth_index is None:
            return False, "No empty berths available"

        berths = self.shipyards[location_id]["berths"]

        if berth_index >= len(berths):
            return False, "Invalid berth index"

        if berths[berth_index] is not None:
            return False, "Berth already occupied"

        berths[berth_index] = ship_id
        return True, f"Ship stored in berth {berth_index + 1}"

    def remove_ship(self, location_id: str, ship_id: str) -> Tuple[bool, str]:
        """
        Remove a ship from its berth
        Returns: (success, message)
        """
        if location_id not in self.shipyards:
            return False, "No shipyard at this location"

        berths = self.shipyards[location_id]["berths"]

        try:
            berth_index = berths.index(ship_id)
            berths[berth_index] = None
            return True, f"Ship removed from berth {berth_index + 1}"
        except ValueError:
            return False, "Ship not found in this shipyard"

    def get_ships_at_location(self, location_id: str) -> List[str]:
        """Get list of ship IDs stored at this location"""
        if location_id not in self.shipyards:
            return []

        return [ship_id for ship_id in self.shipyards[location_id]["berths"] if ship_id is not None]

    def get_berth_overview(self, location_id: str) -> Dict:
        """Get overview of berths at location"""
        if location_id not in self.shipyards:
            return {
                "exists": False,
                "berths": [],
                "used": 0,
                "total": 0,
                "can_purchase": False,
                "purchase_cost": 0,
            }

        shipyard = self.shipyards[location_id]
        used, total = self.get_berth_count(location_id)

        return {
            "exists": True,
            "berths": shipyard["berths"].copy(),
            "used": used,
            "total": total,
            "can_purchase": self.can_purchase_berth(location_id),
            "purchase_cost": self.get_berth_price(location_id),
            "max_berths": shipyard["max_berths"],
        }

    def to_dict(self) -> Dict:
        """Serialize berth data for saving"""
        return {
            "shipyards": self.shipyards
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'BerthManager':
        """Load berth data from save"""
        manager = cls()
        manager.shipyards = data.get("shipyards", {})
        return manager


# Example usage
if __name__ == "__main__":
    # Test the berth system
    berth_mgr = BerthManager()

    # Initialize shipyard
    berth_mgr.initialize_shipyard("nexus_prime", "major_station", starting_berths=1)

    print("Berth Overview:")
    overview = berth_mgr.get_berth_overview("nexus_prime")
    print(f"  Used: {overview['used']}/{overview['total']}")
    print(f"  Can purchase: {overview['can_purchase']}")
    print(f"  Cost: {overview['purchase_cost']:,} CR")

    # Store a ship
    success, msg = berth_mgr.store_ship("nexus_prime", "scout_standard_mk1")
    print(f"\nStore ship: {msg}")

    # Try to store another without berth
    success, msg = berth_mgr.store_ship("nexus_prime", "fighter_standard_mk1")
    print(f"Store second ship: {msg}")

    # Purchase berth
    success, msg, cost = berth_mgr.purchase_berth("nexus_prime", 100000)
    print(f"\nPurchase berth: {msg}")

    # Now store second ship
    success, msg = berth_mgr.store_ship("nexus_prime", "fighter_standard_mk1")
    print(f"Store second ship: {msg}")

    # Get ships
    ships = berth_mgr.get_ships_at_location("nexus_prime")
    print(f"\nShips at location: {ships}")

    overview = berth_mgr.get_berth_overview("nexus_prime")
    print(f"Final berths: {overview['used']}/{overview['total']}")
