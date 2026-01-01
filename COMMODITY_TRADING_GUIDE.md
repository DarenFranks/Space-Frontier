# Void Dominion - Commodity Trading System

## Overview

A complete commodity trading system with **122 unique commodities** across 12 categories. Prices fluctuate dynamically based on supply/demand, player actions, and market conditions.

## Commodity Categories (122 Total)

### 1. Food & Nutrition (15 items)
Basic survival necessities for colonists and crew.
- **Cheap**: Algae Paste (8 CR), Nutrient Paste (10 CR), Carb Blocks (12 CR)
- **Mid-Range**: Protein Rations (15 CR), Freeze-Dried Meals (20 CR), Grain Stores (22 CR)
- **Premium**: Hydroponic Vegetables (45 CR), Synthetic Meat (60 CR)
- **Luxury**: Coffee Substitute (35 CR), Honey Extract (55 CR), Preserved Fruits (30 CR)

**Market Behavior**: Stable prices, universal demand, essential at all colonies

### 2. Medical Supplies (15 items)
Healthcare and emergency treatment products.
- **Basic**: Bandages (15 CR), Painkillers (45 CR)
- **Advanced**: Antibiotics (80 CR), Blood Plasma (90 CR), Immunoboosters (65 CR)
- **Specialized**: Stim Packs (120 CR), Bio-Regen Gel (150 CR), Radiation Meds (175 CR)
- **High-Tech**: Nano Repair Bots (400 CR), Medical Scanners (300 CR), Cryogenic Fluid (250 CR)

**Market Behavior**: Moderate volatility, essential goods, prices spike during emergencies

### 3. Scientific Equipment (14 items)
Laboratory and research instruments.
- **Consumables**: Test Tubes (5 CR), Petri Dishes (20 CR), Specimen Slides (15 CR)
- **Equipment**: Pipettes (40 CR), Lab Chemicals (75 CR), Autoclave Supplies (85 CR)
- **Advanced**: Centrifuges (350 CR), Oscilloscopes (450 CR), Spectrometers (500 CR)
- **Premium**: Research Computers (600 CR), Microscopes (800 CR), DNA Sequencers (1,200 CR)

**Market Behavior**: Low volatility, specialized demand at research stations

### 4. Life Support (12 items)
Critical systems for survival in space.
- **Consumables**: Breathing Masks (35 CR), Oxygen Canisters (50 CR), Pressure Seals (75 CR)
- **Systems**: Water Filters (90 CR), Humidity Controllers (110 CR), CO2 Scrubbers (150 CR)
- **Advanced**: Thermal Regulators (180 CR), Air Recyclers (400 CR), Emergency EVA Suits (500 CR)
- **Critical**: Oxygen Generators (650 CR), Life Support Cores (1,000 CR)

**Market Behavior**: Stable supply, universal need, premium at remote outposts

### 5. Luxury Goods (13 items)
Non-essential high-value items for wealthy colonists.
- **Comfort**: Chocolate (120 CR), Premium Cigars (150 CR), Fine Wines (200 CR)
- **Fashion**: Exotic Perfumes (180 CR), Silk Fabrics (250 CR), Designer Clothing (300 CR)
- **Culture**: Rare Books (350 CR), Musical Instruments (400 CR), Artwork (800 CR)
- **Ultra-Luxury**: Exotic Pets (450 CR), Holographic Art (600 CR), Gemstones (1,000 CR)

**Market Behavior**: HIGH volatility, low demand at poor colonies, premium at wealthy stations

### 6. Research Materials (13 items)
Rare specimens and exotic matter for scientific study.
- **Common**: Geological Samples (250 CR), Atmospheric Samples (180 CR)
- **Uncommon**: Bio Samples (400 CR), Crystalline Formations (600 CR)
- **Rare**: Asteroid Cores (800 CR), Radiation Samples (900 CR), Nebula Dust (1,200 CR)
- **Very Rare**: Exotic Isotopes (1,500 CR), Stellar Samples (2,000 CR)
- **Ultra-Rare**: Dark Matter Traces (3,500 CR), Antimatter Samples (4,000 CR), Alien Artifacts (5,000 CR)

**Market Behavior**: High volatility, research stations pay premium, rare availability

### 7. Technology & Electronics (10 items)
Computing and advanced technology products.
- **Components**: Power Cells (80 CR), Memory Chips (100 CR)
- **Equipment**: Encryption Keys (250 CR), Holographic Displays (350 CR)
- **Advanced**: Sensor Packages (400 CR), Processors (500 CR), Communication Arrays (600 CR)
- **Premium**: Neural Interfaces (1,500 CR), AI Cores (2,000 CR), Gravity Generators (3,000 CR)

**Market Behavior**: Moderate volatility, high demand at tech hubs

### 8. Energy Products (6 items)
Fuel and power storage for ships and stations.
- **Chemical**: Hydrogen Fuel (60 CR)
- **Storage**: Thermal Cores (150 CR), Fusion Pellets (200 CR), Plasma Batteries (300 CR)
- **Advanced**: Solar Arrays (800 CR)
- **Exotic**: Antimatter Cells (5,000 CR)

**Market Behavior**: Price spikes based on local energy needs

### 9. Textiles & Materials (6 items)
Fabrics and construction materials.
- **Basic**: Thermal Blankets (25 CR), Rope & Cables (30 CR), Insulation Foam (45 CR)
- **Advanced**: Protective Clothing (90 CR), Carbon Fiber (120 CR), Smart Fabrics (200 CR)

