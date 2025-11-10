"""
Faction and Territory System
Handles faction relations, territory control, and influence
"""

from typing import Dict, List, Optional
from data import FACTIONS, LOCATIONS


class FactionManager:
    """Manages factions and territory control"""

    def __init__(self):
        self.faction_data = dict(FACTIONS)
        self.territory_control: Dict[str, str] = {}  # location_id: controlling_faction

        # Initialize territory control
        for location_id, location_data in LOCATIONS.items():
            if "faction" in location_data:
                self.territory_control[location_id] = location_data["faction"]

        # Track ongoing conflicts
        self.conflicts: List[Dict] = []

    def get_faction_info(self, faction_id: str) -> Optional[Dict]:
        """Get information about a faction"""
        return self.faction_data.get(faction_id)

    def get_controlling_faction(self, location_id: str) -> Optional[str]:
        """Get faction that controls a location"""
        return self.territory_control.get(location_id)

    def get_faction_territory(self, faction_id: str) -> List[str]:
        """Get all locations controlled by faction"""
        return [loc_id for loc_id, controller in self.territory_control.items()
                if controller == faction_id]

    def calculate_faction_power(self, faction_id: str) -> int:
        """Calculate faction power based on territory"""
        territory_count = len(self.get_faction_territory(faction_id))
        faction_info = self.get_faction_info(faction_id)

        if not faction_info:
            return 0

        # Base power from territory
        power = territory_count * 100

        # Bonus from faction traits
        bonuses = faction_info.get("bonuses", {})
        if "combat" in bonuses:
            power += int(bonuses["combat"] * 500)
        if "territory_control" in bonuses:
            power += int(bonuses["territory_control"] * 500)

        return power

    def get_faction_relations(self, faction_a: str, faction_b: str) -> float:
        """Get relationship value between two factions"""
        if faction_a == faction_b:
            return 1.0

        faction_info = self.get_faction_info(faction_a)
        if not faction_info:
            return 0.0

        relations = faction_info.get("relations", {})
        return relations.get(faction_b, 0.0)

    def is_hostile(self, faction_a: str, faction_b: str) -> bool:
        """Check if two factions are hostile"""
        relation = self.get_faction_relations(faction_a, faction_b)
        return relation < -0.3

    def is_allied(self, faction_a: str, faction_b: str) -> bool:
        """Check if two factions are allied"""
        relation = self.get_faction_relations(faction_a, faction_b)
        return relation > 0.5

    def get_player_access(self, location_id: str, player_standings: Dict[str, float]) -> Dict:
        """
        Check player's access to a location based on faction standing.
        Returns access level and restrictions.
        """
        controlling_faction = self.get_controlling_faction(location_id)

        if not controlling_faction:
            return {"access": "full", "restrictions": []}

        player_standing = player_standings.get(controlling_faction, 0.0)

        # Determine access level
        if player_standing >= 0.5:
            access = "full"
            restrictions = []
        elif player_standing >= 0.0:
            access = "limited"
            restrictions = ["Some services restricted", "Higher prices"]
        elif player_standing >= -0.5:
            access = "hostile"
            restrictions = ["Most services unavailable", "Risk of attack"]
        else:
            access = "forbidden"
            restrictions = ["Attack on sight", "Cannot dock"]

        return {
            "access": access,
            "restrictions": restrictions,
            "controlling_faction": FACTIONS[controlling_faction]["name"],
            "player_standing": player_standing
        }

    def start_conflict(self, location_id: str, attacking_faction: str):
        """Start a territorial conflict"""
        defending_faction = self.get_controlling_faction(location_id)

        if not defending_faction or defending_faction == attacking_faction:
            return

        conflict = {
            "location_id": location_id,
            "attacker": attacking_faction,
            "defender": defending_faction,
            "attacker_progress": 0,
            "duration": 0
        }

        self.conflicts.append(conflict)

    def update_conflicts(self):
        """Simulate ongoing conflicts"""
        resolved_conflicts = []

        for conflict in self.conflicts:
            attacker_power = self.calculate_faction_power(conflict["attacker"])
            defender_power = self.calculate_faction_power(conflict["defender"])

            # Simulate progress
            if attacker_power > defender_power:
                conflict["attacker_progress"] += 10
            elif defender_power > attacker_power:
                conflict["attacker_progress"] -= 5

            conflict["duration"] += 1

            # Check if conflict resolved
            if conflict["attacker_progress"] >= 100:
                # Attacker wins
                self.territory_control[conflict["location_id"]] = conflict["attacker"]
                resolved_conflicts.append(conflict)
            elif conflict["attacker_progress"] <= -50 or conflict["duration"] > 100:
                # Defender wins or stalemate
                resolved_conflicts.append(conflict)

        # Remove resolved conflicts
        for conflict in resolved_conflicts:
            self.conflicts.remove(conflict)

    def get_faction_bonuses(self, faction_id: str, player_standing: float) -> Dict[str, float]:
        """
        Get bonuses player receives based on faction standing.
        Higher standing = better bonuses.
        """
        faction_info = self.get_faction_info(faction_id)
        if not faction_info:
            return {}

        base_bonuses = faction_info.get("bonuses", {})

        # Scale bonuses by standing (max at 1.0 standing)
        standing_multiplier = max(0, player_standing)

        scaled_bonuses = {}
        for bonus_type, bonus_value in base_bonuses.items():
            scaled_bonuses[bonus_type] = bonus_value * standing_multiplier

        return scaled_bonuses

    def get_market_price_modifier(self, location_id: str,
                                  player_standings: Dict[str, float]) -> float:
        """
        Get price modifier for markets based on faction standing.
        Returns multiplier (1.0 = normal, <1.0 = discount, >1.0 = markup)
        """
        controlling_faction = self.get_controlling_faction(location_id)

        if not controlling_faction:
            return 1.0

        player_standing = player_standings.get(controlling_faction, 0.0)

        # Good standing = better prices
        if player_standing >= 0.75:
            return 0.85  # 15% discount
        elif player_standing >= 0.5:
            return 0.92  # 8% discount
        elif player_standing >= 0.0:
            return 1.0  # Normal prices
        elif player_standing >= -0.5:
            return 1.2  # 20% markup
        else:
            return 1.5  # 50% markup

    def get_all_factions_summary(self, player_standings: Dict[str, float]) -> List[Dict]:
        """Get summary of all factions"""
        summaries = []

        for faction_id, faction_data in self.faction_data.items():
            player_standing = player_standings.get(faction_id, 0.0)
            territory = self.get_faction_territory(faction_id)
            power = self.calculate_faction_power(faction_id)

            # Determine relationship status
            if player_standing >= 0.75:
                status = "Excellent"
            elif player_standing >= 0.5:
                status = "Good"
            elif player_standing >= 0.25:
                status = "Friendly"
            elif player_standing >= -0.25:
                status = "Neutral"
            elif player_standing >= -0.5:
                status = "Unfriendly"
            elif player_standing >= -0.75:
                status = "Hostile"
            else:
                status = "At War"

            summaries.append({
                "id": faction_id,
                "name": faction_data["name"],
                "description": faction_data["description"],
                "territory_count": len(territory),
                "power": power,
                "player_standing": player_standing,
                "status": status
            })

        return summaries

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "territory_control": self.territory_control,
            "conflicts": self.conflicts
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'FactionManager':
        """Create from dictionary"""
        manager = cls()
        manager.territory_control = data.get("territory_control", {})
        manager.conflicts = data.get("conflicts", [])
        return manager
