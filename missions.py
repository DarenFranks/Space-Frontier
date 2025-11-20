"""
Mission and Contract System
Handles procedural missions, objectives, and rewards
"""

import random
import time
from typing import Dict, List, Optional
from data import CONTRACT_TYPES, RESOURCES, LOCATIONS


class Contract:
    """Represents a mission contract"""

    def __init__(self, contract_type: str, location_id: str, difficulty: int = 1):
        self.contract_type = contract_type
        self.location_id = location_id
        self.difficulty = difficulty

        if contract_type not in CONTRACT_TYPES:
            raise ValueError(f"Invalid contract type: {contract_type}")

        template = CONTRACT_TYPES[contract_type]

        self.name = template["name"]
        self.description = template["description"]
        self.time_limit = template["time_limit"]

        # Generate rewards based on difficulty
        min_reward, max_reward = template["reward_range"]
        self.reward = random.randint(
            min_reward * difficulty,
            max_reward * difficulty
        )

        # Generate objectives based on type
        self.objectives = self._generate_objectives()
        
        # Override description for cargo transport to include details
        if contract_type == "cargo_transport":
            item_id = self.objectives["resource_id"]
            item_type = self.objectives.get("item_type", "resource")
            quantity = self.objectives["quantity"]
            dest_name = LOCATIONS[self.objectives["destination"]]["name"]
            
            if item_type == "commodity":
                from data import COMMODITIES
                item_name = COMMODITIES.get(item_id, {}).get("name", item_id)
            else:
                item_name = RESOURCES.get(item_id, {}).get("name", item_id)
            
            self.description = f"Transport {quantity}x {item_name} from {LOCATIONS[location_id]['name']} to {dest_name}"

        self.accepted_time: Optional[float] = None
        self.completed = False
        self.failed = False

        self.contract_id = f"{contract_type}_{location_id}_{int(time.time())}"

    def _generate_objectives(self) -> Dict:
        """Generate specific objectives based on contract type"""
        if self.contract_type == "mining_contract":
            # Pick random resources to mine
            resource_id = random.choice(list(RESOURCES.keys()))
            quantity = random.randint(50, 200) * self.difficulty

            return {
                "type": "collect_resource",
                "resource_id": resource_id,
                "target_quantity": quantity,
                "current_quantity": 0
            }

        elif self.contract_type == "combat_patrol":
            # Destroy enemies
            enemy_count = random.randint(2, 5) * self.difficulty

            return {
                "type": "destroy_enemies",
                "target_count": enemy_count,
                "current_count": 0,
                "location": self.location_id
            }

        elif self.contract_type == "cargo_transport":
            # Transport commodities to another location
            # 70% chance of commodity, 30% chance of resource
            if random.random() < 0.7:
                from data import COMMODITIES
                item_id = random.choice(list(COMMODITIES.keys()))
                # Get commodity data
                commodity_data = COMMODITIES[item_id]
                # Base quantity on value (cheaper = more, expensive = less)
                if commodity_data["base_price"] < 50:
                    base_qty = random.randint(50, 150)
                elif commodity_data["base_price"] < 200:
                    base_qty = random.randint(20, 80)
                elif commodity_data["base_price"] < 1000:
                    base_qty = random.randint(10, 40)
                else:
                    base_qty = random.randint(5, 20)
                quantity = base_qty * self.difficulty
                item_type = "commodity"
            else:
                # Use resources for transport
                item_id = random.choice(list(RESOURCES.keys()))
                quantity = random.randint(50, 200) * self.difficulty
                item_type = "resource"

            # Pick a different destination
            all_locations = list(LOCATIONS.keys())
            all_locations.remove(self.location_id)
            destination = random.choice(all_locations)

            return {
                "type": "transport_cargo",
                "resource_id": item_id,  # Can be resource or commodity
                "item_type": item_type,   # Track what type it is
                "quantity": quantity,
                "destination": destination,
                "cargo_delivered": False
            }

        elif self.contract_type == "reconnaissance":
            # Scan locations
            scan_count = random.randint(3, 6)

            return {
                "type": "scan_locations",
                "target_count": scan_count,
                "current_count": 0
            }

        elif self.contract_type == "research_data":
            # Collect data from anomalies
            data_count = random.randint(5, 10) * self.difficulty

            return {
                "type": "collect_data",
                "target_count": data_count,
                "current_count": 0
            }

        return {}

    def accept(self):
        """Accept the contract"""
        self.accepted_time = time.time()

    def is_expired(self) -> bool:
        """Check if contract has expired"""
        if not self.accepted_time:
            return False

        elapsed = time.time() - self.accepted_time
        return elapsed > self.time_limit

    def get_time_remaining(self) -> float:
        """Get remaining time in seconds"""
        if not self.accepted_time:
            return self.time_limit

        elapsed = time.time() - self.accepted_time
        return max(0, self.time_limit - elapsed)

    def update_progress(self, progress_data: Dict) -> bool:
        """
        Update contract progress.
        Returns True if contract is completed.
        """
        # Don't update progress if already completed
        if self.completed:
            return False
            
        obj_type = self.objectives["type"]

        if obj_type == "collect_resource":
            if progress_data.get("resource_id") == self.objectives["resource_id"]:
                self.objectives["current_quantity"] += progress_data.get("quantity", 0)

                if self.objectives["current_quantity"] >= self.objectives["target_quantity"]:
                    self.completed = True
                    return True

        elif obj_type == "destroy_enemies":
            self.objectives["current_count"] += progress_data.get("enemies_destroyed", 0)

            if self.objectives["current_count"] >= self.objectives["target_count"]:
                self.completed = True
                return True

        elif obj_type == "transport_cargo":
            if progress_data.get("delivered", False):
                self.objectives["cargo_delivered"] = True
                self.completed = True
                return True

        elif obj_type == "scan_locations":
            self.objectives["current_count"] += progress_data.get("locations_scanned", 0)

            if self.objectives["current_count"] >= self.objectives["target_count"]:
                self.completed = True
                return True

        elif obj_type == "collect_data":
            self.objectives["current_count"] += progress_data.get("data_collected", 0)

            if self.objectives["current_count"] >= self.objectives["target_count"]:
                self.completed = True
                return True

        return False

    def get_progress_text(self) -> str:
        """Get human-readable progress"""
        obj = self.objectives
        obj_type = obj["type"]

        if obj_type == "collect_resource":
            resource_name = RESOURCES[obj["resource_id"]]["name"]
            return f"Collect {obj['current_quantity']}/{obj['target_quantity']} {resource_name}"

        elif obj_type == "destroy_enemies":
            return f"Destroy {obj['current_count']}/{obj['target_count']} enemies"

        elif obj_type == "transport_cargo":
            # Handle both resources and commodities
            item_id = obj["resource_id"]
            item_type = obj.get("item_type", "resource")  # Default to resource for old saves
            
            if item_type == "commodity":
                from data import COMMODITIES
                item_name = COMMODITIES.get(item_id, {}).get("name", item_id)
            else:
                item_name = RESOURCES.get(item_id, {}).get("name", item_id)
            
            dest_name = LOCATIONS[obj["destination"]]["name"]
            status = "Delivered" if obj["cargo_delivered"] else "In Transit"
            return f"Transport {obj['quantity']}x {item_name} to {dest_name} ({status})"

        elif obj_type == "scan_locations":
            return f"Scan {obj['current_count']}/{obj['target_count']} locations"

        elif obj_type == "collect_data":
            return f"Collect {obj['current_count']}/{obj['target_count']} data samples"

        return "Unknown objective"

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "contract_id": self.contract_id,
            "contract_type": self.contract_type,
            "location_id": self.location_id,
            "difficulty": self.difficulty,
            "name": self.name,
            "description": self.description,
            "reward": self.reward,
            "time_limit": self.time_limit,
            "objectives": self.objectives,
            "accepted_time": self.accepted_time,
            "completed": self.completed,
            "failed": self.failed
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Contract':
        """Create from dictionary"""
        contract = cls(data["contract_type"], data["location_id"], data["difficulty"])
        contract.contract_id = data["contract_id"]
        contract.name = data["name"]
        contract.description = data["description"]
        contract.reward = data["reward"]
        contract.time_limit = data["time_limit"]
        contract.objectives = data["objectives"]
        contract.accepted_time = data.get("accepted_time")
        contract.completed = data.get("completed", False)
        contract.failed = data.get("failed", False)
        return contract


