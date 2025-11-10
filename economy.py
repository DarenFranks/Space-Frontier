"""
Economy and Market System
Handles resource trading, market prices, and economic simulation
"""

import random
from typing import Dict, List, Optional, Tuple
from data import RESOURCES, LOCATIONS, MODULES, SHIP_COMPONENTS, VESSEL_CLASSES
from config import MARKET_FLUCTUATION_RANGE, TAX_RATE


class Market:
    """Represents a market at a location"""

    def __init__(self, location_id: str):
        self.location_id = location_id
        self.prices: Dict[str, float] = {}
        self.stock: Dict[str, int] = {}

        # Initialize prices and stock based on location
        self._initialize_market()

    def _initialize_market(self):
        """Set up initial market conditions"""
        location_data = LOCATIONS.get(self.location_id, {})
        available_resources = location_data.get("resources", [])

        for resource_id, resource_data in RESOURCES.items():
            base_price = resource_data["base_price"]

            # Resources available at location have better prices and more stock
            if resource_id in available_resources:
                # Local resources are 20-30% cheaper
                price_multiplier = random.uniform(0.7, 0.8)
                stock_amount = random.randint(1000, 5000)
            else:
                # Imported resources are more expensive with less stock
                price_multiplier = random.uniform(1.2, 1.5)
                stock_amount = random.randint(100, 500)

            self.prices[resource_id] = base_price * price_multiplier
            self.stock[resource_id] = stock_amount

    def fluctuate_prices(self):
        """Simulate market price changes"""
        for resource_id in self.prices:
            base_price = RESOURCES[resource_id]["base_price"]
            current_price = self.prices[resource_id]

            # Random fluctuation
            change = random.uniform(-MARKET_FLUCTUATION_RANGE, MARKET_FLUCTUATION_RANGE)
            new_price = current_price * (1 + change)

            # Keep prices within reasonable bounds
            min_price = base_price * 0.5
            max_price = base_price * 3.0
            self.prices[resource_id] = max(min_price, min(max_price, new_price))

        # Randomly adjust stock
        for resource_id in self.stock:
            change = random.randint(-100, 200)
            self.stock[resource_id] = max(0, self.stock[resource_id] + change)

    def get_buy_price(self, resource_id: str, quantity: int = 1,
                     trade_bonus: float = 0.0) -> float:
        """Calculate price to buy from market (player buying)"""
        if resource_id not in self.prices:
            return 0

        base_price = self.prices[resource_id]

        # Discount from trade skill
        discount = 1.0 - trade_bonus

        # Bulk purchase has slight premium
        if quantity > 100:
            bulk_multiplier = 1.1
        else:
            bulk_multiplier = 1.0

        return base_price * discount * bulk_multiplier * quantity

    def get_sell_price(self, resource_id: str, quantity: int = 1,
                      trade_bonus: float = 0.0, tax_reduction: float = 0.0) -> float:
        """Calculate price to sell to market (player selling)"""
        if resource_id not in self.prices:
            return 0

        base_price = self.prices[resource_id]

        # Bonus from trade skill
        bonus = 1.0 + trade_bonus

        # Selling in bulk gives slight penalty
        if quantity > 100:
            bulk_penalty = 0.9
        else:
            bulk_penalty = 1.0

        # Calculate tax
        tax = max(0, TAX_RATE - tax_reduction)

        return base_price * bonus * bulk_penalty * (1 - tax) * quantity

    def buy_from_market(self, resource_id: str, quantity: int,
                       player_credits: int, trade_bonus: float = 0.0) -> Tuple[bool, str, int]:
        """
        Player buys from market.
        Returns: (success, message, cost)
        """
        if resource_id not in RESOURCES:
            return False, "Invalid resource", 0

        if resource_id not in self.stock or self.stock[resource_id] < quantity:
            return False, "Insufficient stock available", 0

        cost = self.get_buy_price(resource_id, quantity, trade_bonus)

        if player_credits < cost:
            return False, "Insufficient credits", int(cost)

        # Complete transaction
        self.stock[resource_id] -= quantity

        resource_name = RESOURCES[resource_id]["name"]
        return True, f"Purchased {quantity}x {resource_name}", int(cost)

    def sell_to_market(self, resource_id: str, quantity: int,
                      trade_bonus: float = 0.0, tax_reduction: float = 0.0) -> Tuple[bool, str, int]:
        """
        Player sells to market.
        Returns: (success, message, payment)
        """
        if resource_id not in RESOURCES:
            return False, "Invalid resource", 0

        payment = self.get_sell_price(resource_id, quantity, trade_bonus, tax_reduction)

        # Add to market stock
        if resource_id in self.stock:
            self.stock[resource_id] += quantity
        else:
            self.stock[resource_id] = quantity

        resource_name = RESOURCES[resource_id]["name"]
        return True, f"Sold {quantity}x {resource_name}", int(payment)

    def get_market_listing(self, filter_available: bool = False) -> List[Dict]:
        """Get list of market prices and availability"""
        listings = []

        for resource_id, resource_data in RESOURCES.items():
            if resource_id not in self.prices:
                continue

            if filter_available and self.stock.get(resource_id, 0) == 0:
                continue

            listings.append({
                "id": resource_id,
                "name": resource_data["name"],
                "description": resource_data["description"],
                "buy_price": int(self.prices[resource_id]),
                "sell_price": int(self.prices[resource_id] * 0.8),  # Sell for less
                "stock": self.stock.get(resource_id, 0),
                "rarity": resource_data["rarity"]
            })

        # Sort by price
        listings.sort(key=lambda x: x["buy_price"])

        return listings

    def to_dict(self) -> Dict:
        """Convert market to dictionary"""
        return {
            "location_id": self.location_id,
            "prices": self.prices,
            "stock": self.stock
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Market':
        """Create market from dictionary"""
        market = cls(data["location_id"])
        market.prices = data["prices"]
        market.stock = data["stock"]
        return market


class EconomyManager:
    """Manages all markets and economic simulation"""

    def __init__(self):
        self.markets: Dict[str, Market] = {}
        self._initialize_markets()

    def _initialize_markets(self):
        """Create markets for all locations"""
        for location_id in LOCATIONS.keys():
            location_data = LOCATIONS[location_id]

            # Only create market if location has market service
            if "market" in location_data.get("services", []):
                self.markets[location_id] = Market(location_id)

    def get_market(self, location_id: str) -> Optional[Market]:
        """Get market at location"""
        return self.markets.get(location_id)

    def update_markets(self):
        """Update all market prices and stock"""
        for market in self.markets.values():
            market.fluctuate_prices()

    def find_best_trade_route(self, resource_id: str) -> Optional[Dict]:
        """Find best buy/sell locations for a resource"""
        if resource_id not in RESOURCES:
            return None

        buy_prices = []
        sell_prices = []

        for location_id, market in self.markets.items():
            if resource_id in market.prices and market.stock.get(resource_id, 0) > 0:
                buy_price = market.get_buy_price(resource_id, 1)
                sell_price = market.get_sell_price(resource_id, 1)

                buy_prices.append((location_id, buy_price))
                sell_prices.append((location_id, sell_price))

        if not buy_prices or not sell_prices:
            return None

        # Find cheapest buy and highest sell
        best_buy = min(buy_prices, key=lambda x: x[1])
        best_sell = max(sell_prices, key=lambda x: x[1])

        profit_margin = best_sell[1] - best_buy[1]

        return {
            "resource": RESOURCES[resource_id]["name"],
            "buy_location": LOCATIONS[best_buy[0]]["name"],
            "buy_price": int(best_buy[1]),
            "sell_location": LOCATIONS[best_sell[0]]["name"],
            "sell_price": int(best_sell[1]),
            "profit_per_unit": int(profit_margin)
        }

    def to_dict(self) -> Dict:
        """Convert economy to dictionary"""
        return {
            "markets": {loc_id: market.to_dict()
                       for loc_id, market in self.markets.items()}
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'EconomyManager':
        """Create economy from dictionary"""
        economy = cls()
        economy.markets = {loc_id: Market.from_dict(market_data)
                          for loc_id, market_data in data["markets"].items()}
        return economy


class ModuleMarket:
    """Handles buying and selling of ship modules"""

    def __init__(self):
        self.markup_multiplier = 1.3  # Modules sold for 30% above manufacturing cost
        self.buyback_multiplier = 0.60  # Buy used modules for 60% of cost

    def get_available_modules(self, player_level: int, location_services: List[str]) -> List[Dict]:
        """Get modules available for purchase"""
        if "market" not in location_services and "black_market" not in location_services:
            return []

        available = []

        for module_id, module_data in MODULES.items():
            # Check level requirement
            level_req = module_data.get("level_requirement", 1)
            if player_level >= level_req:
                # Calculate cost
                base_cost = module_data.get("manufacturing_cost", 1000)
                sell_price = int(base_cost * self.markup_multiplier)

                available.append({
                    "id": module_id,
                    "name": module_data["name"],
                    "type": module_data["type"],
                    "tier": module_data.get("tier", 1),
                    "cost": sell_price,
                    "level_req": level_req,
                    "description": module_data["description"]
                })

        # Sort by type, then tier
        available.sort(key=lambda x: (x["type"], x["tier"]))

        return available

    def get_module_cost(self, module_id: str, player_level: int) -> Optional[int]:
        """Get purchase cost for a module"""
        if module_id not in MODULES:
            return None

        module_data = MODULES[module_id]
        level_req = module_data.get("level_requirement", 1)

        if player_level < level_req:
            return None

        base_cost = module_data.get("manufacturing_cost", 1000)
        return int(base_cost * self.markup_multiplier)

    def get_module_value(self, module_id: str) -> int:
        """Get sellback value for a module"""
        if module_id not in MODULES:
            return 0

        base_cost = MODULES[module_id].get("manufacturing_cost", 1000)
        return int(base_cost * self.buyback_multiplier)

    def purchase_module(
        self,
        module_id: str,
        player_credits: int,
        player_level: int,
        trade_bonus: float = 0.0
    ) -> Tuple[bool, str, int]:
        """
        Purchase a module
        Returns: (success, message, cost)
        """
        if module_id not in MODULES:
            return False, "Invalid module", 0

        module_data = MODULES[module_id]

        # Check level requirement
        level_req = module_data.get("level_requirement", 1)
        if player_level < level_req:
            return False, f"Requires level {level_req}", 0

        # Calculate cost with trade bonus
        base_cost = module_data.get("manufacturing_cost", 1000)
        cost = int(base_cost * self.markup_multiplier * (1.0 - trade_bonus))

        # Check funds
        if player_credits < cost:
            return False, f"Insufficient credits. Need {cost:,} CR", 0

        return True, f"Purchased {module_data['name']} for {cost:,} CR", cost

    def sell_module(self, module_id: str, trade_bonus: float = 0.0) -> Tuple[bool, str, int]:
        """
        Sell a module
        Returns: (success, message, value)
        """
        if module_id not in MODULES:
            return False, "Invalid module", 0

        base_value = self.get_module_value(module_id)
        value = int(base_value * (1.0 + trade_bonus))

        module_name = MODULES[module_id]["name"]

        return True, f"Sold {module_name} for {value:,} CR", value

    def get_modules_by_type(self, module_type: str, player_level: int) -> List[Dict]:
        """Get all modules of a specific type"""
        modules = []

        for module_id, module_data in MODULES.items():
            if module_data["type"] == module_type:
                level_req = module_data.get("level_requirement", 1)
                if player_level >= level_req:
                    base_cost = module_data.get("manufacturing_cost", 1000)
                    cost = int(base_cost * self.markup_multiplier)

                    modules.append({
                        "id": module_id,
                        "name": module_data["name"],
                        "tier": module_data.get("tier", 1),
                        "cost": cost,
                        "level_req": level_req
                    })

        modules.sort(key=lambda x: x["tier"])
        return modules


class ComponentMarket:
    """Handles buying and selling of ship components"""

    def __init__(self):
        self.markup_multiplier = 1.8  # Components sold for 80% above manufacturing cost (increased from 1.3)
        self.component_cost_multiplier = 1.5  # Base manufacturing cost multiplier
        self.buyback_multiplier = 0.60  # Buy used components for 60% of cost

    def get_available_components(self, player_level: int, location_services: List[str]) -> List[Dict]:
        """Get components available for purchase"""
        if "market" not in location_services and "black_market" not in location_services:
            return []

        available = []

        for comp_id, comp_data in SHIP_COMPONENTS.items():
            # Check level requirement
            level_req = comp_data.get("level_requirement", 1)
            if player_level >= level_req:
                # Calculate cost
                base_cost = comp_data.get("manufacturing_cost", 1000)
                # Apply component cost multiplier then markup
                sell_price = int(base_cost * self.component_cost_multiplier * self.markup_multiplier)

                available.append({
                    "id": comp_id,
                    "name": comp_data["name"],
                    "type": comp_data["type"],
                    "tier": comp_data.get("tier", 1),
                    "cost": sell_price,
                    "level_req": level_req,
                    "description": comp_data["description"]
                })

        # Sort by type, then tier
        available.sort(key=lambda x: (x["type"], x["tier"]))

        return available

    def get_component_cost(self, comp_id: str, player_level: int) -> Optional[int]:
        """Get purchase cost for a component"""
        if comp_id not in SHIP_COMPONENTS:
            return None

        comp_data = SHIP_COMPONENTS[comp_id]
        level_req = comp_data.get("level_requirement", 1)

        if player_level < level_req:
            return None

        base_cost = comp_data.get("manufacturing_cost", 1000)
        # Apply component cost multiplier then markup
        return int(base_cost * self.component_cost_multiplier * self.markup_multiplier)

    def get_component_value(self, comp_id: str) -> int:
        """Get sellback value for a component"""
        if comp_id not in SHIP_COMPONENTS:
            return 0

        base_cost = SHIP_COMPONENTS[comp_id].get("manufacturing_cost", 1000)
        return int(base_cost * self.buyback_multiplier)

    def purchase_component(
        self,
        comp_id: str,
        player_credits: int,
        player_level: int,
        trade_bonus: float = 0.0
    ) -> Tuple[bool, str, int]:
        """
        Purchase a component
        Returns: (success, message, cost)
        """
        if comp_id not in SHIP_COMPONENTS:
            return False, "Invalid component", 0

        comp_data = SHIP_COMPONENTS[comp_id]

        # Check level requirement
        level_req = comp_data.get("level_requirement", 1)
        if player_level < level_req:
            return False, f"Requires level {level_req}", 0

        # Calculate cost with trade bonus
        base_cost = comp_data.get("manufacturing_cost", 1000)
        # Apply component cost multiplier then markup, then trade bonus
        cost = int(base_cost * self.component_cost_multiplier * self.markup_multiplier * (1.0 - trade_bonus))

        # Check funds
        if player_credits < cost:
            return False, f"Insufficient credits. Need {cost:,} CR", 0

        return True, f"Purchased {comp_data['name']} for {cost:,} CR", cost

    def sell_component(self, comp_id: str, trade_bonus: float = 0.0) -> Tuple[bool, str, int]:
        """
        Sell a component
        Returns: (success, message, value)
        """
        if comp_id not in SHIP_COMPONENTS:
            return False, "Invalid component", 0

        base_value = self.get_component_value(comp_id)
        value = int(base_value * (1.0 + trade_bonus))

        comp_name = SHIP_COMPONENTS[comp_id]["name"]

        return True, f"Sold {comp_name} for {value:,} CR", value

    def get_components_by_type(self, comp_type: str, player_level: int) -> List[Dict]:
        """Get all components of a specific type"""
        components = []

        for comp_id, comp_data in SHIP_COMPONENTS.items():
            if comp_data["type"] == comp_type:
                level_req = comp_data.get("level_requirement", 1)
                if player_level >= level_req:
                    base_cost = comp_data.get("manufacturing_cost", 1000)
                    # Apply component cost multiplier then markup
                    cost = int(base_cost * self.component_cost_multiplier * self.markup_multiplier)

                    components.append({
                        "id": comp_id,
                        "name": comp_data["name"],
                        "tier": comp_data.get("tier", 1),
                        "cost": cost,
                        "level_req": level_req
                    })

        components.sort(key=lambda x: x["tier"])
        return components


class ShipMarket:
    """Handles buying and selling of complete ships"""

    def __init__(self):
        self.markup_multiplier = 2.5  # Ships sold for 150% above component cost (increased from 1.5)
        self.component_cost_multiplier = 1.5  # Component manufacturing costs multiplier (for building ships)
        self.buyback_multiplier = 0.70  # Buy used ships for 70% of cost
        self.station_inventories = {}  # location_id: {ship_id: quantity}
        self.last_restock_time = 0  # Track when inventory was last restocked

    def calculate_ship_cost(self, ship_id: str) -> int:
        """Calculate the market cost of a ship based on its components or base cost"""
        if ship_id not in VESSEL_CLASSES:
            return 0

        from data import SHIP_RECIPES, SHIP_COMPONENTS

        # Get ship recipe to find component requirements
        if ship_id not in SHIP_RECIPES:
            # No recipe available - use base cost from VESSEL_CLASSES with markup
            ship_data = VESSEL_CLASSES[ship_id]
            base_cost = ship_data.get("cost", 0)
            # Apply markup to base cost
            return int(base_cost * self.markup_multiplier)

        recipe = SHIP_RECIPES[ship_id]
        total_component_cost = 0

        # Sum up manufacturing costs of all required components
        for comp_id, quantity in recipe.get("components", {}).items():
            if comp_id in SHIP_COMPONENTS:
                comp_cost = SHIP_COMPONENTS[comp_id].get("manufacturing_cost", 1000)
                # Apply component cost multiplier to increase building costs
                total_component_cost += comp_cost * quantity * self.component_cost_multiplier

        # Apply markup
        return int(total_component_cost * self.markup_multiplier)

    def calculate_ship_value(self, ship_id: str) -> int:
        """Calculate the sellback value of a ship"""
        base_cost = self.calculate_ship_cost(ship_id)
        # Remove markup, then apply buyback multiplier
        component_cost = base_cost / self.markup_multiplier
        return int(component_cost * self.buyback_multiplier)

    def generate_station_inventory(self, location_id: str, location_data: Dict) -> None:
        """Generate RNG-based ship inventory for a station"""
        import random

        if "shipyard" not in location_data.get("services", []):
            return

        inventory = {}

        # Get all ship types and tiers
        ships_by_tier = {}
        for ship_id, ship_data in VESSEL_CLASSES.items():
            tier = ship_data.get("tier_num", 1)
            if tier not in ships_by_tier:
                ships_by_tier[tier] = []
            ships_by_tier[tier].append(ship_id)

        # Stock 8-15 different ship types (increased from 3-8 for better availability)
        num_types = random.randint(8, 15)

        # Bias towards lower tiers (adjusted to show more variety)
        tier_weights = {1: 35, 2: 30, 3: 20, 4: 12, 5: 6, 6: 3, 7: 1}

        available_ships = []
        for tier, ships in ships_by_tier.items():
            weight = tier_weights.get(tier, 1)
            for ship_id in ships:
                for _ in range(int(weight)):
                    available_ships.append(ship_id)

        # Randomly select ships
        if available_ships:
            selected_ships = random.sample(available_ships, min(num_types, len(available_ships)))

            for ship_id in selected_ships:
                ship_data = VESSEL_CLASSES[ship_id]
                tier = ship_data.get("tier_num", 1)

                # Lower tier ships have more stock (increased quantities for better availability)
                if tier == 1:
                    quantity = random.randint(3, 6)
                elif tier == 2:
                    quantity = random.randint(2, 4)
                elif tier <= 4:
                    quantity = random.randint(1, 3)
                else:
                    quantity = random.randint(1, 2)  # High tier ships still somewhat rare

                inventory[ship_id] = quantity

        self.station_inventories[location_id] = inventory

    def initialize_all_stations(self, locations: Dict) -> None:
        """Initialize inventory for all stations"""
        for location_id, location_data in locations.items():
            if "shipyard" in location_data.get("services", []):
                self.generate_station_inventory(location_id, location_data)

    def get_station_inventory(self, location_id: str) -> Dict[str, int]:
        """Get current inventory at a station"""
        return self.station_inventories.get(location_id, {})

    def get_available_ships(self, location_id: str, player_level: int, player_credits: int) -> List[Dict]:
        """
        Get ships available for purchase at a station
        Shows ALL ships in stock regardless of player level/credits
        """
        inventory = self.get_station_inventory(location_id)

        if not inventory:
            return []

        available = []

        for ship_id, stock_quantity in inventory.items():
            if ship_id not in VESSEL_CLASSES:
                continue

            ship_data = VESSEL_CLASSES[ship_id]
            level_req = ship_data.get("level_requirement", 1)
            cost = self.calculate_ship_cost(ship_id)

            # Determine if player can purchase
            can_afford = player_credits >= cost
            can_pilot = player_level >= level_req
            in_stock = stock_quantity > 0
            can_purchase = can_afford and can_pilot and in_stock

            available.append({
                "id": ship_id,
                "name": ship_data["name"],
                "class_type": ship_data.get("class_type", "unknown"),
                "variant": ship_data.get("variant", "standard"),
                "tier": ship_data.get("tier", "mk1"),
                "tier_num": ship_data.get("tier_num", 1),
                "cost": cost,
                "level_req": level_req,
                "stock": stock_quantity,
                "can_afford": can_afford,
                "can_pilot": can_pilot,
                "in_stock": in_stock,
                "can_purchase": can_purchase,
                "stats": {
                    "hull_hp": ship_data.get("hull_hp", 0),
                    "shield_capacity": ship_data.get("base_shield_capacity", 0),
                    "armor_rating": ship_data.get("armor_rating", 0),
                    "base_speed": ship_data.get("base_speed", 0),
                    "cargo_capacity": ship_data.get("cargo_capacity", 0)
                }
            })

        # Sort by tier, then by cost
        available.sort(key=lambda x: (x["tier_num"], x["cost"]))

        return available

    def purchase_ship(
        self,
        ship_id: str,
        location_id: str,
        player_credits: int,
        player_level: int,
        trade_bonus: float = 0.0
    ) -> Tuple[bool, str, int]:
        """
        Purchase a ship from station inventory
        Returns: (success, message, cost)
        """
        if ship_id not in VESSEL_CLASSES:
            return False, "Invalid ship", 0

        # Check if in stock
        inventory = self.get_station_inventory(location_id)
        if ship_id not in inventory or inventory[ship_id] <= 0:
            return False, "Ship not in stock at this location", 0

        ship_data = VESSEL_CLASSES[ship_id]

        # Check level requirement
        level_req = ship_data.get("level_requirement", 1)
        if player_level < level_req:
            return False, f"Requires level {level_req}", 0

        # Calculate cost with trade bonus
        base_cost = self.calculate_ship_cost(ship_id)
        cost = int(base_cost * (1.0 - trade_bonus))

        # Check funds
        if player_credits < cost:
            return False, f"Insufficient credits. Need {cost:,} CR", 0

        # Deduct from inventory
        self.station_inventories[location_id][ship_id] -= 1
        if self.station_inventories[location_id][ship_id] <= 0:
            del self.station_inventories[location_id][ship_id]

        return True, f"Purchased {ship_data['name']} for {cost:,} CR", cost

    def sell_ship(self, ship_id: str, trade_bonus: float = 0.0) -> Tuple[bool, str, int]:
        """
        Sell a ship
        Returns: (success, message, value)
        """
        if ship_id not in VESSEL_CLASSES:
            return False, "Invalid ship", 0

        base_value = self.calculate_ship_value(ship_id)
        value = int(base_value * (1.0 + trade_bonus))

        ship_name = VESSEL_CLASSES[ship_id]["name"]

        return True, f"Sold {ship_name} for {value:,} CR", value

    def to_dict(self) -> Dict:
        """Serialize ship market for saving"""
        return {
            "markup_multiplier": self.markup_multiplier,
            "component_cost_multiplier": self.component_cost_multiplier,
            "buyback_multiplier": self.buyback_multiplier,
            "station_inventories": self.station_inventories,
            "last_restock_time": self.last_restock_time
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'ShipMarket':
        """Deserialize ship market from save data"""
        market = cls()
        market.markup_multiplier = data.get("markup_multiplier", 2.5)
        market.component_cost_multiplier = data.get("component_cost_multiplier", 1.5)
        market.buyback_multiplier = data.get("buyback_multiplier", 0.70)
        market.station_inventories = data.get("station_inventories", {})
        market.last_restock_time = data.get("last_restock_time", 0)
        return market
