"""
Core Game Engine
Main game state and logic management
"""

import time
import random
from typing import Dict, Optional, Tuple, List
from player import Player
from vessels import Vessel
from economy import EconomyManager, ModuleMarket, ComponentMarket, ShipMarket
from combat import CombatEncounter, create_enemy_vessel
from missions import ContractBoard
from factions import FactionManager
from shipyard import Shipyard
from manufacturing import ManufacturingManager
from recycling import RecyclingSystem
from berth_system import BerthManager
from commodity_market import CommodityMarket
from save_system import save_game, load_game
from data import LOCATIONS, RESOURCES, MODULES, RAW_RESOURCES, REFINING_YIELD_RANGES, VESSEL_CLASSES, COMMODITIES
from travel_system import get_travel_distance, calculate_travel_time
from config import STARTING_CREDITS, STARTING_LOCATION, STARTING_VESSEL


class GameEngine:
    """Main game engine managing all systems"""

    def __init__(self):
        self.player: Optional[Player] = None
        self.vessel: Optional[Vessel] = None
        self.economy: EconomyManager = EconomyManager()
        self.contract_board: ContractBoard = ContractBoard()
        self.faction_manager: FactionManager = FactionManager()
        self.shipyard: Shipyard = Shipyard()
        self.berth_manager: BerthManager = BerthManager()
        self.module_market: ModuleMarket = ModuleMarket()
        self.component_market: ComponentMarket = ComponentMarket()
        self.ship_market: ShipMarket = ShipMarket()
        self.manufacturing: ManufacturingManager = ManufacturingManager()
        self.recycling: RecyclingSystem = RecyclingSystem()
        self.commodity_market: CommodityMarket = CommodityMarket()

        self.current_combat: Optional[CombatEncounter] = None
        self.current_trader: Optional[Dict] = None  # Current trader encounter
        self.pending_travel_destination: Optional[str] = None  # Destination when trader encountered during travel
        self.game_time = 0  # In-game time elapsed
        self.last_update = time.time()
        self.mining_attempts = 0  # Track mining attempts for encounters

    def new_game(self, player_name: str):
        """Start a new game"""
        self.player = Player(player_name, STARTING_CREDITS)
        self.player.location = STARTING_LOCATION

        # Give player starting vessel
        self.vessel = Vessel(STARTING_VESSEL)

        # Equip basic starting modules
        self.vessel.install_module("pulse_cannon_t1")
        self.vessel.install_module("aegis_shield_t1")
        self.vessel.install_module("quantum_scanner_t1")
        self.vessel.install_module("harvester_drill_t1")  # Basic mining capability
        self.vessel.install_module("basic_thruster_t1")  # Basic engine

        # Set shields to full capacity after installing modules
        self.vessel.current_shields = self.vessel.get_total_shield_capacity()

        # Initialize systems
        self.economy = EconomyManager()
        self.contract_board = ContractBoard()
        self.faction_manager = FactionManager()
        self.berth_manager = BerthManager()
        self.commodity_market = CommodityMarket()

        # Initialize ship market inventories
        self.ship_market.initialize_all_stations(LOCATIONS)

        # Initialize shipyards at all locations with shipyard service
        for location_id, location_data in LOCATIONS.items():
            if "shipyard" in location_data.get("services", []):
                # Determine location type for berth pricing
                location_type = "major_station" if location_id == STARTING_LOCATION else "standard_station"
                # Start with 1 berth at starting location, 0 elsewhere
                starting_berths = 1 if location_id == STARTING_LOCATION else 0
                self.berth_manager.initialize_shipyard(location_id, location_type, starting_berths)

        # Store starting ship in berth
        self.player.current_ship_id = STARTING_VESSEL
        self.berth_manager.store_ship(STARTING_LOCATION, STARTING_VESSEL)

        # Generate initial contracts for all locations with at least 1 per location
        self.contract_board.generate_contracts_all_locations(min_per_location=1, max_per_location=3)

        print(f"\n=== Welcome to Void Dominion, Commander {player_name}! ===")
        print(f"You begin your journey in {LOCATIONS[self.player.location]['name']}")
        print(f"Credits: {self.player.credits:,}")
        print(f"Vessel: {self.vessel.name}")
        print("\nType 'help' for a list of commands.\n")

    def update_game_state(self):
        """Update game state - called periodically"""
        current_time = time.time()
        delta = current_time - self.last_update
        self.last_update = current_time

        # Update game time (faster than real time)
        self.game_time += delta * 10  # 10x speed

        # Check skill training
        if self.player:
            training_complete = self.player.check_skill_training()
            for msg in training_complete:
                print(f"\n>>> {msg}")

        # Check manufacturing completion
        manufacturing_messages = self.check_manufacturing()
        for msg in manufacturing_messages:
            print(f"\n>>> {msg}")

        # Update markets periodically
        if int(self.game_time) % 600 == 0:  # Every 10 minutes game time
            self.economy.update_markets()
            self.commodity_market.update_markets(delta * 10)  # Update commodity prices

        # Update faction conflicts
        if int(self.game_time) % 300 == 0:  # Every 5 minutes
            self.faction_manager.update_conflicts()

        # Check contract expiry
        self.contract_board.check_expired_contracts()

        # Check for completed contracts and auto-pay
        completed_contracts = self.check_completed_contracts()
        for msg in completed_contracts:
            print(f"\n>>> {msg}")

    def check_completed_contracts(self) -> List[str]:
        """Check for completed contracts and automatically pay out rewards"""
        messages = []
        contracts_to_remove = []

        for contract in self.contract_board.active_contracts:
            if contract.completed and not contract.failed:
                # Award credits
                self.player.add_credits(contract.reward)

                # Award XP (contract reward / 10)
                xp_reward = int(contract.reward / 10)
                self.player.add_experience(xp_reward)

                # Update stats
                self.player.stats['contracts_completed'] += 1

                # Create completion message
                message = f"CONTRACT COMPLETE: {contract.name} | Reward: {contract.reward:,} CR + {xp_reward} XP"
                messages.append(message)

                # Mark for removal
                contracts_to_remove.append(contract)

        # Remove completed contracts
        for contract in contracts_to_remove:
            self.contract_board.active_contracts.remove(contract)

        return messages

    def travel_to_location(self, destination_id: str) -> tuple:
        """Initiate travel to a new location - returns (success, message, travel_info)"""
        if destination_id not in LOCATIONS:
            return False, "Invalid location", None

        if destination_id == self.player.location:
            return False, "You are already at this location", None

        current_loc = LOCATIONS[self.player.location]
        connections = current_loc.get("connections", [])

        if destination_id not in connections:
            return False, "Cannot travel directly to this location", None

        # Check faction access
        access_info = self.faction_manager.get_player_access(
            destination_id, self.player.faction_standings
        )

        if access_info["access"] == "forbidden":
            return False, f"Access denied - {access_info['controlling_faction']} considers you hostile", None

        # Calculate travel distance and time
        distance = get_travel_distance(self.player.location, destination_id)
        travel_time = calculate_travel_time(distance, self.vessel.get_effective_speed())
        
        # Prepare travel info for GUI animation
        travel_info = {
            "origin": self.player.location,
            "origin_name": LOCATIONS[self.player.location]["name"],
            "destination": destination_id,
            "destination_name": LOCATIONS[destination_id]["name"],
            "distance": distance,
            "travel_time": travel_time,
            "danger_level": LOCATIONS[destination_id].get("danger_level", 0)
        }
        
        return True, "Travel initiated", travel_info
    
    def complete_travel(self, destination_id: str) -> tuple[bool, str]:
        """Complete travel to destination (called after animation)"""
        if destination_id not in LOCATIONS:
            return False, "Invalid location"
        
        current_loc_id = self.player.location
        current_loc = LOCATIONS[current_loc_id]
        
        # Random encounter chance during travel
        danger_level = LOCATIONS[destination_id].get("danger_level", 0)
        encounter_chance = danger_level * 0.345  # Up to 34.5% in dangerous areas

        if random.random() < encounter_chance:
            # Start combat encounter (enemies scale with player level)
            difficulty = "easy" if danger_level < 0.4 else "normal" if danger_level < 0.7 else "hard"
            enemy_vessel, enemy_name = create_enemy_vessel(difficulty, self.player.level)
            self.current_combat = CombatEncounter(self.vessel, enemy_vessel, enemy_name, self.player.level)
            # Update location before combat
            self.player.location = destination_id
            return True, f"Ambushed by {enemy_name} on arrival! Combat initiated."

        # Trader encounter chance (only when traveling between stations, not to asteroids)
        current_type = current_loc.get("type", "")
        destination_type = LOCATIONS[destination_id].get("type", "")

        if current_type == "station" and destination_type == "station":
            # 20% chance of trader encounter
            trader_chance = 0.20
            if random.random() < trader_chance:
                self.current_trader = self._generate_trader_encounter()
                # Store destination to complete travel after trader encounter
                self.pending_travel_destination = destination_id
                # Update location
                self.player.location = destination_id
                return True, "Encountered a wandering trader on arrival!"

        # Successful travel
        distance_traveled = get_travel_distance(current_loc_id, destination_id)
        self.player.location = destination_id
        self.player.stats["distance_traveled"] += distance_traveled

        # Track visited location for fog of war
        self.player.visited_locations.add(destination_id)

        # Generate new contracts at destination
        self.contract_board.generate_contracts(destination_id)

        dest_name = LOCATIONS[destination_id]["name"]
        return True, f"Traveled to {dest_name}"

    def handle_ship_destruction(self) -> Tuple[bool, str]:
        """
        Handle player ship destruction - respawn at closest station
        Lose all cargo, but station storage is safe
        """
        # Find closest safe location (station/planet)
        safe_locations = [
            'nexus_prime', 'forge_station', 'meridian_gates', 'corsair_haven',
            'titan_alpha', 'synthesis_planet', 'ironhold_world', 'neural_network',
            'axiom_labs', 'ironhold_sectors'
        ]

        # Simple BFS to find closest station
        from collections import deque

        current_loc = self.player.location
        visited = set()
        queue = deque([(current_loc, 0)])
        closest_station = 'nexus_prime'  # Default fallback
        min_distance = float('inf')

        while queue:
            loc, dist = queue.popleft()

            if loc in visited:
                continue
            visited.add(loc)

            # Check if this is a safe location
            if loc in safe_locations:
                if dist < min_distance:
                    min_distance = dist
                    closest_station = loc

            # Add connected locations
            if loc in LOCATIONS:
                for conn in LOCATIONS[loc].get('connections', []):
                    if conn not in visited:
                        queue.append((conn, dist + 1))

        # Clear ship cargo (lost in destruction)
        cargo_lost = list(self.player.inventory.keys())
        self.player.inventory.clear()

        # Check if player has ships in station storage at closest station
        station_inventory = self.player.get_station_inventory(closest_station)
        available_ships = []

        from data import VESSEL_CLASSES
        for item_id, quantity in station_inventory.items():
            if item_id in VESSEL_CLASSES and quantity > 0:
                available_ships.append(item_id)

        # If player has ships at station, use one of them
        if available_ships:
            # Use the first available ship
            ship_id = available_ships[0]
            station_inventory[ship_id] -= 1
            if station_inventory[ship_id] == 0:
                del station_inventory[ship_id]

            # Create new vessel
            self.vessel = Vessel(ship_id)
            message = f"Ship destroyed! Respawned at {LOCATIONS[closest_station]['name']} with {VESSEL_CLASSES[ship_id]['name']} from storage."
        else:
            # No ships available - give starter ship
            self.vessel = Vessel(STARTING_VESSEL)

            # Equip basic modules
            self.vessel.install_module("pulse_cannon_t1")
            self.vessel.install_module("aegis_shield_t1")
            self.vessel.install_module("quantum_scanner_t1")
            self.vessel.install_module("harvester_drill_t1")

            message = f"Ship destroyed! Respawned at {LOCATIONS[closest_station]['name']} with emergency rescue pod (Basic Scout)."

        # Move player to closest station
        self.player.location = closest_station
        self.player.visited_locations.add(closest_station)

        # End combat
        self.current_combat = None

        # Add info about cargo loss
        if cargo_lost:
            message += f"\n\nCargo lost: {len(cargo_lost)} item types destroyed."

        message += "\n\nStation storage remains safe."

        return True, message

    def mine_resources(self) -> tuple[bool, str]:
        """Mine resources at current location"""
        location_data = LOCATIONS[self.player.location]
        available_resources = location_data.get("resources", [])

        if not available_resources:
            return False, "No resources available at this location"

        # Check if player has mining equipment
        mining_efficiency = self.vessel.get_mining_efficiency()

        if mining_efficiency <= 1.0:
            return False, "No mining equipment installed"

        # Get mining laser tier
        mining_tier = self.vessel.get_mining_tier()

        if mining_tier == 0:
            return False, "No mining laser installed"

        # Filter resources that can be mined with current laser tier
        mineable_resources = []
        for resource_id in available_resources:
            resource_data = RESOURCES.get(resource_id, {})
            ore_tier = resource_data.get("mining_tier", 1)  # Default to tier 1 if not specified
            if mining_tier >= ore_tier:
                mineable_resources.append(resource_id)

        if not mineable_resources:
            return False, f"Your mining laser (Tier {mining_tier}) cannot mine any ores here. Higher tier ores require better mining equipment."

        # Pick random resource from mineable ones
        resource_id = random.choice(mineable_resources)
        resource_data = RESOURCES[resource_id]

        # Calculate yield
        base_yield = random.randint(10, 30)
        skill_bonus = self.player.get_skill_bonus("mining_operations", "mining_yield")
        total_yield = int(base_yield * mining_efficiency * (1 + skill_bonus))

        # Check how much can fit in cargo
        from volume_system import get_max_quantity_can_add
        cargo_capacity = self.vessel.cargo_capacity
        max_can_add = get_max_quantity_can_add(self.player.inventory, cargo_capacity, resource_id)

        if max_can_add <= 0:
            current_volume = self.player.get_cargo_volume()
            return False, f"Cargo hold full! ({current_volume:.1f}/{cargo_capacity} used)"

        # Limit yield to what fits in cargo
        actual_yield = min(total_yield, max_can_add)

        # Add to inventory
        success, message = self.player.add_item(resource_id, actual_yield, cargo_capacity)
        if not success:
            return False, message

        self.player.stats["resources_mined"] += actual_yield

        # Update contract progress and check for completion
        contract_completed_msg = ""
        for contract in self.contract_board.active_contracts:
            if contract.objectives.get("type") == "collect_resource":
                completed = contract.update_progress({"resource_id": resource_id, "quantity": actual_yield})
                if completed:
                    # Auto-pay immediately
                    self.player.add_credits(contract.reward)
                    xp_reward = int(contract.reward / 10)
                    self.player.add_experience(xp_reward)
                    self.player.stats['contracts_completed'] += 1
                    contract_completed_msg = f"\n\n✅ CONTRACT COMPLETE: {contract.name}\nReward: {contract.reward:,} CR + {xp_reward} XP"

        # Inform if cargo limited the yield
        cargo_msg = f" (limited by cargo space)" if actual_yield < total_yield else ""

        # Track mining attempts and check for encounters
        self.mining_attempts += 1
        encounter_msg = ""

        if self.mining_attempts >= 5:
            # Every 5 mining attempts, chance for encounter
            self.mining_attempts = 0  # Reset counter
            encounter_roll = random.random()

            if encounter_roll < 0.46:  # 46% chance of pirate encounter (increased by 15%)
                from combat import create_enemy_vessel
                difficulty = "normal"
                enemy_vessel, enemy_name = create_enemy_vessel(difficulty, self.player.level)
                self.current_combat = CombatEncounter(self.vessel, enemy_vessel, enemy_name, self.player.level)
                encounter_msg = f"\n\n⚠️ PIRATE AMBUSH! {enemy_name} detected! Combat initiated."
            elif encounter_roll < 0.7475:  # 28.75% chance of trader encounter (increased by 15%)
                self.current_trader = self._generate_trader_encounter()
                encounter_msg = f"\n\n📡 TRADER DETECTED! A wandering trader has appeared."

        return True, f"Mined {actual_yield}x {resource_data['name']}{cargo_msg}{contract_completed_msg}{encounter_msg}"

    def _generate_trader_encounter(self) -> Dict:
        """Generate a random trader with inventory and credits"""
        from combat import create_enemy_vessel

        # Traders use lighter ships (scouts/haulers)
        trader_ships = ["scout_standard_mk1", "scout_standard_mk2", "hauler_standard_mk1"]
        trader_ship = random.choice(trader_ships)

        trader_names = [
            "Wandering Merchant", "Star Trader", "Nomadic Vendor", "Void Merchant",
            "Freelance Trader", "Independent Dealer", "Cosmic Peddler", "Space Caravan"
        ]

        trader_vessel = Vessel(trader_ship)
        # Traders have minimal weapons for self-defense
        if trader_vessel.module_slots["weapon"] > 0:
            trader_vessel.install_module("pulse_cannon_t1")
        if trader_vessel.module_slots["defense"] > 0:
            trader_vessel.install_module("aegis_shield_t1")

        # Generate trader inventory
        inventory = {}
        credits = random.randint(10000 + (self.player.level * 2000), 30000 + (self.player.level * 5000))

        # Commodities (always have some)
        num_commodities = random.randint(2, 4)
        for _ in range(num_commodities):
            commodity_id = random.choice(list(COMMODITIES.keys()))
            quantity = random.randint(10, 50)
            inventory[commodity_id] = inventory.get(commodity_id, 0) + quantity

        # Resources (60% chance)
        if random.random() < 0.6:
            num_resources = random.randint(1, 3)
            for _ in range(num_resources):
                resource_id = random.choice(list(RESOURCES.keys()))
                quantity = random.randint(5, 30)
                inventory[resource_id] = inventory.get(resource_id, 0) + quantity

        # Modules (30% chance)
        if random.random() < 0.3:
            tier = "t1" if self.player.level < 10 else "t2"
            available_modules = [m_id for m_id in MODULES.keys() if tier in m_id]
            if available_modules:
                module_id = random.choice(available_modules)
                inventory[module_id] = 1

        return {
            "name": random.choice(trader_names),
            "vessel": trader_vessel,
            "inventory": inventory,
            "credits": credits
        }

    def trade_with_trader(self, item_id: str, quantity: int, is_buying: bool) -> Tuple[bool, str]:
        """Trade with the current trader"""
        if not self.current_trader:
            return False, "No trader present"

        trader = self.current_trader
        item_name = self._get_item_name(item_id)

        if is_buying:
            # Player buying from trader
            if item_id not in trader["inventory"] or trader["inventory"][item_id] < quantity:
                return False, f"Trader doesn't have enough {item_name}"

            # Calculate price (slightly higher than market)
            base_price = self._get_item_base_price(item_id)
            total_cost = int(base_price * quantity * 1.2)  # 20% markup

            if self.player.credits < total_cost:
                return False, f"Insufficient credits. Need {total_cost:,} CR"

            # Execute trade
            self.player.spend_credits(total_cost)
            success, msg = self.player.add_item(item_id, quantity, self.vessel.cargo_capacity)
            if not success:
                self.player.add_credits(total_cost)  # Refund
                return False, msg

            trader["inventory"][item_id] -= quantity
            if trader["inventory"][item_id] == 0:
                del trader["inventory"][item_id]
            trader["credits"] += total_cost

            return True, f"Bought {quantity}x {item_name} for {total_cost:,} CR"
        else:
            # Player selling to trader
            if not self.player.has_item(item_id, quantity):
                return False, f"You don't have enough {item_name}"

            # Calculate price (slightly lower than market)
            base_price = self._get_item_base_price(item_id)
            total_payment = int(base_price * quantity * 0.8)  # 20% markdown

            if trader["credits"] < total_payment:
                return False, "Trader doesn't have enough credits"

            # Execute trade
            self.player.remove_item(item_id, quantity)
            self.player.add_credits(total_payment)
            trader["inventory"][item_id] = trader["inventory"].get(item_id, 0) + quantity
            trader["credits"] -= total_payment

            return True, f"Sold {quantity}x {item_name} for {total_payment:,} CR"

    def attack_trader(self) -> Tuple[bool, str]:
        """Attack the current trader and initiate combat"""
        if not self.current_trader:
            return False, "No trader to attack"

        trader = self.current_trader
        self.current_combat = CombatEncounter(
            self.vessel,
            trader["vessel"],
            trader["name"],
            self.player.level
        )

        # Override combat rewards with trader's actual inventory
        self.current_combat.rewards = {
            "credits": trader["credits"],
            "xp": 50,  # Small XP for attacking traders
            "loot": trader["inventory"].copy()
        }

        # Clear trader (combat takes over)
        trader_name = trader["name"]
        self.current_trader = None

        return True, f"Attacking {trader_name}! Combat initiated."

    def dismiss_trader(self) -> tuple[bool, str]:
        """Dismiss the current trader and complete any pending travel"""
        self.current_trader = None

        # Complete pending travel if trader was encountered during travel
        if self.pending_travel_destination:
            destination_id = self.pending_travel_destination
            self.pending_travel_destination = None

            # Complete the travel
            self.player.location = destination_id
            self.player.stats["distance_traveled"] += 100

            # Track visited location for fog of war
            self.player.visited_locations.add(destination_id)

            # Generate new contracts at destination
            self.contract_board.generate_contracts(destination_id)

            dest_name = LOCATIONS[destination_id]["name"]
            return True, f"Traveled to {dest_name}"

        return True, "Trader dismissed"

    def _get_item_name(self, item_id: str) -> str:
        """Get display name for any item"""
        if item_id in RESOURCES:
            return RESOURCES[item_id]["name"]
        elif item_id in COMMODITIES:
            return COMMODITIES[item_id]["name"]
        elif item_id in MODULES:
            return MODULES[item_id]["name"]
        return item_id

    def _get_item_base_price(self, item_id: str) -> int:
        """Get base price for any item"""
        if item_id in RESOURCES:
            return RESOURCES[item_id]["base_price"]
        elif item_id in COMMODITIES:
            return COMMODITIES[item_id]["base_price"]
        elif item_id in MODULES:
            return MODULES[item_id].get("cost", 1000)
        return 100

    def refine_ore(self, raw_ore_id: str, quantity: int) -> tuple[bool, str]:
        """
        Refine raw ore into refined resources
        Yield is RNG-based depending on ore rarity (50-95%)
        Refined ore goes back to the same location as the source (ship or station)
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

        # Check if player has the raw ore (from ship or station)
        accessible_quantities = self.player.get_total_accessible_quantity(raw_ore_id)
        if accessible_quantities["total"] < quantity:
            ship_qty = accessible_quantities["ship"]
            station_qty = accessible_quantities["station"]
            total_qty = accessible_quantities["total"]
            return False, f"Insufficient raw ore. You have {total_qty}x {raw_ore_data['name']} (Ship: {ship_qty}, Station: {station_qty})"

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
        total_refined = max(1, int(quantity * yield_percent))

        # Determine how much raw ore comes from ship vs station
        ship_raw_qty = min(quantity, accessible_quantities["ship"])
        station_raw_qty = quantity - ship_raw_qty

        # Split refined ore proportionally based on source
        if ship_raw_qty > 0 and station_raw_qty > 0:
            # Split proportionally
            ship_refined = max(1, int(total_refined * (ship_raw_qty / quantity)))
            station_refined = total_refined - ship_refined
        elif ship_raw_qty > 0:
            # All from ship
            ship_refined = total_refined
            station_refined = 0
        else:
            # All from station
            ship_refined = 0
            station_refined = total_refined

        # Check cargo capacity for ship portion only
        if ship_refined > 0:
            cargo_capacity = self.vessel.cargo_capacity
            current_volume = self.player.get_cargo_volume()

            ship_raw_volume = ship_raw_qty * raw_ore_data["volume"]
            ship_refined_volume = ship_refined * refined_data["volume"]
            net_volume_change = ship_refined_volume - ship_raw_volume
            final_volume = current_volume + net_volume_change

            if final_volume > cargo_capacity:
                space_needed = final_volume - cargo_capacity
                return False, f"Insufficient ship cargo space! Refining {ship_raw_qty}x {raw_ore_data['name']} → {ship_refined}x {refined_data['name']} would exceed capacity by {space_needed:.1f}. Current: {current_volume:.1f}/{cargo_capacity}"

        # Remove raw ore from ship
        if ship_raw_qty > 0:
            if not self.player.remove_item(raw_ore_id, ship_raw_qty):
                return False, "Failed to remove raw ore from ship"

        # Remove raw ore from station
        if station_raw_qty > 0:
            station_inv = self.player.get_station_inventory(self.player.location)
            if raw_ore_id not in station_inv or station_inv[raw_ore_id] < station_raw_qty:
                # Refund ship if we already removed from there
                if ship_raw_qty > 0:
                    self.player.add_item(raw_ore_id, ship_raw_qty)
                return False, "Failed to remove raw ore from station"
            station_inv[raw_ore_id] -= station_raw_qty
            if station_inv[raw_ore_id] == 0:
                del station_inv[raw_ore_id]

        # Add refined ore to ship
        if ship_refined > 0:
            cargo_capacity = self.vessel.cargo_capacity
            success, message = self.player.add_item(refined_id, ship_refined, cargo_capacity)
            if not success:
                # Refund raw ore
                if ship_raw_qty > 0:
                    self.player.add_item(raw_ore_id, ship_raw_qty)
                if station_raw_qty > 0:
                    station_inv = self.player.get_station_inventory(self.player.location)
                    station_inv[raw_ore_id] = station_inv.get(raw_ore_id, 0) + station_raw_qty
                return False, f"Failed to add refined resource to ship: {message}"

        # Add refined ore to station
        if station_refined > 0:
            station_inv = self.player.get_station_inventory(self.player.location)
            station_inv[refined_id] = station_inv.get(refined_id, 0) + station_refined

        # Update stats
        self.player.stats["resources_refined"] += total_refined

        # Award XP for refining
        xp_reward = total_refined // 10 + 1
        self.player.add_experience(xp_reward)

        # Create result message with detailed breakdown
        yield_pct = (total_refined / quantity) * 100
        result_parts = [f"Refined {quantity}x {raw_ore_data['name']} → {total_refined}x {refined_data['name']} ({yield_pct:.1f}% yield)"]

        if ship_refined > 0 and station_refined > 0:
            result_parts.append(f"Ship: {ship_raw_qty} raw → {ship_refined} refined")
            result_parts.append(f"Station: {station_raw_qty} raw → {station_refined} refined")
        elif ship_refined > 0:
            result_parts.append(f"(Ship cargo)")
        else:
            result_parts.append(f"(Station storage)")

        result_parts.append(f"+{xp_reward} XP")

        return True, "\n".join(result_parts)

    def repair_vessel(self, repair_hull: bool = True, repair_shields: bool = True) -> tuple[bool, str]:
        """
        Repair vessel hull and/or recharge shields at a station
        Cost is based on damage amount
        """
        location_data = LOCATIONS[self.player.location]

        # Check if at a station with shipyard or repair services
        if "shipyard" not in location_data.get("services", []):
            return False, "No shipyard available at this location"

        # Calculate damage
        hull_damage = self.vessel.max_hull_hp - self.vessel.current_hull_hp
        shield_damage = self.vessel.get_total_shield_capacity() - self.vessel.current_shields

        # Check if repairs needed
        if hull_damage <= 0 and shield_damage <= 0:
            return False, "Your vessel is already at full condition"

        # Calculate repair costs
        # Hull repair: 10 credits per HP
        # Shield recharge: 5 credits per point
        hull_repair_cost = int(hull_damage * 10) if repair_hull else 0
        shield_repair_cost = int(shield_damage * 5) if repair_shields else 0
        total_cost = hull_repair_cost + shield_repair_cost

        # Apply engineering skill discount
        skill_discount = self.player.get_skill_bonus("engineering", "repair_discount")
        if skill_discount > 0:
            total_cost = int(total_cost * (1 - skill_discount))

        # Check if player has enough credits
        if self.player.credits < total_cost:
            return False, f"Insufficient credits. Repair cost: {total_cost:,} CR (You have: {self.player.credits:,} CR)"

        # Perform repairs
        hull_repaired = hull_damage if repair_hull else 0
        shields_recharged = shield_damage if repair_shields else 0

        self.vessel.repair(hull_repaired, shields_recharged)
        self.player.spend_credits(total_cost)

        # Build result message
        message = f"Vessel repaired for {total_cost:,} CR\n"
        if repair_hull and hull_damage > 0:
            message += f"  Hull: +{hull_repaired:.0f} HP (now {self.vessel.current_hull_hp:.0f}/{self.vessel.max_hull_hp:.0f})\n"
        if repair_shields and shield_damage > 0:
            message += f"  Shields: +{shields_recharged:.0f} points (now {self.vessel.current_shields:.0f}/{self.vessel.get_total_shield_capacity():.0f})"

        return True, message.strip()

    def get_repair_cost(self) -> dict:
        """Calculate repair costs without performing the repair"""
        hull_damage = self.vessel.max_hull_hp - self.vessel.current_hull_hp
        shield_damage = self.vessel.get_total_shield_capacity() - self.vessel.current_shields

        hull_cost = int(hull_damage * 10)
        shield_cost = int(shield_damage * 5)
        total_cost = hull_cost + shield_cost

        # Apply skill discount
        skill_discount = self.player.get_skill_bonus("engineering", "repair_discount")
        if skill_discount > 0:
            total_cost = int(total_cost * (1 - skill_discount))
            hull_cost = int(hull_cost * (1 - skill_discount))
            shield_cost = int(shield_cost * (1 - skill_discount))

        return {
            "hull_damage": hull_damage,
            "shield_damage": shield_damage,
            "hull_cost": hull_cost,
            "shield_cost": shield_cost,
            "total_cost": total_cost,
            "can_afford": self.player.credits >= total_cost
        }

    def scan_area(self) -> tuple[bool, str]:
        """Scan current area"""
        scan_range = self.vessel.get_scan_range()
        skill_bonus = self.player.get_skill_bonus("scanning", "scan_range")
        effective_range = scan_range * (1 + skill_bonus)

        location_data = LOCATIONS[self.player.location]

        info = f"\n=== Scan Results ===\n"
        info += f"Location: {location_data['name']}\n"
        info += f"Description: {location_data['description']}\n"
        info += f"Danger Level: {int(location_data.get('danger_level', 0) * 100)}%\n"
        info += f"Scan Range: {effective_range:.0f} units\n\n"

        # Show available resources
        resources = location_data.get("resources", [])
        if resources:
            info += "Resources detected:\n"
            for res_id in resources:
                info += f"  - {RESOURCES[res_id]['name']}\n"

        # Show anomalies
        if location_data.get("anomalies"):
            info += "\n⚠️ ANOMALIES DETECTED - Use 'Scan Anomaly' to collect research data\n"

        # Show services
        services = location_data.get("services", [])
        if services:
            info += f"\nServices: {', '.join(services)}\n"

        # Show connections
        connections = location_data.get("connections", [])
        if connections:
            info += f"\nConnected locations:\n"
            for conn_id in connections:
                info += f"  - {LOCATIONS[conn_id]['name']}\n"

        # Update contract progress and check for completion
        completed_contracts = []
        for contract in self.contract_board.active_contracts:
            if contract.objectives.get("type") == "scan_locations":
                completed = contract.update_progress({"locations_scanned": 1})
                if completed:
                    # Auto-pay immediately
                    self.player.add_credits(contract.reward)
                    xp_reward = int(contract.reward / 10)
                    self.player.add_experience(xp_reward)
                    self.player.stats['contracts_completed'] += 1
                    info += f"\n\n✅ CONTRACT COMPLETE: {contract.name}\nReward: {contract.reward:,} CR + {xp_reward} XP"
                    completed_contracts.append(contract)
        
        # Remove completed contracts from active list
        for contract in completed_contracts:
            self.contract_board.active_contracts.remove(contract)

        return True, info

    def scan_anomaly(self) -> tuple[bool, str]:
        """Scan anomalies at current location for research data"""
        location_data = LOCATIONS[self.player.location]

        # Check if location has anomalies
        if not location_data.get("anomalies"):
            return False, "No anomalies detected at this location"

        # Check if player has scanning equipment
        scan_range = self.vessel.get_scan_range()
        if scan_range <= 1.0:
            return False, "Insufficient scanning equipment to analyze anomalies"

        # Generate data collection amount based on scan range and skills
        skill_bonus = self.player.get_skill_bonus("scanning", "scan_range")
        data_collected = random.randint(1, 3)  # Base 1-3 data samples

        # Bonus from better scanners
        if scan_range > 50:
            data_collected += 1

        info = f"Scanning anomalies at {location_data['name']}...\n\n"
        info += f"Collected {data_collected} data sample{'s' if data_collected != 1 else ''}"

        # Update contract progress and check for completion
        completed_contracts = []
        for contract in self.contract_board.active_contracts:
            if contract.objectives.get("type") == "collect_data":
                completed = contract.update_progress({"data_collected": data_collected})
                if completed:
                    # Auto-pay immediately
                    self.player.add_credits(contract.reward)
                    xp_reward = int(contract.reward / 10)
                    self.player.add_experience(xp_reward)
                    self.player.stats['contracts_completed'] += 1
                    info += f"\n\n✅ CONTRACT COMPLETE: {contract.name}\nReward: {contract.reward:,} CR + {xp_reward} XP"
                    completed_contracts.append(contract)
        
        # Remove completed contracts from active list
        for contract in completed_contracts:
            self.contract_board.active_contracts.remove(contract)

        return True, info

    def deliver_cargo(self) -> tuple[bool, str]:
        """Attempt to deliver cargo for active transport contracts"""
        location_data = LOCATIONS[self.player.location]
        deliveries_made = []

        # Check all active transport contracts
        for contract in self.contract_board.active_contracts:
            if contract.objectives.get("type") == "transport_cargo":
                # Check if we're at the destination
                if self.player.location == contract.objectives.get("destination"):
                    item_id = contract.objectives.get("resource_id")
                    item_type = contract.objectives.get("item_type", "resource")
                    required_qty = contract.objectives.get("quantity", 0)

                    # Check if player has the required cargo
                    current_qty = self.player.inventory.get(item_id, 0)

                    if current_qty >= required_qty:
                        # Remove cargo from inventory
                        self.player.inventory[item_id] -= required_qty
                        if self.player.inventory[item_id] == 0:
                            del self.player.inventory[item_id]

                        # Mark contract as delivered
                        completed = contract.update_progress({"delivered": True})

                        if completed:
                            # Auto-pay immediately
                            self.player.add_credits(contract.reward)
                            xp_reward = int(contract.reward / 10)
                            self.player.add_experience(xp_reward)
                            self.player.stats['contracts_completed'] += 1

                            # Get item name based on type
                            if item_type == "commodity":
                                from data import COMMODITIES
                                item_name = COMMODITIES.get(item_id, {}).get("name", item_id)
                            else:
                                item_name = RESOURCES.get(item_id, {}).get("name", item_id)

                            deliveries_made.append({
                                "contract_name": contract.name,
                                "item": item_name,
                                "quantity": required_qty,
                                "reward": contract.reward,
                                "xp": xp_reward
                            })

        if deliveries_made:
            info = f"Cargo delivered at {location_data['name']}!\n\n"
            for delivery in deliveries_made:
                info += f"✅ Delivered {delivery['quantity']}x {delivery['item']}\n"
                info += f"✅ CONTRACT COMPLETE: {delivery['contract_name']}\n"
                info += f"Reward: {delivery['reward']:,} CR + {delivery['xp']} XP\n\n"
            
            # Remove completed contracts from active list
            contracts_to_remove = [c for c in self.contract_board.active_contracts 
                                   if c.objectives.get("type") == "transport_cargo" 
                                   and c.completed]
            for contract in contracts_to_remove:
                self.contract_board.active_contracts.remove(contract)
            
            return True, info.strip()

        # Check if player is at any destination but missing cargo
        for contract in self.contract_board.active_contracts:
            if contract.objectives.get("type") == "transport_cargo":
                if self.player.location == contract.objectives.get("destination"):
                    item_id = contract.objectives.get("resource_id")
                    item_type = contract.objectives.get("item_type", "resource")
                    required_qty = contract.objectives.get("quantity", 0)
                    current_qty = self.player.inventory.get(item_id, 0)
                    
                    # Get item name based on type
                    if item_type == "commodity":
                        from data import COMMODITIES
                        item_name = COMMODITIES.get(item_id, {}).get("name", item_id)
                    else:
                        item_name = RESOURCES.get(item_id, {}).get("name", item_id)

                    return False, f"Missing cargo! Need {required_qty}x {item_name}, have {current_qty}x"

        return False, "No cargo delivery contracts for this location"

    def get_location_info(self) -> Dict:
        """Get current location information"""
        location_data = LOCATIONS[self.player.location]

        return {
            "name": location_data["name"],
            "description": location_data["description"],
            "faction": location_data.get("faction"),
            "services": location_data.get("services", []),
            "danger_level": location_data.get("danger_level", 0),
            "connections": [LOCATIONS[c]["name"] for c in location_data.get("connections", [])]
        }

    def save_current_game(self) -> bool:
        """Save current game state"""
        if not self.player or not self.vessel:
            return False

        game_state = {
            "player": self.player.to_dict(),
            "vessel": self.vessel.to_dict(),
            "economy": self.economy.to_dict(),
            "contract_board": self.contract_board.to_dict(),
            "faction_manager": self.faction_manager.to_dict(),
            "manufacturing": self.manufacturing.to_dict(),
            "berth_manager": self.berth_manager.to_dict(),
            "commodity_market": self.commodity_market.to_dict(),
            "ship_market": self.ship_market.to_dict(),
            "game_time": self.game_time
        }

        return save_game(game_state)

    def load_saved_game(self) -> bool:
        """Load game from save file"""
        game_state = load_game()

        if not game_state:
            return False

        try:
            self.player = Player.from_dict(game_state["player"])
            self.vessel = Vessel.from_dict(game_state["vessel"])
            self.economy = EconomyManager.from_dict(game_state["economy"])
            self.contract_board = ContractBoard.from_dict(game_state["contract_board"])
            self.faction_manager = FactionManager.from_dict(game_state["faction_manager"])
            self.game_time = game_state.get("game_time", 0)

            # Load manufacturing if present (backwards compatibility)
            if "manufacturing" in game_state:
                self.manufacturing = ManufacturingManager.from_dict(game_state["manufacturing"])
            else:
                self.manufacturing = ManufacturingManager()

            # Load berth manager if present (backwards compatibility)
            if "berth_manager" in game_state:
                self.berth_manager = BerthManager.from_dict(game_state["berth_manager"])
            else:
                self.berth_manager = BerthManager()
                # Initialize shipyards for old saves
                for location_id, location_data in LOCATIONS.items():
                    if "shipyard" in location_data.get("services", []):
                        location_type = "major_station" if location_id == STARTING_LOCATION else "standard_station"
                        # Give starting location and current location at least 1 berth
                        starting_berths = 1 if (location_id == STARTING_LOCATION or location_id == self.player.location) else 0
                        self.berth_manager.initialize_shipyard(location_id, location_type, starting_berths)

                # Store player's current vessel in berth at their current location (or starting location as fallback)
                # This ensures old saves have their ship properly registered
                current_ship_id = self.vessel.vessel_class_id
                storage_location = self.player.location if self.player.location in self.berth_manager.shipyards else STARTING_LOCATION

                if storage_location in self.berth_manager.shipyards:
                    self.berth_manager.store_ship(storage_location, current_ship_id)
                    print(f"  [Compatibility] Registered {self.vessel.name} in berth at {LOCATIONS[storage_location]['name']}")

            # Load commodity market if present (backwards compatibility)
            if "commodity_market" in game_state:
                self.commodity_market = CommodityMarket.from_dict(game_state["commodity_market"])
            else:
                self.commodity_market = CommodityMarket()

            # Load ship market if present (backwards compatibility)
            if "ship_market" in game_state:
                self.ship_market = ShipMarket.from_dict(game_state["ship_market"])
            else:
                self.ship_market = ShipMarket()

            print(f"\n=== Welcome back, Commander {self.player.name}! ===")
            print(f"Location: {LOCATIONS[self.player.location]['name']}")
            print(f"Credits: {self.player.credits:,}")
            print(f"Vessel: {self.vessel.name}\n")

            return True
        except Exception as e:
            print(f"Error loading game: {e}")
            return False

    # ==================== SHIPYARD METHODS ====================

    def purchase_ship(self, ship_id: str, trade_in: bool = False) -> Tuple[bool, str]:
        """Purchase a new ship at current location's shipyard"""
        location_data = LOCATIONS[self.player.location]

        if "shipyard" not in location_data.get("services", []):
            return False, "No shipyard at this location"

        # Check berth availability if not trading in
        if not trade_in and not self.berth_manager.has_empty_berth(self.player.location):
            return False, "NO_BERTH"  # Special flag for GUI to offer berth purchase

        current_ship_id = self.vessel.vessel_class_id

        # Execute purchase
        success, message, cost = self.shipyard.purchase_ship(
            ship_id,
            self.player.credits,
            self.player.level,
            current_ship_id,
            trade_in
        )

        if not success:
            return False, message

        # Deduct credits
        self.player.spend_credits(cost)

        if trade_in:
            # Remove old ship from berth and replace with new one
            self.berth_manager.remove_ship(self.player.location, current_ship_id)
            self.berth_manager.store_ship(self.player.location, ship_id)

            # Transfer modules from old ship
            old_modules = dict(self.vessel.installed_modules)

            # Create new ship
            self.vessel = Vessel(ship_id)
            self.player.current_ship_id = ship_id

            # Try to reinstall compatible modules
            reinstalled = []
            for mod_type, modules in old_modules.items():
                for module_id in modules:
                    if self.vessel.install_module(module_id):
                        reinstalled.append(module_id)
                    else:
                        # Add to player inventory if can't install
                        self.player.add_item(module_id, 1)

            # Set hull and shields to full after installing modules
            self.vessel.current_hull_hp = self.vessel.max_hull_hp
            self.vessel.current_shields = self.vessel.get_total_shield_capacity()

            return True, message + f" | Reinstalled {len(reinstalled)} modules"
        else:
            # Store new ship in berth (keeping current ship active)
            success, berth_msg = self.berth_manager.store_ship(self.player.location, ship_id)
            if not success:
                # Refund purchase if can't store (shouldn't happen due to check above)
                self.player.add_credits(cost)
                return False, f"Failed to store ship: {berth_msg}"

            return True, message + f" | Ship stored in berth at this location"

    def purchase_berth(self) -> Tuple[bool, str, int]:
        """Purchase a new berth at current location
        Returns: (success, message, cost)
        """
        if self.player.location not in self.berth_manager.shipyards:
            return False, "No shipyard at this location", 0

        success, message, cost = self.berth_manager.purchase_berth(
            self.player.location,
            self.player.credits
        )

        if success:
            self.player.spend_credits(cost)

        return success, message, cost

    # ==================== MODULE MARKETPLACE METHODS ====================

    def buy_module(self, module_id: str) -> Tuple[bool, str]:
        """Buy a module from the market"""
        location_data = LOCATIONS[self.player.location]

        if "market" not in location_data.get("services", []) and "black_market" not in location_data.get("services", []):
            return False, "No market at this location"

        trade_bonus = self.player.get_skill_bonus("trade_proficiency", "buy_discount")

        success, message, cost = self.module_market.purchase_module(
            module_id,
            self.player.credits,
            self.player.level,
            trade_bonus
        )

        if not success:
            return False, message

        # Deduct credits
        self.player.spend_credits(cost)

        # Add module to inventory
        self.player.add_item(module_id, 1)

        return True, message

    def sell_module(self, module_id: str) -> Tuple[bool, str]:
        """Sell a module to the market"""
        location_data = LOCATIONS[self.player.location]

        if "market" not in location_data.get("services", []) and "black_market" not in location_data.get("services", []):
            return False, "No market at this location"

        # Check if player has module
        if not self.player.has_item(module_id, 1):
            return False, "You don't have this module"

        trade_bonus = self.player.get_skill_bonus("trade_proficiency", "sell_bonus")

        success, message, value = self.module_market.sell_module(module_id, trade_bonus)

        if not success:
            return False, message

        # Remove from inventory
        self.player.remove_item(module_id, 1)

        # Add credits
        self.player.add_credits(value)

        return True, message

    # ==================== COMPONENT MARKETPLACE METHODS ====================

    def buy_component(self, comp_id: str) -> Tuple[bool, str]:
        """Buy a ship component from the market"""
        location_data = LOCATIONS[self.player.location]

        if "market" not in location_data.get("services", []) and "black_market" not in location_data.get("services", []):
            return False, "No market at this location"

        trade_bonus = self.player.get_skill_bonus("trade_proficiency", "buy_discount")

        success, message, cost = self.component_market.purchase_component(
            comp_id,
            self.player.credits,
            self.player.level,
            trade_bonus
        )

        if not success:
            return False, message

        # Deduct credits
        self.player.spend_credits(cost)

        # Add component to inventory
        cargo_capacity = self.vessel.cargo_capacity
        success, add_msg = self.player.add_item(comp_id, 1, cargo_capacity)

        if not success:
            # Refund if cargo is full
            self.player.add_credits(cost)
            return False, f"Cargo hold full! {add_msg}"

        return True, message

    def sell_component(self, comp_id: str) -> Tuple[bool, str]:
        """Sell a ship component to the market"""
        location_data = LOCATIONS[self.player.location]

        if "market" not in location_data.get("services", []) and "black_market" not in location_data.get("services", []):
            return False, "No market at this location"

        # Check if player has component
        if not self.player.has_item(comp_id, 1):
            return False, "You don't have this component"

        trade_bonus = self.player.get_skill_bonus("trade_proficiency", "sell_bonus")

        success, message, value = self.component_market.sell_component(comp_id, trade_bonus)

        if not success:
            return False, message

        # Remove from inventory
        self.player.remove_item(comp_id, 1)

        # Add credits
        self.player.add_credits(value)

        return True, message

    def buy_ship(self, ship_id: str) -> Tuple[bool, str]:
        """Buy a complete ship from the shipyard"""
        location_data = LOCATIONS[self.player.location]

        if "shipyard" not in location_data.get("services", []):
            return False, "No shipyard at this location"

        # Check berth availability
        if not self.berth_manager.has_empty_berth(self.player.location):
            return False, "NO_BERTH"  # Special flag for GUI to offer berth purchase

        trade_bonus = self.player.get_skill_bonus("trade_proficiency", "buy_discount")

        success, message, cost = self.ship_market.purchase_ship(
            ship_id,
            self.player.location,
            self.player.credits,
            self.player.level,
            trade_bonus
        )

        if not success:
            return False, message

        # Deduct credits
        self.player.spend_credits(cost)

        # Store ship in berth
        success_berth, berth_msg = self.berth_manager.store_ship(self.player.location, ship_id)
        if not success_berth:
            # Refund if can't store (shouldn't happen due to check above)
            self.player.add_credits(cost)
            return False, f"Failed to store ship: {berth_msg}"

        # Award XP for major purchase
        xp_reward = 100
        self.player.add_experience(xp_reward)

        return True, f"{message} - Stored in shipyard berth (+{xp_reward} XP)"

    def sell_ship(self, ship_id: str) -> Tuple[bool, str]:
        """Sell a ship to the shipyard"""
        location_data = LOCATIONS[self.player.location]

        if "shipyard" not in location_data.get("services", []):
            return False, "No shipyard at this location"

        # Check if player has ship in station inventory
        station_inv = self.player.get_station_inventory(self.player.location)
        if ship_id not in station_inv or station_inv[ship_id] < 1:
            return False, "You don't have this ship at this station"

        # Don't allow selling current vessel
        if self.vessel and self.vessel.vessel_class_id == ship_id:
            return False, "Cannot sell your current vessel. Switch to another ship first."

        trade_bonus = self.player.get_skill_bonus("trade_proficiency", "sell_bonus")

        success, message, value = self.ship_market.sell_ship(ship_id, trade_bonus)

        if not success:
            return False, message

        # Remove from station inventory
        station_inv[ship_id] -= 1
        if station_inv[ship_id] == 0:
            del station_inv[ship_id]

        # Add credits
        self.player.add_credits(value)

        return True, message

    def switch_ship(self, new_ship_id: str) -> Tuple[bool, str]:
        """
        Switch from current ship to another ship in berths at current location
        Returns: (success, message)
        """
        # Check if at a shipyard
        location_data = LOCATIONS[self.player.location]
        if "shipyard" not in location_data.get("services", []):
            return False, "No shipyard at this location"

        # Check if new ship is in berths at this location
        ships_in_berths = self.berth_manager.get_ships_at_location(self.player.location)
        if new_ship_id not in ships_in_berths:
            return False, "Ship not found in berths at this location"

        # Can't switch to current ship
        current_ship_id = self.vessel.vessel_class_id
        if new_ship_id == current_ship_id:
            return False, "You are already piloting this ship"

        # Check if player meets level requirement for new ship
        if new_ship_id not in VESSEL_CLASSES:
            return False, "Invalid ship"

        new_ship_data = VESSEL_CLASSES[new_ship_id]
        level_req = new_ship_data.get("level_requirement", 1)
        if self.player.level < level_req:
            return False, f"Requires level {level_req} to pilot this ship"

        # Save current ship modules
        old_modules = dict(self.vessel.installed_modules)

        # Simply switch to the new ship (both remain in berths at this location)
        # No need to remove/add - just change which vessel we're piloting
        self.vessel = Vessel(new_ship_id)
        self.player.current_ship_id = new_ship_id

        # Try to reinstall compatible modules from old ship
        reinstalled = []
        moved_to_inventory = []

        for mod_type, modules in old_modules.items():
            for module_id in modules:
                success, msg, _ = self.vessel.install_module(module_id)
                if success:
                    reinstalled.append(module_id)
                else:
                    # Add to player ship cargo if can't install
                    self.player.add_item(module_id, 1)
                    moved_to_inventory.append(module_id)

        # Set hull and shields to full after installing modules
        self.vessel.current_hull_hp = self.vessel.max_hull_hp
        self.vessel.current_shields = self.vessel.get_total_shield_capacity()

        # Build result message
        result_msg = f"Switched to {new_ship_data['name']}"

        if reinstalled:
            result_msg += f"\n\nReinstalled {len(reinstalled)} compatible modules"

        if moved_to_inventory:
            result_msg += f"\n\n{len(moved_to_inventory)} incompatible modules moved to cargo"

        # Check cargo capacity
        cargo_used = self.player.get_cargo_volume()
        cargo_capacity = self.vessel.cargo_capacity
        if cargo_used > cargo_capacity:
            result_msg += f"\n\n⚠️ WARNING: Cargo exceeds capacity ({cargo_used:.1f}/{cargo_capacity:.0f})! Offload items to travel."

        return True, result_msg

    # ==================== COMMODITY TRADING METHODS ====================

    def buy_commodity(self, commodity_id: str, quantity: int) -> Tuple[bool, str]:
        """Buy commodity from market"""
        location_data = LOCATIONS[self.player.location]

        if "market" not in location_data.get("services", []):
            return False, "No market at this location"

        # Get purchase price
        buy_price = self.commodity_market.get_price(self.player.location, commodity_id, is_buying=True)
        total_cost = buy_price * quantity

        # Check if player has enough credits
        if self.player.credits < total_cost:
            return False, f"Insufficient credits. Need {total_cost:,} CR (have {self.player.credits:,} CR)"

        # Attempt purchase
        success, message, actual_cost = self.commodity_market.buy_commodity(
            self.player.location,
            commodity_id,
            quantity
        )

        if not success:
            return False, message

        # Deduct credits
        self.player.spend_credits(actual_cost)

        # Add to ship cargo (commodities go to ship inventory)
        cargo_capacity = self.vessel.cargo_capacity if self.vessel else None
        add_success, add_message = self.player.add_item(commodity_id, quantity, cargo_capacity)

        if not add_success:
            # Refund if cargo full
            self.player.add_credits(actual_cost)
            # Refund market transaction
            self.commodity_market.sell_commodity(self.player.location, commodity_id, quantity)
            return False, add_message

        return True, message

    def sell_commodity(self, commodity_id: str, quantity: int) -> Tuple[bool, str]:
        """Sell commodity to market"""
        location_data = LOCATIONS[self.player.location]

        if "market" not in location_data.get("services", []):
            return False, "No market at this location"

        # Check if player has commodity
        if not self.player.has_item(commodity_id, quantity):
            return False, "You don't have enough of this commodity"

        # Attempt sale
        success, message, revenue = self.commodity_market.sell_commodity(
            self.player.location,
            commodity_id,
            quantity
        )

        if not success:
            return False, message

        # Remove from inventory
        self.player.remove_item(commodity_id, quantity)

        # Add credits
        self.player.add_credits(revenue)

        return True, message

    # ==================== RECYCLING METHODS ====================

    def recycle_component(self, comp_id: str) -> Tuple[bool, str]:
        """Recycle a component into materials"""
        location_data = LOCATIONS[self.player.location]

        if "manufacturing" not in location_data.get("services", []):
            return False, "Recycling requires a manufacturing facility"

        # Check if player has component
        if not self.player.has_item(comp_id, 1):
            return False, "You don't have this component"

        success, message, materials = self.recycling.recycle_component(comp_id)

        if not success:
            return False, message

        # Remove component from inventory
        self.player.remove_item(comp_id, 1)

        # Add recovered materials to cargo
        cargo_capacity = self.vessel.cargo_capacity
        materials_added = []
        cargo_warnings = []

        for material, quantity in materials.items():
            success_add, add_msg = self.player.add_item(material, quantity, cargo_capacity)
            if success_add:
                materials_added.append(f"{material}×{quantity}")
            else:
                cargo_warnings.append(f"Could not add {material}×{quantity}: {add_msg}")

        # Award XP for recycling
        xp_reward = 20
        self.player.add_experience(xp_reward)

        result_msg = f"{message} (+{xp_reward} XP)"
        if cargo_warnings:
            result_msg += f" WARNING: {', '.join(cargo_warnings)}"

        return True, result_msg

    def recycle_ship(self, ship_id: str) -> Tuple[bool, str]:
        """Recycle a ship into materials"""
        location_data = LOCATIONS[self.player.location]

        if "manufacturing" not in location_data.get("services", []):
            return False, "Recycling requires a manufacturing facility"

        # Check if player has ship
        if not self.player.has_item(ship_id, 1):
            return False, "You don't have this ship"

        # Don't allow recycling current vessel
        if self.vessel and self.vessel.vessel_class_id == ship_id:
            return False, "Cannot recycle your current vessel. Switch to another ship first."

        success, message, materials = self.recycling.recycle_ship(ship_id)

        if not success:
            return False, message

        # Remove ship from inventory
        self.player.remove_item(ship_id, 1)

        # Add recovered materials to cargo
        cargo_capacity = self.vessel.cargo_capacity
        materials_added = []
        cargo_warnings = []

        for material, quantity in materials.items():
            success_add, add_msg = self.player.add_item(material, quantity, cargo_capacity)
            if success_add:
                materials_added.append(f"{material}×{quantity}")
            else:
                cargo_warnings.append(f"Could not add {material}×{quantity}: {add_msg}")

        # Award XP for recycling (ships give more XP)
        xp_reward = 150
        self.player.add_experience(xp_reward)

        result_msg = f"{message} (+{xp_reward} XP)"
        if cargo_warnings:
            result_msg += f" WARNING: {', '.join(cargo_warnings)}"

        return True, result_msg

    # ==================== MANUFACTURING METHODS ====================

    def start_manufacturing(self, item_id: str, quantity: int) -> Tuple[bool, str]:
        """Start manufacturing modules, components, or ships"""
        location_data = LOCATIONS[self.player.location]

        if "manufacturing" not in location_data.get("services", []):
            return False, "No manufacturing facility at this location"

        # Determine item type and use appropriate skill
        item_type = self.manufacturing.detect_item_type(item_id)
        if item_type == "ship":
            skill_name = "ship_construction"
        else:
            skill_name = "module_manufacturing"

        skill_level = self.player.get_skill_level(skill_name)
        skill_bonus = self.player.get_skill_bonus(skill_name, "manufacturing_speed")

        success, message = self.manufacturing.start_manufacturing(
            item_id,
            quantity,
            self.player.ship_cargo,
            self.player.level,
            skill_level,
            skill_bonus,
            self.player.remove_item
        )

        return success, message

    def check_manufacturing(self) -> List[str]:
        """Check for completed manufacturing jobs"""
        messages = []

        completed = self.manufacturing.check_completed_jobs()
        cargo_capacity = self.vessel.cargo_capacity

        for item_id, quantity, item_type in completed:
            item_name = self.manufacturing.get_item_name(item_id)

            # Handle ship manufacturing differently
            if item_type == "ship":
                # For ships, we don't add to inventory - player would use shipyard to "claim" it
                # For now, just add notification and add to inventory temporarily
                success, msg = self.player.add_item(item_id, quantity, cargo_capacity)
                if success:
                    messages.append(f"Ship construction complete: {quantity}x {item_name} (available in inventory)")
                else:
                    messages.append(f"Ship construction complete but cargo full: {msg}")
            else:
                # Add manufactured items to inventory (components and modules)
                success, msg = self.player.add_item(item_id, quantity, cargo_capacity)
                if success:
                    messages.append(f"Manufacturing complete: {quantity}x {item_name}")
                else:
                    messages.append(f"Manufacturing complete but cargo full: {msg}")

            if success:
                self.player.stats["items_manufactured"] += quantity

        return messages

    # ==================== INVENTORY MANAGEMENT METHODS ====================

    def transfer_to_station(self, item_id: str, quantity: int) -> Tuple[bool, str]:
        """Transfer items from ship to station storage"""
        return self.player.transfer_to_station(item_id, quantity)

    def transfer_to_ship(self, item_id: str, quantity: int, location_id: str = None) -> Tuple[bool, str]:
        """Transfer items from station to ship"""
        return self.player.transfer_to_ship(item_id, quantity, location_id)

    # ==================== MODULE INSTALLATION METHODS ====================

    def install_module_on_ship(self, module_id: str) -> Tuple[bool, str]:
        """Install a module from inventory onto ship"""
        if not self.player.has_item(module_id, 1):
            return False, "Module not in inventory"

        success, message, replaced_mod = self.vessel.install_module(module_id)
        if success:
            self.player.remove_item(module_id, 1)

            # If a module was replaced, add it to station inventory
            if replaced_mod:
                station_inv = self.player.get_station_inventory(self.player.location)
                if replaced_mod in station_inv:
                    station_inv[replaced_mod] += 1
                else:
                    station_inv[replaced_mod] = 1

            return True, message
        else:
            return False, message

    def uninstall_module_from_ship(self, module_id: str) -> Tuple[bool, str]:
        """Uninstall a module from ship to inventory"""
        if self.vessel.uninstall_module(module_id):
            self.player.add_item(module_id, 1)
            module_name = MODULES[module_id]["name"]
            return True, f"Uninstalled {module_name}"
        else:
            return False, "Module not installed on ship"

    def get_game_stats(self) -> Dict:
        """Get comprehensive game statistics"""
        if not self.player:
            return {}

        self.player.update_play_time()

        return {
            "player_name": self.player.name,
            "credits": self.player.credits,
            "location": LOCATIONS[self.player.location]["name"],
            "vessel": self.vessel.name,
            "play_time": f"{int(self.player.stats['time_played'] / 60)} minutes",
            "contracts_completed": self.player.stats["contracts_completed"],
            "enemies_destroyed": self.player.stats["enemies_destroyed"],
            "resources_mined": self.player.stats["resources_mined"],
            "total_earnings": self.player.stats["total_earnings"],
            "total_spent": self.player.stats["total_spent"]
        }