class ContractBoard:
    """Manages available contracts"""

    def __init__(self):
        # Store contracts per location: {location_id: [contracts]}
        self.available_contracts_by_location: Dict[str, List[Contract]] = {}
        self.active_contracts: List[Contract] = []
        self.last_refresh = time.time()
        self.refresh_interval = 1800  # 30 minutes

    def generate_contracts_all_locations(self, min_per_location: int = 1, max_per_location: int = 3):
        """Generate contracts for all locations with contract services"""
        for location_id, location_data in LOCATIONS.items():
            if "contracts" in location_data.get("services", []):
                # Generate between min and max contracts per location
                count = random.randint(min_per_location, max_per_location)
                self.generate_contracts(location_id, count)

    def generate_contracts(self, location_id: str, count: int = 3):
        """Generate new contracts for a specific location"""
        location_data = LOCATIONS.get(location_id, {})

        if "contracts" not in location_data.get("services", []):
            return

        # Initialize location's contract list if needed
        if location_id not in self.available_contracts_by_location:
            self.available_contracts_by_location[location_id] = []

        # Generate contracts
        contracts = []
        for _ in range(count):
            contract_type = random.choice(list(CONTRACT_TYPES.keys()))
            difficulty = random.randint(1, 3)

            contract = Contract(contract_type, location_id, difficulty)
            contracts.append(contract)

        # Replace old contracts for this location
        self.available_contracts_by_location[location_id] = contracts

    def get_available_contracts(self, location_id: str) -> List[Contract]:
        """Get available contracts for a specific location"""
        # Generate contracts if this location has none
        if location_id not in self.available_contracts_by_location:
            location_data = LOCATIONS.get(location_id, {})
            if "contracts" in location_data.get("services", []):
                self.generate_contracts(location_id)
        
        return self.available_contracts_by_location.get(location_id, [])

    def accept_contract(self, contract_id: str, player=None) -> Optional[Contract]:
        """Move contract from available to active and place cargo items if transport contract"""
        # Search all locations for the contract
        for location_id, contracts in self.available_contracts_by_location.items():
            for contract in contracts:
                if contract.contract_id == contract_id:
                    contract.accept()
                    
                    # If it's a cargo transport contract, place items in station inventory
                    if contract.objectives.get("type") == "transport_cargo" and player:
                        item_id = contract.objectives.get("resource_id")
                        quantity = contract.objectives.get("quantity", 0)
                        location_id = contract.location_id
                        
                        # Add items to station inventory at contract location
                        if location_id not in player.station_inventories:
                            player.station_inventories[location_id] = {}
                        
                        if item_id not in player.station_inventories[location_id]:
                            player.station_inventories[location_id][item_id] = 0
                        
                        player.station_inventories[location_id][item_id] += quantity
                    
                    # Remove from available contracts for this location
                    contracts.remove(contract)
                    self.active_contracts.append(contract)
                    return contract
        return None

    def complete_contract(self, contract_id: str) -> Optional[int]:
        """Complete contract and get reward"""
        for contract in self.active_contracts:
            if contract.contract_id == contract_id and contract.completed:
                reward = contract.reward
                self.active_contracts.remove(contract)
                return reward
        return None

    def abandon_contract(self, contract_id: str) -> bool:
        """Abandon an active contract"""
        for contract in self.active_contracts:
            if contract.contract_id == contract_id:
                self.active_contracts.remove(contract)
                return True
        return False

    def complete_delivery_contract(self, contract_id: str, player) -> tuple[bool, str]:
        """
        Complete a delivery contract by depositing cargo at destination.
        Returns (success, message)
        """
        for contract in self.active_contracts:
            if contract.contract_id == contract_id:
                # Check if this is a delivery contract
                if contract.objectives.get("type") != "transport_cargo":
                    return False, "This is not a delivery contract"
                
                # Get contract details
                item_id = contract.objectives.get("resource_id")
                quantity = contract.objectives.get("quantity", 0)
                destination = contract.objectives.get("destination")
                
                # Check if player is at the destination
                if player.location != destination:
                    dest_name = LOCATIONS[destination]["name"]
                    return False, f"You must be at {dest_name} to complete this delivery"
                
                # Check if player has the items in ship cargo
                if player.ship_cargo.get(item_id, 0) < quantity:
                    return False, f"You don't have enough {item_id} in your cargo"
                
                # Remove items from ship cargo
                player.ship_cargo[item_id] -= quantity
                if player.ship_cargo[item_id] == 0:
                    del player.ship_cargo[item_id]
                
                # Add items to destination station inventory
                if destination not in player.station_inventories:
                    player.station_inventories[destination] = {}
                
                if item_id not in player.station_inventories[destination]:
                    player.station_inventories[destination][item_id] = 0
                
                player.station_inventories[destination][item_id] += quantity
                
                # Mark contract as complete
                contract.completed = True
                return True, f"Delivery complete! {quantity}x {item_id} deposited at {LOCATIONS[destination]['name']}"
        
        return False, "Contract not found"

    def check_expired_contracts(self):
        """Mark expired contracts as failed"""
        for contract in self.active_contracts:
            if contract.is_expired() and not contract.completed:
                contract.failed = True

    def get_active_contracts(self) -> List[Contract]:
        """Get all active contracts (excludes failed and completed)"""
        self.check_expired_contracts()
        return [c for c in self.active_contracts if not c.failed and not c.completed]

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        # Convert available_contracts_by_location to serializable format
        available_by_loc = {}
        for location_id, contracts in self.available_contracts_by_location.items():
            available_by_loc[location_id] = [c.to_dict() for c in contracts]
        
        return {
            "available_contracts_by_location": available_by_loc,
            "active_contracts": [c.to_dict() for c in self.active_contracts],
            "last_refresh": self.last_refresh
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'ContractBoard':
        """Create from dictionary"""
        board = cls()
        
        # Load available contracts by location
        available_by_loc = data.get("available_contracts_by_location", {})
        for location_id, contracts_data in available_by_loc.items():
            board.available_contracts_by_location[location_id] = [
                Contract.from_dict(c) for c in contracts_data
            ]
        
        # Handle old save format (legacy compatibility)
        if "available_contracts" in data and not available_by_loc:
            # Old format had a single list - put them all in a generic location
            old_contracts = [Contract.from_dict(c) for c in data["available_contracts"]]
            if old_contracts:
                # Group by location_id
                for contract in old_contracts:
                    loc_id = contract.location_id
                    if loc_id not in board.available_contracts_by_location:
                        board.available_contracts_by_location[loc_id] = []
                    board.available_contracts_by_location[loc_id].append(contract)
        
        board.active_contracts = [Contract.from_dict(c) for c in data.get("active_contracts", [])]
        board.last_refresh = data.get("last_refresh", time.time())
        return board
