"""
Player Character System
Handles player stats, skills, inventory, and progression
"""

import time
from typing import Dict, List, Optional, Tuple
from data import SKILLS
from config import BASE_SKILL_TRAIN_TIME, SKILL_TIME_MULTIPLIER
from volume_system import calculate_cargo_volume, can_add_item


class Player:
    """Represents the player character"""

    def __init__(self, name: str, credits: int = 50000):
        self.name = name
        self.credits = credits
        self.location = "nexus_prime"

        # Level system
        self.level = 1
        self.experience = 0
        self.experience_to_next = 1000

        # Skills system
        self.skills: Dict[str, int] = {skill_id: 0 for skill_id in SKILLS.keys()}
        self.skill_training: List[Dict] = []  # List of currently training skills

        # Inventory systems
        self.ship_cargo: Dict[str, int] = {}  # Items in ship cargo hold
        self.station_inventories: Dict[str, Dict[str, int]] = {}  # location_id: {item_id: quantity}

        # Backwards compatibility - inventory now refers to ship_cargo
        self.inventory = self.ship_cargo

        # Statistics
        self.stats = {
            "total_earnings": 0,
            "total_spent": 0,
            "contracts_completed": 0,
            "enemies_destroyed": 0,
            "resources_mined": 0,
            "resources_refined": 0,
            "items_manufactured": 0,
            "distance_traveled": 0,
            "time_played": 0
        }

        # Faction standings
        self.faction_standings: Dict[str, float] = {
            "meridian_collective": 0.0,
            "cipher_dominion": 0.0,
            "technocrat_union": 0.0,
            "void_corsairs": -0.2  # Start slightly hostile with pirates
        }

        # Shipyard berths - track owned berths at each location
        # Structure: {location_id: {"berths": [ship_id or None, ...]}}
        # BerthManager handles this in game_engine
        self.current_ship_id: Optional[str] = None  # Currently active ship

        # Game time tracking
        self.game_start_time = time.time()

        # Exploration tracking (for fog of war)
        self.visited_locations = {"nexus_prime"}  # Start with current location visible

    def add_credits(self, amount: int):
        """Add credits to player"""
        self.credits += amount
        if amount > 0:
            self.stats["total_earnings"] += amount

    def spend_credits(self, amount: int) -> bool:
        """Attempt to spend credits. Returns True if successful."""
        if self.credits >= amount:
            self.credits -= amount
            self.stats["total_spent"] += amount
            return True
        return False

    def add_item(self, item_id: str, quantity: int = 1, cargo_capacity: Optional[float] = None) -> Tuple[bool, str]:
        """
        Add items to inventory with optional cargo capacity check
        Returns: (success, message)
        """
        # If cargo capacity is provided, check if items fit
        if cargo_capacity is not None:
            can_add, message = can_add_item(self.inventory, cargo_capacity, item_id, quantity)
            if not can_add:
                return False, message

        # Add items to inventory
        if item_id in self.inventory:
            self.inventory[item_id] += quantity
        else:
            self.inventory[item_id] = quantity

        return True, f"Added {quantity}x {item_id}"

    def remove_item(self, item_id: str, quantity: int = 1) -> bool:
        """Remove items from inventory. Returns True if successful."""
        if item_id in self.inventory and self.inventory[item_id] >= quantity:
            self.inventory[item_id] -= quantity
            if self.inventory[item_id] == 0:
                del self.inventory[item_id]
            return True
        return False

    def remove_item_multi_source(self, item_id: str, quantity: int) -> tuple[bool, Dict[str, int]]:
        """
        Remove items from ship and station storage (current location only).
        Prioritizes ship cargo first, then station storage.
        Returns: (success, {"ship": qty_removed, "station": qty_removed})
        """
        quantities = self.get_total_accessible_quantity(item_id)

        if quantities["total"] < quantity:
            return False, {"ship": 0, "station": 0}

        remaining = quantity
        removed_from_ship = 0
        removed_from_station = 0

        # Remove from ship first
        ship_available = quantities["ship"]
        if ship_available > 0:
            to_remove = min(remaining, ship_available)
            self.ship_cargo[item_id] -= to_remove
            if self.ship_cargo[item_id] == 0:
                del self.ship_cargo[item_id]
            removed_from_ship = to_remove
            remaining -= to_remove

        # Remove from station if needed
        if remaining > 0 and quantities["station"] > 0:
            station_inv = self.get_station_inventory(self.location)
            to_remove = min(remaining, quantities["station"])
            station_inv[item_id] -= to_remove
            if station_inv[item_id] == 0:
                del station_inv[item_id]
            removed_from_station = to_remove
            remaining -= to_remove

        return True, {"ship": removed_from_ship, "station": removed_from_station}

    def get_cargo_volume(self) -> float:
        """Get current cargo volume usage"""
        return calculate_cargo_volume(self.inventory)

    def has_item(self, item_id: str, quantity: int = 1) -> bool:
        """Check if player has item in ship cargo"""
        return item_id in self.ship_cargo and self.ship_cargo[item_id] >= quantity

    def get_total_accessible_quantity(self, item_id: str) -> Dict[str, int]:
        """
        Get total quantity of an item accessible from ship and current station.
        Returns: {"ship": qty, "station": qty, "total": qty}
        """
        ship_qty = self.ship_cargo.get(item_id, 0)
        station_qty = 0

        # Get quantity from current location's station storage
        if self.location in self.station_inventories:
            station_qty = self.station_inventories[self.location].get(item_id, 0)

        return {
            "ship": ship_qty,
            "station": station_qty,
            "total": ship_qty + station_qty
        }

    def get_station_inventory(self, location_id: str) -> Dict[str, int]:
        """Get inventory at a specific station"""
        if location_id not in self.station_inventories:
            self.station_inventories[location_id] = {}
        return self.station_inventories[location_id]

    def can_access_remote_stations(self) -> bool:
        """Check if player can access remote station inventories"""
        # Requires logistics_management skill level 5+
        return self.get_skill_level("logistics_management") >= 5

    def get_accessible_stations(self) -> List[str]:
        """Get list of stations player can access inventory from"""
        accessible = [self.location]  # Always can access current location

        if self.can_access_remote_stations():
            # Can access all stations where player has inventory
            accessible.extend([loc for loc in self.station_inventories.keys() if loc != self.location])

        return accessible

    def transfer_to_station(self, item_id: str, quantity: int, location_id: str = None) -> tuple[bool, str]:
        """Transfer items from ship cargo to station storage"""
        if location_id is None:
            location_id = self.location

        # Can only transfer to current location
        if location_id != self.location:
            return False, "Can only transfer items at your current location"

        if not self.has_item(item_id, quantity):
            return False, "Insufficient items in ship cargo"

        # Remove from ship
        self.remove_item(item_id, quantity)

        # Add to station
        station_inv = self.get_station_inventory(location_id)
        if item_id in station_inv:
            station_inv[item_id] += quantity
        else:
            station_inv[item_id] = quantity

        return True, f"Transferred {quantity}x to station storage"

    def transfer_to_ship(self, item_id: str, quantity: int, location_id: str = None) -> tuple[bool, str]:
        """Transfer items from station storage to ship cargo"""
        if location_id is None:
            location_id = self.location

        # Check if can access this station
        if location_id not in self.get_accessible_stations():
            return False, "Cannot access this station's inventory"

        station_inv = self.get_station_inventory(location_id)

        if item_id not in station_inv or station_inv[item_id] < quantity:
            return False, "Insufficient items in station storage"

        # Remove from station
        station_inv[item_id] -= quantity
        if station_inv[item_id] == 0:
            del station_inv[item_id]

        # Add to ship
        self.add_item(item_id, quantity)

        return True, f"Transferred {quantity}x to ship cargo"

    def get_total_item_count(self, item_id: str) -> int:
        """Get total count of item across ship and all accessible stations"""
        total = self.ship_cargo.get(item_id, 0)

        for location_id in self.get_accessible_stations():
            station_inv = self.get_station_inventory(location_id)
            total += station_inv.get(item_id, 0)

        return total

    def get_skill_level(self, skill_id: str) -> int:
        """Get current level of a skill"""
        return self.skills.get(skill_id, 0)

    def get_skill_bonus(self, skill_id: str, bonus_type: str) -> float:
        """Calculate bonus from skill level"""
        if skill_id not in SKILLS:
            return 0.0

        skill_level = self.get_skill_level(skill_id)
        skill_data = SKILLS[skill_id]
        bonus_per_level = skill_data.get("bonus_per_level", {})

        if bonus_type in bonus_per_level:
            return skill_level * bonus_per_level[bonus_type]
        return 0.0

    def get_max_training_slots(self) -> int:
        """Get the maximum number of skills that can be trained simultaneously"""
        base_slots = 1
        multi_tasking_level = self.get_skill_level("multi_tasking")
        return base_slots + multi_tasking_level

    def start_skill_training(self, skill_id: str) -> tuple[bool, str]:
        """Start training a skill"""
        if skill_id not in SKILLS:
            return False, "Invalid skill"

        # Check if skill is already training
        for training in self.skill_training:
            if training["skill_id"] == skill_id:
                return False, f"{SKILLS[skill_id]['name']} is already training"

        # Check if we have available training slots
        max_slots = self.get_max_training_slots()
        if len(self.skill_training) >= max_slots:
            if max_slots == 1:
                return False, f"Already training {SKILLS[self.skill_training[0]['skill_id']]['name']}. Train Multi-Tasking skill to train multiple skills at once."
            else:
                return False, f"All {max_slots} training slots are full. Wait for a skill to complete first."

        skill_data = SKILLS[skill_id]
        current_level = self.get_skill_level(skill_id)

        if current_level >= skill_data["max_level"]:
            return False, "Skill already at maximum level"

        # Calculate training time
        next_level = current_level + 1
        training_time = BASE_SKILL_TRAIN_TIME * (SKILL_TIME_MULTIPLIER ** current_level)

        self.skill_training.append({
            "skill_id": skill_id,
            "start_time": time.time(),
            "duration": training_time,
            "target_level": next_level
        })

        return True, f"Started training {skill_data['name']} to level {next_level}"

    def check_skill_training(self) -> List[str]:
        """Check if any skill training is complete. Returns list of completion messages."""
        if not self.skill_training:
            return []

        completed_messages = []
        remaining_training = []

        for training in self.skill_training:
            elapsed = time.time() - training["start_time"]

            if elapsed >= training["duration"]:
                skill_id = training["skill_id"]
                target_level = training["target_level"]

                self.skills[skill_id] = target_level
                skill_name = SKILLS[skill_id]["name"]

                # Award XP for completing training (scales with level)
                xp_reward = 50 * target_level
                self.add_experience(xp_reward)

                completed_messages.append(f"{skill_name} trained to level {target_level}! (+{xp_reward} XP)")
            else:
                remaining_training.append(training)

        self.skill_training = remaining_training
        return completed_messages

    def get_training_progress(self, skill_id: Optional[str] = None) -> Optional[Dict | List[Dict]]:
        """Get current training progress. If skill_id provided, returns progress for that skill, otherwise returns all."""
        if not self.skill_training:
            return None

        if skill_id:
            # Return progress for specific skill
            for training in self.skill_training:
                if training["skill_id"] == skill_id:
                    elapsed = time.time() - training["start_time"]
                    progress = (elapsed / training["duration"]) * 100
                    remaining = training["duration"] - elapsed

                    skill_data = SKILLS[training["skill_id"]]

                    return {
                        "skill_name": skill_data["name"],
                        "target_level": training["target_level"],
                        "progress": min(progress, 100),
                        "remaining_seconds": max(remaining, 0)
                    }
            return None
        else:
            # Return progress for all training skills
            all_progress = []
            for training in self.skill_training:
                elapsed = time.time() - training["start_time"]
                progress = (elapsed / training["duration"]) * 100
                remaining = training["duration"] - elapsed

                skill_data = SKILLS[training["skill_id"]]

                all_progress.append({
                    "skill_id": training["skill_id"],
                    "skill_name": skill_data["name"],
                    "target_level": training["target_level"],
                    "progress": min(progress, 100),
                    "remaining_seconds": max(remaining, 0)
                })
            return all_progress if all_progress else None

    def modify_faction_standing(self, faction_id: str, change: float):
        """Modify standing with a faction"""
        if faction_id in self.faction_standings:
            self.faction_standings[faction_id] = max(-1.0, min(1.0,
                self.faction_standings[faction_id] + change))

    def get_faction_status(self, faction_id: str) -> str:
        """Get relationship status with faction"""
        standing = self.faction_standings.get(faction_id, 0.0)

        if standing >= 0.75:
            return "Excellent"
        elif standing >= 0.5:
            return "Good"
        elif standing >= 0.25:
            return "Friendly"
        elif standing >= -0.25:
            return "Neutral"
        elif standing >= -0.5:
            return "Unfriendly"
        elif standing >= -0.75:
            return "Hostile"
        else:
            return "At War"

    def add_experience(self, amount: int):
        """Add experience and check for level up"""
        self.experience += amount

        while self.experience >= self.experience_to_next:
            self.level_up()

    def level_up(self):
        """Level up the player"""
        self.level += 1
        self.experience -= self.experience_to_next
        # Experience required scales: 1000 * level * 1.5
        self.experience_to_next = int(1000 * self.level * 1.5)
        return True

    def get_level_progress(self) -> float:
        """Get progress to next level as percentage"""
        return (self.experience / self.experience_to_next) * 100

    def update_play_time(self):
        """Update total play time"""
        self.stats["time_played"] = time.time() - self.game_start_time

    def to_dict(self) -> Dict:
        """Convert player to dictionary for saving"""
        self.update_play_time()

        return {
            "name": self.name,
            "credits": self.credits,
            "location": self.location,
            "level": self.level,
            "experience": self.experience,
            "experience_to_next": self.experience_to_next,
            "skills": self.skills,
            "skill_training": self.skill_training,
            "ship_cargo": self.ship_cargo,
            "station_inventories": self.station_inventories,
            "inventory": self.ship_cargo,  # Backwards compatibility
            "stats": self.stats,
            "faction_standings": self.faction_standings,
            "game_start_time": self.game_start_time,
            "visited_locations": list(self.visited_locations)
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Player':
        """Create player from dictionary"""
        player = cls(data["name"], data["credits"])
        player.location = data["location"]
        player.level = data.get("level", 1)
        player.experience = data.get("experience", 0)
        player.experience_to_next = data.get("experience_to_next", 1000)

        # Load skills and add any new skills that didn't exist in old saves
        player.skills = data["skills"]
        for skill_id in SKILLS.keys():
            if skill_id not in player.skills:
                player.skills[skill_id] = 0

        # Handle backwards compatibility for skill_training (old format was dict, new is list)
        skill_training_data = data.get("skill_training")
        if skill_training_data is None:
            player.skill_training = []
        elif isinstance(skill_training_data, list):
            player.skill_training = skill_training_data
        elif isinstance(skill_training_data, dict):
            # Old format - convert to list
            player.skill_training = [skill_training_data]
        else:
            player.skill_training = []

        # Handle backwards compatibility - old saves have "inventory", new saves have "ship_cargo"
        if "ship_cargo" in data:
            player.ship_cargo = data["ship_cargo"]
            player.station_inventories = data.get("station_inventories", {})
        else:
            # Old save format - treat inventory as ship cargo
            player.ship_cargo = data.get("inventory", {})
            player.station_inventories = {}

        player.inventory = player.ship_cargo  # Keep reference for compatibility

        player.stats = data["stats"]
        player.faction_standings = data["faction_standings"]
        player.game_start_time = data.get("game_start_time", time.time())

        # Load visited locations (backwards compatibility)
        player.visited_locations = set(data.get("visited_locations", [player.location]))

        return player
