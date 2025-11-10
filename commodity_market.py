"""
Commodity Market System
Dynamic pricing based on supply/demand, player actions, and market events
"""

import random
import time
from typing import Dict, List, Tuple, Optional
from data import COMMODITIES, COMMODITY_CATEGORIES, LOCATIONS


class CommodityMarket:
    """Manages commodity trading with dynamic prices at each location"""

    def __init__(self):
        # Market state for each location: {location_id: {commodity_id: market_data}}
        self.markets = {}

        # Player transaction history affects prices
        self.transaction_history = []  # List of (timestamp, location, commodity, quantity, buy/sell)

        # Market events that affect prices
        self.active_events = []  # List of market events

        # Initialize markets for all locations
        self.initialize_markets()

    def initialize_markets(self):
        """Create initial market conditions for all locations"""
        for location_id, location_data in LOCATIONS.items():
            if "market" in location_data.get("services", []):
                self.markets[location_id] = {}

                for commodity_id, commodity_data in COMMODITIES.items():
                    # Each commodity at each location has:
                    # - current_price: fluctuating price
                    # - supply_level: 0.0-2.0 (1.0 = normal)
                    # - demand_level: 0.0-2.0 (1.0 = normal)
                    # - price_trend: current price momentum
                    # - stock: available quantity

                    base_price = commodity_data["base_price"]
                    category = commodity_data["category"]
                    category_data = COMMODITY_CATEGORIES[category]

                    # Initial supply/demand varies by location type
                    supply = random.uniform(0.7, 1.3)
                    demand = random.uniform(0.7, 1.3)

                    # Calculate initial price based on supply/demand
                    price_multiplier = (demand / supply) * random.uniform(0.95, 1.05)
                    current_price = int(base_price * price_multiplier)

                    # Initial stock varies by commodity and location
                    stock = random.randint(100, 500)

                    self.markets[location_id][commodity_id] = {
                        "current_price": current_price,
                        "supply_level": supply,
                        "demand_level": demand,
                        "price_trend": 0.0,  # -1.0 to 1.0
                        "stock": stock,
                        "max_stock": stock * 2,
                        "last_update": time.time(),
                    }

    def get_price(self, location_id: str, commodity_id: str, is_buying: bool = True) -> int:
        """Get current price for a commodity at a location
        is_buying = True means player is buying from market (higher price)
        is_buying = False means player is selling to market (lower price)
        """
        if location_id not in self.markets:
            return 0

        if commodity_id not in self.markets[location_id]:
            return 0

        market_data = self.markets[location_id][commodity_id]
        base_price = market_data["current_price"]

        # Market spread: buy higher, sell lower
        if is_buying:
            return int(base_price * 1.1)  # 10% markup when buying from market
        else:
            return int(base_price * 0.9)  # 10% discount when selling to market

    def buy_commodity(self, location_id: str, commodity_id: str, quantity: int) -> Tuple[bool, str, int]:
        """Player buys commodity from market
        Returns: (success, message, total_cost)
        """
        if location_id not in self.markets:
            return False, "No market at this location", 0

        if commodity_id not in self.markets[location_id]:
            return False, "Commodity not available", 0

        market_data = self.markets[location_id][commodity_id]

        # Check stock
        available = market_data["stock"]
        if quantity > available:
            return False, f"Only {available} units available", 0

        # Calculate cost
        unit_price = self.get_price(location_id, commodity_id, is_buying=True)
        total_cost = unit_price * quantity

        # Update market
        market_data["stock"] -= quantity
        market_data["demand_level"] += quantity * 0.001  # Buying increases demand slightly

        # Record transaction
        self.transaction_history.append({
            "timestamp": time.time(),
            "location": location_id,
            "commodity": commodity_id,
            "quantity": quantity,
            "action": "buy",
            "price": unit_price
        })

        # Update prices based on transaction
        self._update_price_from_transaction(location_id, commodity_id, quantity, "buy")

        return True, f"Purchased {quantity} units for {total_cost:,} CR", total_cost

    def sell_commodity(self, location_id: str, commodity_id: str, quantity: int) -> Tuple[bool, str, int]:
        """Player sells commodity to market
        Returns: (success, message, total_revenue)
        """
        if location_id not in self.markets:
            return False, "No market at this location", 0

        if commodity_id not in self.markets[location_id]:
            return False, "Market doesn't buy this commodity", 0

        market_data = self.markets[location_id][commodity_id]

        # Check if market can accept
        max_stock = market_data["max_stock"]
        current_stock = market_data["stock"]

        if current_stock + quantity > max_stock:
            max_can_buy = max_stock - current_stock
            if max_can_buy <= 0:
                return False, "Market is oversupplied", 0
            return False, f"Market can only buy {max_can_buy} units", 0

        # Calculate revenue
        unit_price = self.get_price(location_id, commodity_id, is_buying=False)
        total_revenue = unit_price * quantity

        # Update market
        market_data["stock"] += quantity
        market_data["supply_level"] += quantity * 0.001  # Selling increases supply slightly

        # Record transaction
        self.transaction_history.append({
            "timestamp": time.time(),
            "location": location_id,
            "commodity": commodity_id,
            "quantity": quantity,
            "action": "sell",
            "price": unit_price
        })

        # Update prices based on transaction
        self._update_price_from_transaction(location_id, commodity_id, quantity, "sell")

        return True, f"Sold {quantity} units for {total_revenue:,} CR", total_revenue

    def _update_price_from_transaction(self, location_id: str, commodity_id: str, quantity: int, action: str):
        """Update prices based on player transaction"""
        market_data = self.markets[location_id][commodity_id]

        # Large transactions affect prices more
        impact = min(quantity / 100.0, 0.1)  # Max 10% impact

        if action == "buy":
            # Player buying drives price up (demand increases)
            market_data["demand_level"] += impact
            market_data["price_trend"] += impact * 0.5
        else:
            # Player selling drives price down (supply increases)
            market_data["supply_level"] += impact
            market_data["price_trend"] -= impact * 0.5

        # Recalculate current price
        self._recalculate_price(location_id, commodity_id)

    def _recalculate_price(self, location_id: str, commodity_id: str):
        """Recalculate commodity price based on supply/demand"""
        market_data = self.markets[location_id][commodity_id]
        commodity_data = COMMODITIES[commodity_id]
        base_price = commodity_data["base_price"]

        supply = market_data["supply_level"]
        demand = market_data["demand_level"]
        volatility = commodity_data["volatility"]

        # Price is based on demand/supply ratio
        if supply > 0:
            price_multiplier = demand / supply
        else:
            price_multiplier = 2.0

        # Apply volatility (some commodities fluctuate more)
        price_multiplier *= (1.0 + random.uniform(-volatility, volatility) * 0.1)

        # Clamp to reasonable range (0.5x to 3.0x base price)
        price_multiplier = max(0.5, min(3.0, price_multiplier))

        market_data["current_price"] = int(base_price * price_multiplier)

    def update_markets(self, time_passed: float = 60.0):
        """Update all markets - prices drift, supply/demand rebalance
        time_passed: seconds since last update
        """
        for location_id in self.markets:
            for commodity_id in self.markets[location_id]:
                market_data = self.markets[location_id][commodity_id]
                commodity_data = COMMODITIES[commodity_id]
                category_data = COMMODITY_CATEGORIES[commodity_data["category"]]

                # Supply and demand drift back toward equilibrium
                drift_rate = 0.1 * (time_passed / 60.0)  # 10% per minute

                market_data["supply_level"] += (1.0 - market_data["supply_level"]) * drift_rate
                market_data["demand_level"] += (1.0 - market_data["demand_level"]) * drift_rate

                # Stock replenishes slowly
                if market_data["stock"] < market_data["max_stock"]:
                    replenish = int(market_data["max_stock"] * 0.05 * (time_passed / 60.0))  # 5% per minute
                    market_data["stock"] = min(market_data["stock"] + replenish, market_data["max_stock"])

                # Random market fluctuations
                if random.random() < category_data["demand_volatility"] * 0.1:
                    market_data["demand_level"] *= random.uniform(0.95, 1.05)

                if random.random() < (1.0 - category_data["supply_stability"]) * 0.1:
                    market_data["supply_level"] *= random.uniform(0.95, 1.05)

                # Recalculate price
                self._recalculate_price(location_id, commodity_id)

                market_data["last_update"] = time.time()

    def get_market_overview(self, location_id: str, category_filter: Optional[str] = None) -> List[Dict]:
        """Get list of all commodities with prices at a location"""
        if location_id not in self.markets:
            return []

        overview = []
        for commodity_id, market_data in self.markets[location_id].items():
            commodity_data = COMMODITIES[commodity_id]

            if category_filter and commodity_data["category"] != category_filter:
                continue

            overview.append({
                "id": commodity_id,
                "name": commodity_data["name"],
                "description": commodity_data["description"],
                "category": commodity_data["category"],
                "buy_price": self.get_price(location_id, commodity_id, is_buying=True),
                "sell_price": self.get_price(location_id, commodity_id, is_buying=False),
                "stock": market_data["stock"],
                "supply": market_data["supply_level"],
                "demand": market_data["demand_level"],
                "volume": commodity_data["volume"],
            })

        return sorted(overview, key=lambda x: x["name"])

    def get_best_trade_routes(self) -> List[Dict]:
        """Find profitable trading opportunities between locations"""
        routes = []

        locations = list(self.markets.keys())
        for commodity_id in COMMODITIES:
            best_buy_location = None
            best_buy_price = float('inf')
            best_sell_location = None
            best_sell_price = 0

            for location_id in locations:
                if commodity_id in self.markets[location_id]:
                    buy_price = self.get_price(location_id, commodity_id, is_buying=True)
                    sell_price = self.get_price(location_id, commodity_id, is_buying=False)

                    if sell_price < best_buy_price:
                        best_buy_price = sell_price
                        best_buy_location = location_id

                    if buy_price > best_sell_price:
                        best_sell_price = buy_price
                        best_sell_location = location_id

            if best_buy_location and best_sell_location and best_buy_location != best_sell_location:
                profit_per_unit = best_sell_price - best_buy_price
                if profit_per_unit > 0:
                    routes.append({
                        "commodity": COMMODITIES[commodity_id]["name"],
                        "commodity_id": commodity_id,
                        "buy_at": best_buy_location,
                        "buy_price": best_buy_price,
                        "sell_at": best_sell_location,
                        "sell_price": best_sell_price,
                        "profit": profit_per_unit,
                        "profit_margin": (profit_per_unit / best_buy_price) * 100
                    })

        return sorted(routes, key=lambda x: x["profit"], reverse=True)[:10]

    def to_dict(self) -> Dict:
        """Serialize market state for saving"""
        return {
            "markets": self.markets,
            "transaction_history": self.transaction_history[-100:],  # Keep last 100
            "active_events": self.active_events,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'CommodityMarket':
        """Load market state from save"""
        market = cls()
        market.markets = data.get("markets", {})
        market.transaction_history = data.get("transaction_history", [])
        market.active_events = data.get("active_events", [])
        return market


# Example usage
if __name__ == "__main__":
    # Test the market system
    market = CommodityMarket()

    # Get overview for a location
    overview = market.get_market_overview("nexus_prime", "food")
    print("Food commodities at Nexus Prime:")
    for item in overview[:5]:
        print(f"  {item['name']}: Buy {item['buy_price']} CR | Sell {item['sell_price']} CR | Stock: {item['stock']}")

    # Test buying
    success, msg, cost = market.buy_commodity("nexus_prime", "protein_rations", 10)
    print(f"\nBuy test: {msg}")

    # Test selling
    success, msg, revenue = market.sell_commodity("nexus_prime", "protein_rations", 5)
    print(f"Sell test: {msg}")

    # Update markets
    market.update_markets(60.0)
    print("\nMarkets updated")

    # Find trade routes
    print("\nTop 5 trade routes:")
    for route in market.get_best_trade_routes()[:5]:
        print(f"  {route['commodity']}: Buy at {route['buy_at']} ({route['buy_price']} CR) → "
              f"Sell at {route['sell_at']} ({route['sell_price']} CR) = {route['profit']} CR profit ({route['profit_margin']:.1f}%)")