**Market Behavior**: Stable, industrial demand

### 10. Entertainment & Culture (6 items)
Digital and physical entertainment products.
- **Digital**: Digital Books (20 CR), Board Games (40 CR), Music Libraries (60 CR)
- **Media**: Movie Databases (70 CR), VR Games (80 CR)
- **Physical**: Sports Equipment (100 CR)

**Market Behavior**: Moderate demand, higher at leisure stations

### 11. Agricultural (6 items)
Farming and crop production supplies.
- **Basic**: Fertilizers (35 CR), Soil Supplements (40 CR)
- **Seeds**: Seed Variety Packs (50 CR), Hydroponics Solution (55 CR)
- **Advanced**: Pest Control (65 CR), Growth Hormones (120 CR)

**Market Behavior**: Seasonal demand at agricultural colonies

### 12. Data & Information (6 items)
Digital information and intelligence.
- **Navigation**: Star Charts (150 CR), Cultural Databases (180 CR)
- **Research**: Research Papers (200 CR)
- **Commercial**: Market Intelligence (300 CR)
- **Classified**: Encrypted Data (500 CR), Military Schematics (1,000 CR)

**Market Behavior**: High volatility, value depends on buyer

---

## Market Mechanics

### Price Fluctuation

Prices change based on:
1. **Supply/Demand Ratio**
   - High demand + Low supply = High prices (up to 3x base)
   - Low demand + High supply = Low prices (down to 0.5x base)

2. **Player Actions**
   - Buying drives prices UP (+impact on demand)
   - Selling drives prices DOWN (+impact on supply)
   - Large transactions (100+ units) have bigger impact

3. **Market Volatility**
   - Each commodity has volatility rating (0.2 to 1.2)
   - Luxury goods most volatile (0.6-1.0)
   - Basic goods least volatile (0.2-0.3)

4. **Natural Drift**
   - Prices drift back toward equilibrium
   - Supply/demand rebalance at 10% per minute
   - Stock replenishes at 5% per minute

### Buy/Sell Spread

- **Buying from market**: Pay 110% of current price
- **Selling to market**: Receive 90% of current price
- **20% spread** = market profit margin

### Stock Limits

- Each location has limited stock (100-500 units per commodity)
- Market won't buy if oversupplied (stock at max)
- Stock replenishes over time

---

## Trading Strategies

### 1. Buy Low, Sell High
- Monitor prices across locations
- Buy where supply is high (low prices)
- Sell where demand is high (high prices)

### 2. Trade Routes
- Use `get_best_trade_routes()` to find profitable routes
- Example routes can yield 100%+ profit margins
- Consider travel time and fuel costs

### 3. Market Manipulation
- Buy large quantities to drive price up
- Sell to other markets at inflated prices
- Risk: Prices eventually stabilize

### 4. Speculation
- Buy luxury goods during low demand
- Hold until prices rise
- Sell during high demand periods

### 5. Arbitrage
- Exploit price differences between locations
- Quick trades minimize price impact
- Best with high-value, low-volume goods

---

## Integration with Game

### Requirements
1. **Location Service**: Markets only at locations with "market" service
2. **Cargo Space**: Limited by ship cargo capacity
3. **Credits**: Need funds to purchase commodities

### Game Engine Integration
```python
from commodity_market import CommodityMarket

# In GameEngine.__init__
self.commodity_market = CommodityMarket()

# In update loop
self.commodity_market.update_markets(time_delta)

# For trading
success, msg, cost = self.commodity_market.buy_commodity(location, commodity, qty)
```

### Save/Load
```python
# Save
save_data["commodity_market"] = self.commodity_market.to_dict()

# Load
self.commodity_market = CommodityMarket.from_dict(save_data["commodity_market"])
```

---

## Example Trade Routes

Based on initial market generation:

1. **Antimatter Cells**
   - Buy at Axiom Labs: 3,208 CR
   - Sell at Forge Station: 9,010 CR
   - Profit: **5,802 CR per unit (181% margin)**

2. **Alien Artifacts**
   - Buy at Neural Network: 3,073 CR
   - Sell at Titan Alpha: 7,832 CR
   - Profit: **4,759 CR per unit (155% margin)**

3. **Gravity Generators**
   - Buy at Meridian Gates: 1,599 CR
   - Sell at Synthesis Planet: 5,683 CR
   - Profit: **4,084 CR per unit (255% margin)**

4. **Dark Matter Traces**
   - Buy at Titan Alpha: 2,123 CR
   - Sell at Neural Network: 6,183 CR
   - Profit: **4,060 CR per unit (191% margin)**

5. **Luxury Goods (Stable Income)**
   - Buy Fine Wines at production colony: ~150 CR
   - Sell at wealthy station: ~250 CR
   - Lower profit but consistent demand

---

## Market Events (Future Feature)

Planned dynamic events that affect prices:
- **Plague Outbreak**: Medical supplies spike 200%
- **Food Shortage**: Food prices increase 150%
- **Scientific Discovery**: Research materials surge
- **War**: Military schematics, weapons premium
- **Trade Blockade**: All goods scarce at affected location
- **Resource Boom**: Specific commodities plummet

---

## File Structure

- `data.py`: COMMODITIES and COMMODITY_CATEGORIES dictionaries
- `commodity_market.py`: CommodityMarket class with all trading logic
- `COMMODITY_TRADING_GUIDE.md`: This documentation

---

*Generated: 2025-11-06*
*Total Commodities: 122*
*Categories: 12*
