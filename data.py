"""
Game Data - EXPANDED VERSION
All content definitions with 8 ship types, 7 tiers, raw/refined resources, manufacturing, and more
"""

# ============= REFINING YIELD RANGES =============
# RNG-based refining yields based on rarity
# Less rare = more refined yield, More rare = less refined yield
REFINING_YIELD_RANGES = {
    "common": (0.80, 0.95),       # 80-95% yield
    "uncommon": (0.70, 0.85),     # 70-85% yield
    "rare": (0.60, 0.75),         # 60-75% yield
    "very_rare": (0.55, 0.65),    # 55-65% yield
    "legendary": (0.50, 0.60)     # 50-60% yield
}

# ============= RAW RESOURCES (Found in Asteroid Belts) =============
RAW_RESOURCES = {
    "raw_voltium": {
        "name": "Raw Voltium Ore",
        "description": "Unprocessed conductive crystalline material",
        "base_price": 100,
        "volume": 1.0,
        "rarity": "common",
        "mining_tier": 1,  # Basic ore - T1 laser
        "refines_to": "voltium",
        "refine_ratio": 0.7  # 10 raw = 7 refined
    },
    "raw_nexium": {
        "name": "Raw Nexium Gas",
        "description": "Unrefined exotic gas",
        "base_price": 600,
        "volume": 2.0,
        "rarity": "uncommon",
        "mining_tier": 1,  # Basic ore - T1 laser
        "refines_to": "nexium",
        "refine_ratio": 0.6
    },
    "raw_chronite": {
        "name": "Raw Chronite Crystal",
        "description": "Unprocessed time-dilated crystal",
        "base_price": 4000,
        "volume": 0.5,
        "rarity": "rare",
        "mining_tier": 2,  # Mid-tier ore - T2 laser
        "refines_to": "chronite",
        "refine_ratio": 0.5
    },
    "raw_titanite": {
        "name": "Raw Titanite Ore",
        "description": "Heavy metallic ore for hull plating",
        "base_price": 200,
        "volume": 3.0,
        "rarity": "common",
        "mining_tier": 1,  # Basic ore - T1 laser
        "refines_to": "titanite",
        "refine_ratio": 0.8
    },
    "raw_synthcrystal": {
        "name": "Raw Synthcrystal",
        "description": "Unprocessed programmable crystal",
        "base_price": 10000,
        "volume": 0.1,
        "rarity": "very_rare",
        "mining_tier": 3,  # Advanced ore - T3 laser
        "refines_to": "synthcrystal",
        "refine_ratio": 0.4
    },
    "raw_darkwater": {
        "name": "Raw Darkwater",
        "description": "Unrefined void anomaly fluid",
        "base_price": 30000,
        "volume": 0.5,
        "rarity": "legendary",
        "mining_tier": 3,  # Advanced ore - T3 laser
        "refines_to": "darkwater",
        "refine_ratio": 0.3
    },
    "raw_neuralfiber": {
        "name": "Raw Neural Fiber",
        "description": "Unprocessed organic computing substrate",
        "base_price": 2500,
        "volume": 0.2,
        "rarity": "rare",
        "mining_tier": 2,  # Mid-tier ore - T2 laser
        "refines_to": "neural_fiber",
        "refine_ratio": 0.6
    },
    "raw_quantum_dust": {
        "name": "Raw Quantum Dust",
        "description": "Unstable quantum particles",
        "base_price": 12000,
        "volume": 0.1,
        "rarity": "very_rare",
        "mining_tier": 3,  # Advanced ore - T3 laser
        "refines_to": "quantum_dust",
        "refine_ratio": 0.5
    }
}

# ============= REFINED RESOURCES (Processed at Refineries) =============
# Refined resources are significantly more compact than raw ore
# Volume reduction makes refining worthwhile for cargo management
REFINED_RESOURCES = {
    "voltium": {
        "name": "Voltium Ingot",
        "description": "Refined conductive material",
        "base_price": 200,
        "volume": 0.4,  # 40% of raw (1.0 → 0.4) - common
        "rarity": "common"
    },
    "nexium": {
        "name": "Nexium Fuel",
        "description": "Refined exotic propulsion fuel",
        "base_price": 1200,
        "volume": 0.7,  # 35% of raw (2.0 → 0.7) - uncommon
        "rarity": "uncommon"
    },
    "chronite": {
        "name": "Chronite Wafer",
        "description": "Processed quantum computing crystal",
        "base_price": 10000,
        "volume": 0.15,  # 30% of raw (0.5 → 0.15) - rare
        "rarity": "rare"
    },
    "titanite": {
        "name": "Titanite Alloy",
        "description": "Processed hull material",
        "base_price": 350,
        "volume": 1.2,  # 40% of raw (3.0 → 1.2) - common
        "rarity": "common"
    },
    "synthcrystal": {
        "name": "Synthcrystal Matrix",
        "description": "Refined programmable matter",
        "base_price": 22000,
        "volume": 0.025,  # 25% of raw (0.1 → 0.025) - very rare
        "rarity": "very_rare"
    },
    "darkwater": {
        "name": "Darkwater Essence",
        "description": "Stabilized void anomaly fluid",
        "base_price": 65000,
        "volume": 0.1,  # 20% of raw (0.5 → 0.1) - legendary
        "rarity": "legendary"
    },
    "neural_fiber": {
        "name": "Neural Fiber Mesh",
        "description": "Processed organic computing material",
        "base_price": 5000,
        "volume": 0.06,  # 30% of raw (0.2 → 0.06) - rare
        "rarity": "rare"
    },
    "quantum_dust": {
        "name": "Stabilized Quantum Dust",
        "description": "Stable quantum particles",
        "base_price": 30000,
        "volume": 0.025,  # 25% of raw (0.1 → 0.025) - very rare
        "rarity": "very_rare"
    },
    # Manufacturing components
    "plasmic_fuel": {
        "name": "Plasmic Fuel Cell",
        "description": "Standard energy source",
        "base_price": 50,
        "volume": 1.0,
        "rarity": "common"
    }
}

# Combine all resources
RESOURCES = {**RAW_RESOURCES, **REFINED_RESOURCES}

# ============= SHIP TYPES (8 types, 7 tiers each) =============

SHIP_TYPES = ["scout", "fighter", "hauler", "cruiser", "destroyer", "battleship", "carrier", "refinery"]
SHIP_TIERS = ["mk1", "mk2", "mk3", "mk4", "mk5", "mk6", "mk7"]

def generate_ship_classes():
    """Generate all 96 ship classes (8 types × 4 variants × 3 tiers)"""
    ships = {}

    # Base stats for each ship type
    ship_types = {
        "scout": {
            "hull_hp": 500,
            "shield": 300,
            "armor": 50,
            "speed": 180,
            "cargo": 200,
            "weapon_slots": 1,      # Starter: 1 weapon
            "defense_slots": 1,     # 1 shield
            "utility_slots": 2,     # 2 utility (scanner + miner)
            "engine_slots": 1,      # 1 engine (total: 5 slots)
            "cost_base": 100000
        },
        "fighter": {
            "hull_hp": 800,
            "shield": 500,
            "armor": 100,
            "speed": 160,
            "cargo": 150,
            "weapon_slots": 2,      # Combat focused
            "defense_slots": 1,     # Light defense
            "utility_slots": 1,     # Minimal utility
            "engine_slots": 1,      # 1 engine (total: 5 slots)
            "cost_base": 250000
        },
        "hauler": {
            "hull_hp": 2000,
            "shield": 400,
            "armor": 200,
            "speed": 60,
            "cargo": 3000,
            "weapon_slots": 1,      # Minimal weapons
            "defense_slots": 2,     # Better defense
            "utility_slots": 3,     # Utility focused
            "engine_slots": 1,      # 1 engine (total: 7 slots)
            "cost_base": 400000
        },
        "cruiser": {
            "hull_hp": 3000,
            "shield": 1500,
            "armor": 300,
            "speed": 100,
            "cargo": 500,
            "weapon_slots": 3,      # Balanced mid-game
            "defense_slots": 2,     # Decent defense
            "utility_slots": 2,     # Some utility
            "engine_slots": 1,      # 1 engine (total: 8 slots)
            "cost_base": 1200000
        },
        "destroyer": {
            "hull_hp": 5000,
            "shield": 2000,
            "armor": 500,
            "speed": 80,
            "cargo": 800,
            "weapon_slots": 4,      # Heavy weapons
            "defense_slots": 3,     # Strong defense
            "utility_slots": 2,     # Some utility
            "engine_slots": 2,      # 2 engines (total: 11 slots)
            "cost_base": 2500000
        },
        "battleship": {
            "hull_hp": 10000,
            "shield": 4000,
            "armor": 800,
            "speed": 60,
            "cargo": 1200,
            "weapon_slots": 6,      # Maximum firepower
            "defense_slots": 4,     # Heavy defense
            "utility_slots": 3,     # Moderate utility
            "engine_slots": 2,      # 2 engines (total: 15 slots)
            "cost_base": 6000000
        },
        "carrier": {
            "hull_hp": 7000,
            "shield": 3000,
            "armor": 600,
            "speed": 70,
            "cargo": 2000,
            "weapon_slots": 3,      # Moderate weapons
            "defense_slots": 4,     # Strong defense
            "utility_slots": 6,     # Support/utility focused
            "engine_slots": 2,      # 2 engines (total: 15 slots)
            "cost_base": 5000000
        },
        "refinery": {
            "hull_hp": 4000,
            "shield": 1000,
            "armor": 400,
            "speed": 50,
            "cargo": 4000,
            "weapon_slots": 1,      # Minimal weapons
            "defense_slots": 3,     # Moderate defense
            "utility_slots": 8,     # Maximum utility/industry
            "engine_slots": 1,      # 1 engine (total: 13 slots)
            "cost_base": 8000000
        },
        "mothership": {
            "hull_hp": 15000,
            "shield": 5000,
            "armor": 1000,
            "speed": 40,
            "cargo": 6000,
            "weapon_slots": 4,      # Moderate weapons for defense
            "defense_slots": 6,     # Heavy defense
            "utility_slots": 10,    # Maximum utility (refining + more)
            "engine_slots": 2,      # 2 engines (total: 22 slots)
            "cost_base": 12000000   # Most expensive ship
        }
    }

    # Variant multipliers (affects all stats except cargo)
    variants = {
        "standard": {
            "multiplier": 1.0,
            "cost_mult": 1.0,
            "level": 1,
            "name_suffix": "Standard"
        },
        "advanced": {
            "multiplier": 1.2,
            "cost_mult": 1.3,
            "level": 5,
            "name_suffix": "Advanced"
        },
        "elite": {
            "multiplier": 1.5,
            "cost_mult": 1.7,
            "level": 10,
            "name_suffix": "Elite"
        },
        "specialized": {
            "multiplier": 1.8,
            "cost_mult": 2.2,
            "level": 15,
            "name_suffix": "Specialized"
        }
    }

    # Tier multipliers (affects everything)
    tiers = {
        "mk1": {"tier_mult": 1.0, "tier_level": 0, "tier_num": 1, "tier_name": "MK1"},
        "mk2": {"tier_mult": 1.8, "tier_level": 7, "tier_num": 2, "tier_name": "MK2"},
        "mk3": {"tier_mult": 3.0, "tier_level": 14, "tier_num": 3, "tier_name": "MK3"}
    }

    # Generate 96 ships: 8 types × 4 variants × 3 tiers
    for ship_type, base_stats in ship_types.items():
        for variant_key, variant_data in variants.items():
            for tier_key, tier_data in tiers.items():
                ship_id = f"{ship_type}_{variant_key}_{tier_key}"

                # Calculate final stats
                var_mult = variant_data["multiplier"]
                tier_mult = tier_data["tier_mult"]
                combined_mult = var_mult * tier_mult

                # Calculate level requirement
                base_level = variant_data["level"] + tier_data["tier_level"]

                # Create ship entry
                ships[ship_id] = {
                    "name": f"{variant_data['name_suffix']} {ship_type.capitalize()} {tier_data['tier_name']}",
                    "description": f"{variant_data['name_suffix']} {ship_type} - Tier {tier_data['tier_num']}",
                    "cost": int(base_stats["cost_base"] * variant_data["cost_mult"] * tier_mult),
                    "hull_hp": int(base_stats["hull_hp"] * combined_mult),
                    "shield_capacity": int(base_stats["shield"] * combined_mult),
                    "armor_rating": int(base_stats["armor"] * combined_mult),
                    "cargo_capacity": int(base_stats["cargo"] * tier_mult),  # Cargo only scales with tier
                    "base_speed": int(base_stats["speed"] * (1 + (var_mult - 1) * 0.3)),  # Speed scales with variant only
                    "module_slots": {
                        "weapon": base_stats["weapon_slots"],
                        "defense": base_stats["defense_slots"],
                        "utility": base_stats["utility_slots"],
                        "engine": base_stats["engine_slots"]
                    },
                    "class_type": ship_type,
                    "variant": variant_key,
                    "tier": tier_key,
                    "tier_num": tier_data["tier_num"],
                    "level_requirement": base_level
                }

    return ships

VESSEL_CLASSES = generate_ship_classes()

# Starting vessel
STARTING_VESSEL = "scout_standard_mk1"

# ============= SHIP-SPECIFIC COMPONENTS =============
SHIP_COMPONENTS = {
    "battleship_computer_system_t1": {
        "name": "Battleship Computer System T1",
        "type": "computer_system",
        "ship_type": "battleship",
        "tier": 1,
        "description": "Battleship-class AI processor - Tier 1",
        "cost": 127000,
        "manufacturing_cost": 88900,
        "level_requirement": 1,
        "computer_bonus": 1.0,
    },
    "battleship_computer_system_t2": {
        "name": "Battleship Computer System T2",
        "type": "computer_system",
        "ship_type": "battleship",
        "tier": 2,
        "description": "Battleship-class AI processor - Tier 2",
        "cost": 381000,
        "manufacturing_cost": 266700,
        "level_requirement": 8,
        "computer_bonus": 2.0,
    },
    "battleship_computer_system_t3": {
        "name": "Battleship Computer System T3",
        "type": "computer_system",
        "ship_type": "battleship",
        "tier": 3,
        "description": "Battleship-class AI processor - Tier 3",
        "cost": 1143000,
        "manufacturing_cost": 800100,
        "level_requirement": 15,
        "computer_bonus": 3.0,
    },
    "battleship_hull_frame_t1": {
        "name": "Battleship Hull Frame T1",
        "type": "hull_frame",
        "ship_type": "battleship",
        "tier": 1,
        "description": "Battleship-class hull structure - Tier 1",
        "cost": 127000,
        "manufacturing_cost": 88900,
        "level_requirement": 1,
        "hull_bonus": 1.0,
    },
    "battleship_hull_frame_t2": {
        "name": "Battleship Hull Frame T2",
        "type": "hull_frame",
        "ship_type": "battleship",
        "tier": 2,
        "description": "Battleship-class hull structure - Tier 2",
        "cost": 381000,
        "manufacturing_cost": 266700,
        "level_requirement": 8,
        "hull_bonus": 2.0,
    },
    "battleship_hull_frame_t3": {
        "name": "Battleship Hull Frame T3",
        "type": "hull_frame",
        "ship_type": "battleship",
        "tier": 3,
        "description": "Battleship-class hull structure - Tier 3",
        "cost": 1143000,
        "manufacturing_cost": 800100,
        "level_requirement": 15,
        "hull_bonus": 3.0,
    },
    "battleship_life_support_t1": {
        "name": "Battleship Life Support T1",
        "type": "life_support",
        "ship_type": "battleship",
        "tier": 1,
        "description": "Battleship-class crew systems - Tier 1",
        "cost": 127000,
        "manufacturing_cost": 88900,
        "level_requirement": 1,
        "life_support_bonus": 1.0,
    },
    "battleship_life_support_t2": {
        "name": "Battleship Life Support T2",
        "type": "life_support",
        "ship_type": "battleship",
        "tier": 2,
        "description": "Battleship-class crew systems - Tier 2",
        "cost": 381000,
        "manufacturing_cost": 266700,
        "level_requirement": 8,
        "life_support_bonus": 2.0,
    },
    "battleship_life_support_t3": {
        "name": "Battleship Life Support T3",
        "type": "life_support",
        "ship_type": "battleship",
        "tier": 3,
        "description": "Battleship-class crew systems - Tier 3",
        "cost": 1143000,
        "manufacturing_cost": 800100,
        "level_requirement": 15,
        "life_support_bonus": 3.0,
    },
    "battleship_power_core_t1": {
        "name": "Battleship Power Core T1",
        "type": "power_core",
        "ship_type": "battleship",
        "tier": 1,
        "description": "Battleship-class energy generation - Tier 1",
        "cost": 127000,
        "manufacturing_cost": 88900,
        "level_requirement": 1,
        "power_bonus": 1.0,
    },
    "battleship_power_core_t2": {
        "name": "Battleship Power Core T2",
        "type": "power_core",
        "ship_type": "battleship",
        "tier": 2,
        "description": "Battleship-class energy generation - Tier 2",
        "cost": 381000,
        "manufacturing_cost": 266700,
        "level_requirement": 8,
        "power_bonus": 2.0,
    },
    "battleship_power_core_t3": {
        "name": "Battleship Power Core T3",
        "type": "power_core",
        "ship_type": "battleship",
        "tier": 3,
        "description": "Battleship-class energy generation - Tier 3",
        "cost": 1143000,
        "manufacturing_cost": 800100,
        "level_requirement": 15,
        "power_bonus": 3.0,
    },
    "battleship_sensor_suite_t1": {
        "name": "Battleship Sensor Suite T1",
        "type": "sensor_suite",
        "ship_type": "battleship",
        "tier": 1,
        "description": "Battleship-class detection system - Tier 1",
        "cost": 127000,
        "manufacturing_cost": 88900,
        "level_requirement": 1,
        "sensor_bonus": 1.0,
    },
    "battleship_sensor_suite_t2": {
        "name": "Battleship Sensor Suite T2",
        "type": "sensor_suite",
        "ship_type": "battleship",
        "tier": 2,
        "description": "Battleship-class detection system - Tier 2",
        "cost": 381000,
        "manufacturing_cost": 266700,
        "level_requirement": 8,
        "sensor_bonus": 2.0,
    },
    "battleship_sensor_suite_t3": {
        "name": "Battleship Sensor Suite T3",
        "type": "sensor_suite",
        "ship_type": "battleship",
        "tier": 3,
        "description": "Battleship-class detection system - Tier 3",
        "cost": 1143000,
        "manufacturing_cost": 800100,
        "level_requirement": 15,
        "sensor_bonus": 3.0,
    },
    "battleship_shield_generator_t1": {
        "name": "Battleship Shield Generator T1",
        "type": "shield_generator",
        "ship_type": "battleship",
        "tier": 1,
        "description": "Battleship-class defensive shielding - Tier 1",
        "cost": 127000,
        "manufacturing_cost": 88900,
        "level_requirement": 1,
        "shield_bonus": 1.0,
    },
    "battleship_shield_generator_t2": {
        "name": "Battleship Shield Generator T2",
        "type": "shield_generator",
        "ship_type": "battleship",
        "tier": 2,
        "description": "Battleship-class defensive shielding - Tier 2",
        "cost": 381000,
        "manufacturing_cost": 266700,
        "level_requirement": 8,
        "shield_bonus": 2.0,
    },
    "battleship_shield_generator_t3": {
        "name": "Battleship Shield Generator T3",
        "type": "shield_generator",
        "ship_type": "battleship",
        "tier": 3,
        "description": "Battleship-class defensive shielding - Tier 3",
        "cost": 1143000,
        "manufacturing_cost": 800100,
        "level_requirement": 15,
        "shield_bonus": 3.0,
    },
    "battleship_thruster_array_t1": {
        "name": "Battleship Thruster Array T1",
        "type": "thruster_array",
        "ship_type": "battleship",
        "tier": 1,
        "description": "Battleship-class propulsion system - Tier 1",
        "cost": 127000,
        "manufacturing_cost": 88900,
        "level_requirement": 1,
        "speed_bonus": 1.0,
    },
    "battleship_thruster_array_t2": {
        "name": "Battleship Thruster Array T2",
        "type": "thruster_array",
        "ship_type": "battleship",
        "tier": 2,
        "description": "Battleship-class propulsion system - Tier 2",
        "cost": 381000,
        "manufacturing_cost": 266700,
        "level_requirement": 8,
        "speed_bonus": 2.0,
    },
    "battleship_thruster_array_t3": {
        "name": "Battleship Thruster Array T3",
        "type": "thruster_array",
        "ship_type": "battleship",
        "tier": 3,
        "description": "Battleship-class propulsion system - Tier 3",
        "cost": 1143000,
        "manufacturing_cost": 800100,
        "level_requirement": 15,
        "speed_bonus": 3.0,
    },
    "battleship_weapon_mount_t1": {
        "name": "Battleship Weapon Mount T1",
        "type": "weapon_mount",
        "ship_type": "battleship",
        "tier": 1,
        "description": "Battleship-class weapon hardpoint - Tier 1",
        "cost": 127000,
        "manufacturing_cost": 88900,
        "level_requirement": 1,
        "weapon_bonus": 1.0,
    },
    "battleship_weapon_mount_t2": {
        "name": "Battleship Weapon Mount T2",
        "type": "weapon_mount",
        "ship_type": "battleship",
        "tier": 2,
        "description": "Battleship-class weapon hardpoint - Tier 2",
        "cost": 381000,
        "manufacturing_cost": 266700,
        "level_requirement": 8,
        "weapon_bonus": 2.0,
    },
    "battleship_weapon_mount_t3": {
        "name": "Battleship Weapon Mount T3",
        "type": "weapon_mount",
        "ship_type": "battleship",
        "tier": 3,
        "description": "Battleship-class weapon hardpoint - Tier 3",
        "cost": 1143000,
        "manufacturing_cost": 800100,
        "level_requirement": 15,
        "weapon_bonus": 3.0,
    },
    "carrier_computer_system_t1": {
        "name": "Carrier Computer System T1",
        "type": "computer_system",
        "ship_type": "carrier",
        "tier": 1,
        "description": "Carrier-class AI processor - Tier 1",
        "cost": 134000,
        "manufacturing_cost": 93800,
        "level_requirement": 1,
        "computer_bonus": 1.0,
    },
    "carrier_computer_system_t2": {
        "name": "Carrier Computer System T2",
        "type": "computer_system",
        "ship_type": "carrier",
        "tier": 2,
        "description": "Carrier-class AI processor - Tier 2",
        "cost": 402000,
        "manufacturing_cost": 281400,
        "level_requirement": 8,
        "computer_bonus": 2.0,
    },
    "carrier_computer_system_t3": {
        "name": "Carrier Computer System T3",
        "type": "computer_system",
        "ship_type": "carrier",
        "tier": 3,
        "description": "Carrier-class AI processor - Tier 3",
        "cost": 1206000,
        "manufacturing_cost": 844200,
        "level_requirement": 15,
        "computer_bonus": 3.0,
    },
    "carrier_hull_frame_t1": {
        "name": "Carrier Hull Frame T1",
        "type": "hull_frame",
        "ship_type": "carrier",
        "tier": 1,
        "description": "Carrier-class hull structure - Tier 1",
        "cost": 134000,
        "manufacturing_cost": 93800,
        "level_requirement": 1,
        "hull_bonus": 1.0,
    },
    "carrier_hull_frame_t2": {
        "name": "Carrier Hull Frame T2",
        "type": "hull_frame",
        "ship_type": "carrier",
        "tier": 2,
        "description": "Carrier-class hull structure - Tier 2",
        "cost": 402000,
        "manufacturing_cost": 281400,
        "level_requirement": 8,
        "hull_bonus": 2.0,
    },
    "carrier_hull_frame_t3": {
        "name": "Carrier Hull Frame T3",
        "type": "hull_frame",
        "ship_type": "carrier",
        "tier": 3,
        "description": "Carrier-class hull structure - Tier 3",
        "cost": 1206000,
        "manufacturing_cost": 844200,
        "level_requirement": 15,
        "hull_bonus": 3.0,
    },
    "carrier_life_support_t1": {
        "name": "Carrier Life Support T1",
        "type": "life_support",
        "ship_type": "carrier",
        "tier": 1,
        "description": "Carrier-class crew systems - Tier 1",
        "cost": 134000,
        "manufacturing_cost": 93800,
        "level_requirement": 1,
        "life_support_bonus": 1.0,
    },
    "carrier_life_support_t2": {
        "name": "Carrier Life Support T2",
        "type": "life_support",
        "ship_type": "carrier",
        "tier": 2,
        "description": "Carrier-class crew systems - Tier 2",
        "cost": 402000,
        "manufacturing_cost": 281400,
        "level_requirement": 8,
        "life_support_bonus": 2.0,
    },
    "carrier_life_support_t3": {
        "name": "Carrier Life Support T3",
        "type": "life_support",
        "ship_type": "carrier",
        "tier": 3,
        "description": "Carrier-class crew systems - Tier 3",
        "cost": 1206000,
        "manufacturing_cost": 844200,
        "level_requirement": 15,
        "life_support_bonus": 3.0,
    },
    "carrier_power_core_t1": {
        "name": "Carrier Power Core T1",
        "type": "power_core",
        "ship_type": "carrier",
        "tier": 1,
        "description": "Carrier-class energy generation - Tier 1",
        "cost": 134000,
        "manufacturing_cost": 93800,
        "level_requirement": 1,
        "power_bonus": 1.0,
    },
    "carrier_power_core_t2": {
        "name": "Carrier Power Core T2",
        "type": "power_core",
        "ship_type": "carrier",
        "tier": 2,
        "description": "Carrier-class energy generation - Tier 2",
        "cost": 402000,
        "manufacturing_cost": 281400,
        "level_requirement": 8,
        "power_bonus": 2.0,
    },
    "carrier_power_core_t3": {
        "name": "Carrier Power Core T3",
        "type": "power_core",
        "ship_type": "carrier",
        "tier": 3,
        "description": "Carrier-class energy generation - Tier 3",
        "cost": 1206000,
        "manufacturing_cost": 844200,
        "level_requirement": 15,
        "power_bonus": 3.0,
    },
    "carrier_sensor_suite_t1": {
        "name": "Carrier Sensor Suite T1",
        "type": "sensor_suite",
        "ship_type": "carrier",
        "tier": 1,
        "description": "Carrier-class detection system - Tier 1",
        "cost": 134000,
        "manufacturing_cost": 93800,
        "level_requirement": 1,
        "sensor_bonus": 1.0,
    },
    "carrier_sensor_suite_t2": {
        "name": "Carrier Sensor Suite T2",
        "type": "sensor_suite",
        "ship_type": "carrier",
        "tier": 2,
        "description": "Carrier-class detection system - Tier 2",
        "cost": 402000,
        "manufacturing_cost": 281400,
        "level_requirement": 8,
        "sensor_bonus": 2.0,
    },
    "carrier_sensor_suite_t3": {
        "name": "Carrier Sensor Suite T3",
        "type": "sensor_suite",
        "ship_type": "carrier",
        "tier": 3,
        "description": "Carrier-class detection system - Tier 3",
        "cost": 1206000,
        "manufacturing_cost": 844200,
        "level_requirement": 15,
        "sensor_bonus": 3.0,
    },
    "carrier_shield_generator_t1": {
        "name": "Carrier Shield Generator T1",
        "type": "shield_generator",
        "ship_type": "carrier",
        "tier": 1,
        "description": "Carrier-class defensive shielding - Tier 1",
        "cost": 134000,
        "manufacturing_cost": 93800,
        "level_requirement": 1,
        "shield_bonus": 1.0,
    },
    "carrier_shield_generator_t2": {
        "name": "Carrier Shield Generator T2",
        "type": "shield_generator",
        "ship_type": "carrier",
        "tier": 2,
        "description": "Carrier-class defensive shielding - Tier 2",
        "cost": 402000,
        "manufacturing_cost": 281400,
        "level_requirement": 8,
        "shield_bonus": 2.0,
    },
    "carrier_shield_generator_t3": {
        "name": "Carrier Shield Generator T3",
        "type": "shield_generator",
        "ship_type": "carrier",
        "tier": 3,
        "description": "Carrier-class defensive shielding - Tier 3",
        "cost": 1206000,
        "manufacturing_cost": 844200,
        "level_requirement": 15,
        "shield_bonus": 3.0,
    },
    "carrier_thruster_array_t1": {
        "name": "Carrier Thruster Array T1",
        "type": "thruster_array",
        "ship_type": "carrier",
        "tier": 1,
        "description": "Carrier-class propulsion system - Tier 1",
        "cost": 134000,
        "manufacturing_cost": 93800,
        "level_requirement": 1,
        "speed_bonus": 1.0,
    },
    "carrier_thruster_array_t2": {
        "name": "Carrier Thruster Array T2",
        "type": "thruster_array",
        "ship_type": "carrier",
        "tier": 2,
        "description": "Carrier-class propulsion system - Tier 2",
        "cost": 402000,
        "manufacturing_cost": 281400,
        "level_requirement": 8,
        "speed_bonus": 2.0,
    },
    "carrier_thruster_array_t3": {
        "name": "Carrier Thruster Array T3",
        "type": "thruster_array",
        "ship_type": "carrier",
        "tier": 3,
        "description": "Carrier-class propulsion system - Tier 3",
        "cost": 1206000,
        "manufacturing_cost": 844200,
        "level_requirement": 15,
        "speed_bonus": 3.0,
    },
    "carrier_weapon_mount_t1": {
        "name": "Carrier Weapon Mount T1",
        "type": "weapon_mount",
        "ship_type": "carrier",
        "tier": 1,
        "description": "Carrier-class weapon hardpoint - Tier 1",
        "cost": 134000,
        "manufacturing_cost": 93800,
        "level_requirement": 1,
        "weapon_bonus": 1.0,
    },
    "carrier_weapon_mount_t2": {
        "name": "Carrier Weapon Mount T2",
        "type": "weapon_mount",
        "ship_type": "carrier",
        "tier": 2,
        "description": "Carrier-class weapon hardpoint - Tier 2",
        "cost": 402000,
        "manufacturing_cost": 281400,
        "level_requirement": 8,
        "weapon_bonus": 2.0,
    },
    "carrier_weapon_mount_t3": {
        "name": "Carrier Weapon Mount T3",
        "type": "weapon_mount",
        "ship_type": "carrier",
        "tier": 3,
        "description": "Carrier-class weapon hardpoint - Tier 3",
        "cost": 1206000,
        "manufacturing_cost": 844200,
        "level_requirement": 15,
        "weapon_bonus": 3.0,
    },
    "cruiser_computer_system_t1": {
        "name": "Cruiser Computer System T1",
        "type": "computer_system",
        "ship_type": "cruiser",
        "tier": 1,
        "description": "Cruiser-class AI processor - Tier 1",
        "cost": 30000,
        "manufacturing_cost": 21000,
        "level_requirement": 1,
        "computer_bonus": 1.0,
    },
    "cruiser_computer_system_t2": {
        "name": "Cruiser Computer System T2",
        "type": "computer_system",
        "ship_type": "cruiser",
        "tier": 2,
        "description": "Cruiser-class AI processor - Tier 2",
        "cost": 90000,
        "manufacturing_cost": 62999,
        "level_requirement": 8,
        "computer_bonus": 2.0,
    },
    "cruiser_computer_system_t3": {
        "name": "Cruiser Computer System T3",
        "type": "computer_system",
        "ship_type": "cruiser",
        "tier": 3,
        "description": "Cruiser-class AI processor - Tier 3",
        "cost": 270000,
        "manufacturing_cost": 189000,
        "level_requirement": 15,
        "computer_bonus": 3.0,
    },
    "cruiser_hull_frame_t1": {
        "name": "Cruiser Hull Frame T1",
        "type": "hull_frame",
        "ship_type": "cruiser",
        "tier": 1,
        "description": "Cruiser-class hull structure - Tier 1",
        "cost": 30000,
        "manufacturing_cost": 21000,
        "level_requirement": 1,
        "hull_bonus": 1.0,
    },
    "cruiser_hull_frame_t2": {
        "name": "Cruiser Hull Frame T2",
        "type": "hull_frame",
        "ship_type": "cruiser",
        "tier": 2,
        "description": "Cruiser-class hull structure - Tier 2",
        "cost": 90000,
        "manufacturing_cost": 62999,
        "level_requirement": 8,
        "hull_bonus": 2.0,
    },
    "cruiser_hull_frame_t3": {
        "name": "Cruiser Hull Frame T3",
        "type": "hull_frame",
        "ship_type": "cruiser",
        "tier": 3,
        "description": "Cruiser-class hull structure - Tier 3",
        "cost": 270000,
        "manufacturing_cost": 189000,
        "level_requirement": 15,
        "hull_bonus": 3.0,
    },
    "cruiser_life_support_t1": {
        "name": "Cruiser Life Support T1",
        "type": "life_support",
        "ship_type": "cruiser",
        "tier": 1,
        "description": "Cruiser-class crew systems - Tier 1",
        "cost": 30000,
        "manufacturing_cost": 21000,
        "level_requirement": 1,
        "life_support_bonus": 1.0,
    },
    "cruiser_life_support_t2": {
        "name": "Cruiser Life Support T2",
        "type": "life_support",
        "ship_type": "cruiser",
        "tier": 2,
        "description": "Cruiser-class crew systems - Tier 2",
        "cost": 90000,
        "manufacturing_cost": 62999,
        "level_requirement": 8,
        "life_support_bonus": 2.0,
    },
    "cruiser_life_support_t3": {
        "name": "Cruiser Life Support T3",
        "type": "life_support",
        "ship_type": "cruiser",
        "tier": 3,
        "description": "Cruiser-class crew systems - Tier 3",
        "cost": 270000,
        "manufacturing_cost": 189000,
        "level_requirement": 15,
        "life_support_bonus": 3.0,
    },
    "cruiser_power_core_t1": {
        "name": "Cruiser Power Core T1",
        "type": "power_core",
        "ship_type": "cruiser",
        "tier": 1,
        "description": "Cruiser-class energy generation - Tier 1",
        "cost": 30000,
        "manufacturing_cost": 21000,
        "level_requirement": 1,
        "power_bonus": 1.0,
    },
    "cruiser_power_core_t2": {
        "name": "Cruiser Power Core T2",
        "type": "power_core",
        "ship_type": "cruiser",
        "tier": 2,
        "description": "Cruiser-class energy generation - Tier 2",
        "cost": 90000,
        "manufacturing_cost": 62999,
        "level_requirement": 8,
        "power_bonus": 2.0,
    },
    "cruiser_power_core_t3": {
        "name": "Cruiser Power Core T3",
        "type": "power_core",
        "ship_type": "cruiser",
        "tier": 3,
        "description": "Cruiser-class energy generation - Tier 3",
        "cost": 270000,
        "manufacturing_cost": 189000,
        "level_requirement": 15,
        "power_bonus": 3.0,
    },
    "cruiser_sensor_suite_t1": {
        "name": "Cruiser Sensor Suite T1",
        "type": "sensor_suite",
        "ship_type": "cruiser",
        "tier": 1,
        "description": "Cruiser-class detection system - Tier 1",
        "cost": 30000,
        "manufacturing_cost": 21000,
        "level_requirement": 1,
        "sensor_bonus": 1.0,
    },
    "cruiser_sensor_suite_t2": {
        "name": "Cruiser Sensor Suite T2",
        "type": "sensor_suite",
        "ship_type": "cruiser",
        "tier": 2,
        "description": "Cruiser-class detection system - Tier 2",
        "cost": 90000,
        "manufacturing_cost": 62999,
        "level_requirement": 8,
        "sensor_bonus": 2.0,
    },
    "cruiser_sensor_suite_t3": {
        "name": "Cruiser Sensor Suite T3",
        "type": "sensor_suite",
        "ship_type": "cruiser",
        "tier": 3,
        "description": "Cruiser-class detection system - Tier 3",
        "cost": 270000,
        "manufacturing_cost": 189000,
        "level_requirement": 15,
        "sensor_bonus": 3.0,
    },
    "cruiser_shield_generator_t1": {
        "name": "Cruiser Shield Generator T1",
        "type": "shield_generator",
        "ship_type": "cruiser",
        "tier": 1,
        "description": "Cruiser-class defensive shielding - Tier 1",
        "cost": 30000,
        "manufacturing_cost": 21000,
        "level_requirement": 1,
        "shield_bonus": 1.0,
    },
    "cruiser_shield_generator_t2": {
        "name": "Cruiser Shield Generator T2",
        "type": "shield_generator",
        "ship_type": "cruiser",
        "tier": 2,
        "description": "Cruiser-class defensive shielding - Tier 2",
        "cost": 90000,
        "manufacturing_cost": 62999,
        "level_requirement": 8,
        "shield_bonus": 2.0,
    },
    "cruiser_shield_generator_t3": {
        "name": "Cruiser Shield Generator T3",
        "type": "shield_generator",
        "ship_type": "cruiser",
        "tier": 3,
        "description": "Cruiser-class defensive shielding - Tier 3",
        "cost": 270000,
        "manufacturing_cost": 189000,
        "level_requirement": 15,
        "shield_bonus": 3.0,
    },
    "cruiser_thruster_array_t1": {
        "name": "Cruiser Thruster Array T1",
        "type": "thruster_array",
        "ship_type": "cruiser",
        "tier": 1,
        "description": "Cruiser-class propulsion system - Tier 1",
        "cost": 30000,
        "manufacturing_cost": 21000,
        "level_requirement": 1,
        "speed_bonus": 1.0,
    },
    "cruiser_thruster_array_t2": {
        "name": "Cruiser Thruster Array T2",
        "type": "thruster_array",
        "ship_type": "cruiser",
        "tier": 2,
        "description": "Cruiser-class propulsion system - Tier 2",
        "cost": 90000,
        "manufacturing_cost": 62999,
        "level_requirement": 8,
        "speed_bonus": 2.0,
    },
    "cruiser_thruster_array_t3": {
        "name": "Cruiser Thruster Array T3",
        "type": "thruster_array",
        "ship_type": "cruiser",
        "tier": 3,
        "description": "Cruiser-class propulsion system - Tier 3",
        "cost": 270000,
        "manufacturing_cost": 189000,
        "level_requirement": 15,
        "speed_bonus": 3.0,
    },
    "cruiser_weapon_mount_t1": {
        "name": "Cruiser Weapon Mount T1",
        "type": "weapon_mount",
        "ship_type": "cruiser",
        "tier": 1,
        "description": "Cruiser-class weapon hardpoint - Tier 1",
        "cost": 30000,
        "manufacturing_cost": 21000,
        "level_requirement": 1,
        "weapon_bonus": 1.0,
    },
    "cruiser_weapon_mount_t2": {
        "name": "Cruiser Weapon Mount T2",
        "type": "weapon_mount",
        "ship_type": "cruiser",
        "tier": 2,
        "description": "Cruiser-class weapon hardpoint - Tier 2",
        "cost": 90000,
        "manufacturing_cost": 62999,
        "level_requirement": 8,
        "weapon_bonus": 2.0,
    },
    "cruiser_weapon_mount_t3": {
        "name": "Cruiser Weapon Mount T3",
        "type": "weapon_mount",
        "ship_type": "cruiser",
        "tier": 3,
        "description": "Cruiser-class weapon hardpoint - Tier 3",
        "cost": 270000,
        "manufacturing_cost": 189000,
        "level_requirement": 15,
        "weapon_bonus": 3.0,
    },
    "destroyer_computer_system_t1": {
        "name": "Destroyer Computer System T1",
        "type": "computer_system",
        "ship_type": "destroyer",
        "tier": 1,
        "description": "Destroyer-class AI processor - Tier 1",
        "cost": 48000,
        "manufacturing_cost": 33600,
        "level_requirement": 1,
        "computer_bonus": 1.0,
    },
    "destroyer_computer_system_t2": {
        "name": "Destroyer Computer System T2",
        "type": "computer_system",
        "ship_type": "destroyer",
        "tier": 2,
        "description": "Destroyer-class AI processor - Tier 2",
        "cost": 144000,
        "manufacturing_cost": 100800,
        "level_requirement": 8,
        "computer_bonus": 2.0,
    },
    "destroyer_computer_system_t3": {
        "name": "Destroyer Computer System T3",
        "type": "computer_system",
        "ship_type": "destroyer",
        "tier": 3,
        "description": "Destroyer-class AI processor - Tier 3",
        "cost": 432000,
        "manufacturing_cost": 302400,
        "level_requirement": 15,
        "computer_bonus": 3.0,
    },
    "destroyer_hull_frame_t1": {
        "name": "Destroyer Hull Frame T1",
        "type": "hull_frame",
        "ship_type": "destroyer",
        "tier": 1,
        "description": "Destroyer-class hull structure - Tier 1",
        "cost": 48000,
        "manufacturing_cost": 33600,
        "level_requirement": 1,
        "hull_bonus": 1.0,
    },
    "destroyer_hull_frame_t2": {
        "name": "Destroyer Hull Frame T2",
        "type": "hull_frame",
        "ship_type": "destroyer",
        "tier": 2,
        "description": "Destroyer-class hull structure - Tier 2",
        "cost": 144000,
        "manufacturing_cost": 100800,
        "level_requirement": 8,
        "hull_bonus": 2.0,
    },
    "destroyer_hull_frame_t3": {
        "name": "Destroyer Hull Frame T3",
        "type": "hull_frame",
        "ship_type": "destroyer",
        "tier": 3,
        "description": "Destroyer-class hull structure - Tier 3",
        "cost": 432000,
        "manufacturing_cost": 302400,
        "level_requirement": 15,
        "hull_bonus": 3.0,
    },
    "destroyer_life_support_t1": {
        "name": "Destroyer Life Support T1",
        "type": "life_support",
        "ship_type": "destroyer",
        "tier": 1,
        "description": "Destroyer-class crew systems - Tier 1",
        "cost": 48000,
        "manufacturing_cost": 33600,
        "level_requirement": 1,
        "life_support_bonus": 1.0,
    },
    "destroyer_life_support_t2": {
        "name": "Destroyer Life Support T2",
        "type": "life_support",
        "ship_type": "destroyer",
        "tier": 2,
        "description": "Destroyer-class crew systems - Tier 2",
        "cost": 144000,
        "manufacturing_cost": 100800,
        "level_requirement": 8,
        "life_support_bonus": 2.0,
    },
    "destroyer_life_support_t3": {
        "name": "Destroyer Life Support T3",
        "type": "life_support",
        "ship_type": "destroyer",
        "tier": 3,
        "description": "Destroyer-class crew systems - Tier 3",
        "cost": 432000,
        "manufacturing_cost": 302400,
        "level_requirement": 15,
        "life_support_bonus": 3.0,
    },
    "destroyer_power_core_t1": {
        "name": "Destroyer Power Core T1",
        "type": "power_core",
        "ship_type": "destroyer",
        "tier": 1,
        "description": "Destroyer-class energy generation - Tier 1",
        "cost": 48000,
        "manufacturing_cost": 33600,
        "level_requirement": 1,
        "power_bonus": 1.0,
    },
    "destroyer_power_core_t2": {
        "name": "Destroyer Power Core T2",
        "type": "power_core",
        "ship_type": "destroyer",
        "tier": 2,
        "description": "Destroyer-class energy generation - Tier 2",
        "cost": 144000,
        "manufacturing_cost": 100800,
        "level_requirement": 8,
        "power_bonus": 2.0,
    },
    "destroyer_power_core_t3": {
        "name": "Destroyer Power Core T3",
        "type": "power_core",
        "ship_type": "destroyer",
        "tier": 3,
        "description": "Destroyer-class energy generation - Tier 3",
        "cost": 432000,
        "manufacturing_cost": 302400,
        "level_requirement": 15,
        "power_bonus": 3.0,
    },
    "destroyer_sensor_suite_t1": {
        "name": "Destroyer Sensor Suite T1",
        "type": "sensor_suite",
        "ship_type": "destroyer",
        "tier": 1,
        "description": "Destroyer-class detection system - Tier 1",
        "cost": 48000,
        "manufacturing_cost": 33600,
        "level_requirement": 1,
        "sensor_bonus": 1.0,
    },
    "destroyer_sensor_suite_t2": {
        "name": "Destroyer Sensor Suite T2",
        "type": "sensor_suite",
        "ship_type": "destroyer",
        "tier": 2,
        "description": "Destroyer-class detection system - Tier 2",
        "cost": 144000,
        "manufacturing_cost": 100800,
        "level_requirement": 8,
        "sensor_bonus": 2.0,
    },
    "destroyer_sensor_suite_t3": {
        "name": "Destroyer Sensor Suite T3",
        "type": "sensor_suite",
        "ship_type": "destroyer",
        "tier": 3,
        "description": "Destroyer-class detection system - Tier 3",
        "cost": 432000,
        "manufacturing_cost": 302400,
        "level_requirement": 15,
        "sensor_bonus": 3.0,
    },
    "destroyer_shield_generator_t1": {
        "name": "Destroyer Shield Generator T1",
        "type": "shield_generator",
        "ship_type": "destroyer",
        "tier": 1,
        "description": "Destroyer-class defensive shielding - Tier 1",
        "cost": 48000,
        "manufacturing_cost": 33600,
        "level_requirement": 1,
        "shield_bonus": 1.0,
    },
    "destroyer_shield_generator_t2": {
        "name": "Destroyer Shield Generator T2",
        "type": "shield_generator",
        "ship_type": "destroyer",
        "tier": 2,
        "description": "Destroyer-class defensive shielding - Tier 2",
        "cost": 144000,
        "manufacturing_cost": 100800,
        "level_requirement": 8,
        "shield_bonus": 2.0,
    },
    "destroyer_shield_generator_t3": {
        "name": "Destroyer Shield Generator T3",
        "type": "shield_generator",
        "ship_type": "destroyer",
        "tier": 3,
        "description": "Destroyer-class defensive shielding - Tier 3",
        "cost": 432000,
        "manufacturing_cost": 302400,
        "level_requirement": 15,
        "shield_bonus": 3.0,
    },
    "destroyer_thruster_array_t1": {
        "name": "Destroyer Thruster Array T1",
        "type": "thruster_array",
        "ship_type": "destroyer",
        "tier": 1,
        "description": "Destroyer-class propulsion system - Tier 1",
        "cost": 48000,
        "manufacturing_cost": 33600,
        "level_requirement": 1,
        "speed_bonus": 1.0,
    },
    "destroyer_thruster_array_t2": {
        "name": "Destroyer Thruster Array T2",
        "type": "thruster_array",
        "ship_type": "destroyer",
        "tier": 2,
        "description": "Destroyer-class propulsion system - Tier 2",
        "cost": 144000,
        "manufacturing_cost": 100800,
        "level_requirement": 8,
        "speed_bonus": 2.0,
    },
    "destroyer_thruster_array_t3": {
        "name": "Destroyer Thruster Array T3",
        "type": "thruster_array",
        "ship_type": "destroyer",
        "tier": 3,
        "description": "Destroyer-class propulsion system - Tier 3",
        "cost": 432000,
        "manufacturing_cost": 302400,
        "level_requirement": 15,
        "speed_bonus": 3.0,
    },
    "destroyer_weapon_mount_t1": {
        "name": "Destroyer Weapon Mount T1",
        "type": "weapon_mount",
        "ship_type": "destroyer",
        "tier": 1,
        "description": "Destroyer-class weapon hardpoint - Tier 1",
        "cost": 48000,
        "manufacturing_cost": 33600,
        "level_requirement": 1,
        "weapon_bonus": 1.0,
    },
    "destroyer_weapon_mount_t2": {
        "name": "Destroyer Weapon Mount T2",
        "type": "weapon_mount",
        "ship_type": "destroyer",
        "tier": 2,
        "description": "Destroyer-class weapon hardpoint - Tier 2",
        "cost": 144000,
        "manufacturing_cost": 100800,
        "level_requirement": 8,
        "weapon_bonus": 2.0,
    },
    "destroyer_weapon_mount_t3": {
        "name": "Destroyer Weapon Mount T3",
        "type": "weapon_mount",
        "ship_type": "destroyer",
        "tier": 3,
        "description": "Destroyer-class weapon hardpoint - Tier 3",
        "cost": 432000,
        "manufacturing_cost": 302400,
        "level_requirement": 15,
        "weapon_bonus": 3.0,
    },
    "fighter_computer_system_t1": {
        "name": "Fighter Computer System T1",
        "type": "computer_system",
        "ship_type": "fighter",
        "tier": 1,
        "description": "Fighter-class AI processor - Tier 1",
        "cost": 4800,
        "manufacturing_cost": 3360,
        "level_requirement": 1,
        "computer_bonus": 1.0,
    },
    "fighter_computer_system_t2": {
        "name": "Fighter Computer System T2",
        "type": "computer_system",
        "ship_type": "fighter",
        "tier": 2,
        "description": "Fighter-class AI processor - Tier 2",
        "cost": 14400,
        "manufacturing_cost": 10080,
        "level_requirement": 8,
        "computer_bonus": 2.0,
    },
    "fighter_computer_system_t3": {
        "name": "Fighter Computer System T3",
        "type": "computer_system",
        "ship_type": "fighter",
        "tier": 3,
        "description": "Fighter-class AI processor - Tier 3",
        "cost": 43200,
        "manufacturing_cost": 30239,
        "level_requirement": 15,
        "computer_bonus": 3.0,
    },
    "fighter_hull_frame_t1": {
        "name": "Fighter Hull Frame T1",
        "type": "hull_frame",
        "ship_type": "fighter",
        "tier": 1,
        "description": "Fighter-class hull structure - Tier 1",
        "cost": 4800,
        "manufacturing_cost": 3360,
        "level_requirement": 1,
        "hull_bonus": 1.0,
    },
    "fighter_hull_frame_t2": {
        "name": "Fighter Hull Frame T2",
        "type": "hull_frame",
        "ship_type": "fighter",
        "tier": 2,
        "description": "Fighter-class hull structure - Tier 2",
        "cost": 14400,
        "manufacturing_cost": 10080,
        "level_requirement": 8,
        "hull_bonus": 2.0,
    },
    "fighter_hull_frame_t3": {
        "name": "Fighter Hull Frame T3",
        "type": "hull_frame",
        "ship_type": "fighter",
        "tier": 3,
        "description": "Fighter-class hull structure - Tier 3",
        "cost": 43200,
        "manufacturing_cost": 30239,
        "level_requirement": 15,
        "hull_bonus": 3.0,
    },
    "fighter_life_support_t1": {
        "name": "Fighter Life Support T1",
        "type": "life_support",
        "ship_type": "fighter",
        "tier": 1,
        "description": "Fighter-class crew systems - Tier 1",
        "cost": 4800,
        "manufacturing_cost": 3360,
        "level_requirement": 1,
        "life_support_bonus": 1.0,
    },
    "fighter_life_support_t2": {
        "name": "Fighter Life Support T2",
        "type": "life_support",
        "ship_type": "fighter",
        "tier": 2,
        "description": "Fighter-class crew systems - Tier 2",
        "cost": 14400,
        "manufacturing_cost": 10080,
        "level_requirement": 8,
        "life_support_bonus": 2.0,
    },
    "fighter_life_support_t3": {
        "name": "Fighter Life Support T3",
        "type": "life_support",
        "ship_type": "fighter",
        "tier": 3,
        "description": "Fighter-class crew systems - Tier 3",
        "cost": 43200,
        "manufacturing_cost": 30239,
        "level_requirement": 15,
        "life_support_bonus": 3.0,
    },
    "fighter_power_core_t1": {
        "name": "Fighter Power Core T1",
        "type": "power_core",
        "ship_type": "fighter",
        "tier": 1,
        "description": "Fighter-class energy generation - Tier 1",
        "cost": 4800,
        "manufacturing_cost": 3360,
        "level_requirement": 1,
        "power_bonus": 1.0,
    },
    "fighter_power_core_t2": {
        "name": "Fighter Power Core T2",
        "type": "power_core",
        "ship_type": "fighter",
        "tier": 2,
        "description": "Fighter-class energy generation - Tier 2",
        "cost": 14400,
        "manufacturing_cost": 10080,
        "level_requirement": 8,
        "power_bonus": 2.0,
    },
    "fighter_power_core_t3": {
        "name": "Fighter Power Core T3",
        "type": "power_core",
        "ship_type": "fighter",
        "tier": 3,
        "description": "Fighter-class energy generation - Tier 3",
        "cost": 43200,
        "manufacturing_cost": 30239,
        "level_requirement": 15,
        "power_bonus": 3.0,
    },
    "fighter_sensor_suite_t1": {
        "name": "Fighter Sensor Suite T1",
        "type": "sensor_suite",
        "ship_type": "fighter",
        "tier": 1,
        "description": "Fighter-class detection system - Tier 1",
        "cost": 4800,
        "manufacturing_cost": 3360,
        "level_requirement": 1,
        "sensor_bonus": 1.0,
    },
    "fighter_sensor_suite_t2": {
        "name": "Fighter Sensor Suite T2",
        "type": "sensor_suite",
        "ship_type": "fighter",
        "tier": 2,
        "description": "Fighter-class detection system - Tier 2",
        "cost": 14400,
        "manufacturing_cost": 10080,
        "level_requirement": 8,
        "sensor_bonus": 2.0,
    },
    "fighter_sensor_suite_t3": {
        "name": "Fighter Sensor Suite T3",
        "type": "sensor_suite",
        "ship_type": "fighter",
        "tier": 3,
        "description": "Fighter-class detection system - Tier 3",
        "cost": 43200,
        "manufacturing_cost": 30239,
        "level_requirement": 15,
        "sensor_bonus": 3.0,
    },
    "fighter_shield_generator_t1": {
        "name": "Fighter Shield Generator T1",
        "type": "shield_generator",
        "ship_type": "fighter",
        "tier": 1,
        "description": "Fighter-class defensive shielding - Tier 1",
        "cost": 4800,
        "manufacturing_cost": 3360,
        "level_requirement": 1,
        "shield_bonus": 1.0,
    },
    "fighter_shield_generator_t2": {
        "name": "Fighter Shield Generator T2",
        "type": "shield_generator",
        "ship_type": "fighter",
        "tier": 2,
        "description": "Fighter-class defensive shielding - Tier 2",
        "cost": 14400,
        "manufacturing_cost": 10080,
        "level_requirement": 8,
        "shield_bonus": 2.0,
    },
    "fighter_shield_generator_t3": {
        "name": "Fighter Shield Generator T3",
        "type": "shield_generator",
        "ship_type": "fighter",
        "tier": 3,
        "description": "Fighter-class defensive shielding - Tier 3",
        "cost": 43200,
        "manufacturing_cost": 30239,
        "level_requirement": 15,
        "shield_bonus": 3.0,
    },
    "fighter_thruster_array_t1": {
        "name": "Fighter Thruster Array T1",
        "type": "thruster_array",
        "ship_type": "fighter",
        "tier": 1,
        "description": "Fighter-class propulsion system - Tier 1",
        "cost": 4800,
        "manufacturing_cost": 3360,
        "level_requirement": 1,
        "speed_bonus": 1.0,
    },
    "fighter_thruster_array_t2": {
        "name": "Fighter Thruster Array T2",
        "type": "thruster_array",
        "ship_type": "fighter",
        "tier": 2,
        "description": "Fighter-class propulsion system - Tier 2",
        "cost": 14400,
        "manufacturing_cost": 10080,
        "level_requirement": 8,
        "speed_bonus": 2.0,
    },
    "fighter_thruster_array_t3": {
        "name": "Fighter Thruster Array T3",
        "type": "thruster_array",
        "ship_type": "fighter",
        "tier": 3,
        "description": "Fighter-class propulsion system - Tier 3",
        "cost": 43200,
        "manufacturing_cost": 30239,
        "level_requirement": 15,
        "speed_bonus": 3.0,
    },
    "fighter_weapon_mount_t1": {
        "name": "Fighter Weapon Mount T1",
        "type": "weapon_mount",
        "ship_type": "fighter",
        "tier": 1,
        "description": "Fighter-class weapon hardpoint - Tier 1",
        "cost": 4800,
        "manufacturing_cost": 3360,
        "level_requirement": 1,
        "weapon_bonus": 1.0,
    },
    "fighter_weapon_mount_t2": {
        "name": "Fighter Weapon Mount T2",
        "type": "weapon_mount",
        "ship_type": "fighter",
        "tier": 2,
        "description": "Fighter-class weapon hardpoint - Tier 2",
        "cost": 14400,
        "manufacturing_cost": 10080,
        "level_requirement": 8,
        "weapon_bonus": 2.0,
    },
    "fighter_weapon_mount_t3": {
        "name": "Fighter Weapon Mount T3",
        "type": "weapon_mount",
        "ship_type": "fighter",
        "tier": 3,
        "description": "Fighter-class weapon hardpoint - Tier 3",
        "cost": 43200,
        "manufacturing_cost": 30239,
        "level_requirement": 15,
        "weapon_bonus": 3.0,
    },
    "hauler_computer_system_t1": {
        "name": "Hauler Computer System T1",
        "type": "computer_system",
        "ship_type": "hauler",
        "tier": 1,
        "description": "Hauler-class AI processor - Tier 1",
        "cost": 8600,
        "manufacturing_cost": 6020,
        "level_requirement": 1,
        "computer_bonus": 1.0,
    },
    "hauler_computer_system_t2": {
        "name": "Hauler Computer System T2",
        "type": "computer_system",
        "ship_type": "hauler",
        "tier": 2,
        "description": "Hauler-class AI processor - Tier 2",
        "cost": 25800,
        "manufacturing_cost": 18060,
        "level_requirement": 8,
        "computer_bonus": 2.0,
    },
    "hauler_computer_system_t3": {
        "name": "Hauler Computer System T3",
        "type": "computer_system",
        "ship_type": "hauler",
        "tier": 3,
        "description": "Hauler-class AI processor - Tier 3",
        "cost": 77400,
        "manufacturing_cost": 54180,
        "level_requirement": 15,
        "computer_bonus": 3.0,
    },
    "hauler_hull_frame_t1": {
        "name": "Hauler Hull Frame T1",
        "type": "hull_frame",
        "ship_type": "hauler",
        "tier": 1,
        "description": "Hauler-class hull structure - Tier 1",
        "cost": 8600,
        "manufacturing_cost": 6020,
        "level_requirement": 1,
        "hull_bonus": 1.0,
    },
    "hauler_hull_frame_t2": {
        "name": "Hauler Hull Frame T2",
        "type": "hull_frame",
        "ship_type": "hauler",
        "tier": 2,
        "description": "Hauler-class hull structure - Tier 2",
        "cost": 25800,
        "manufacturing_cost": 18060,
        "level_requirement": 8,
        "hull_bonus": 2.0,
    },
    "hauler_hull_frame_t3": {
        "name": "Hauler Hull Frame T3",
        "type": "hull_frame",
        "ship_type": "hauler",
        "tier": 3,
        "description": "Hauler-class hull structure - Tier 3",
        "cost": 77400,
        "manufacturing_cost": 54180,
        "level_requirement": 15,
        "hull_bonus": 3.0,
    },
    "hauler_life_support_t1": {
        "name": "Hauler Life Support T1",
        "type": "life_support",
        "ship_type": "hauler",
        "tier": 1,
        "description": "Hauler-class crew systems - Tier 1",
        "cost": 8600,
        "manufacturing_cost": 6020,
        "level_requirement": 1,
        "life_support_bonus": 1.0,
    },
    "hauler_life_support_t2": {
        "name": "Hauler Life Support T2",
        "type": "life_support",
        "ship_type": "hauler",
        "tier": 2,
        "description": "Hauler-class crew systems - Tier 2",
        "cost": 25800,
        "manufacturing_cost": 18060,
        "level_requirement": 8,
        "life_support_bonus": 2.0,
    },
    "hauler_life_support_t3": {
        "name": "Hauler Life Support T3",
        "type": "life_support",
        "ship_type": "hauler",
        "tier": 3,
        "description": "Hauler-class crew systems - Tier 3",
        "cost": 77400,
        "manufacturing_cost": 54180,
        "level_requirement": 15,
        "life_support_bonus": 3.0,
    },
    "hauler_power_core_t1": {
        "name": "Hauler Power Core T1",
        "type": "power_core",
        "ship_type": "hauler",
        "tier": 1,
        "description": "Hauler-class energy generation - Tier 1",
        "cost": 8600,
        "manufacturing_cost": 6020,
        "level_requirement": 1,
        "power_bonus": 1.0,
    },
    "hauler_power_core_t2": {
        "name": "Hauler Power Core T2",
        "type": "power_core",
        "ship_type": "hauler",
        "tier": 2,
        "description": "Hauler-class energy generation - Tier 2",
        "cost": 25800,
        "manufacturing_cost": 18060,
        "level_requirement": 8,
        "power_bonus": 2.0,
    },
    "hauler_power_core_t3": {
        "name": "Hauler Power Core T3",
        "type": "power_core",
        "ship_type": "hauler",
        "tier": 3,
        "description": "Hauler-class energy generation - Tier 3",
        "cost": 77400,
        "manufacturing_cost": 54180,
        "level_requirement": 15,
        "power_bonus": 3.0,
    },
    "hauler_sensor_suite_t1": {
        "name": "Hauler Sensor Suite T1",
        "type": "sensor_suite",
        "ship_type": "hauler",
        "tier": 1,
        "description": "Hauler-class detection system - Tier 1",
        "cost": 8600,
        "manufacturing_cost": 6020,
        "level_requirement": 1,
        "sensor_bonus": 1.0,
    },
    "hauler_sensor_suite_t2": {
        "name": "Hauler Sensor Suite T2",
        "type": "sensor_suite",
        "ship_type": "hauler",
        "tier": 2,
        "description": "Hauler-class detection system - Tier 2",
        "cost": 25800,
        "manufacturing_cost": 18060,
        "level_requirement": 8,
        "sensor_bonus": 2.0,
    },
    "hauler_sensor_suite_t3": {
        "name": "Hauler Sensor Suite T3",
        "type": "sensor_suite",
        "ship_type": "hauler",
        "tier": 3,
        "description": "Hauler-class detection system - Tier 3",
        "cost": 77400,
        "manufacturing_cost": 54180,
        "level_requirement": 15,
        "sensor_bonus": 3.0,
    },
    "hauler_shield_generator_t1": {
        "name": "Hauler Shield Generator T1",
        "type": "shield_generator",
        "ship_type": "hauler",
        "tier": 1,
        "description": "Hauler-class defensive shielding - Tier 1",
        "cost": 8600,
        "manufacturing_cost": 6020,
        "level_requirement": 1,
        "shield_bonus": 1.0,
    },
    "hauler_shield_generator_t2": {
        "name": "Hauler Shield Generator T2",
        "type": "shield_generator",
        "ship_type": "hauler",
        "tier": 2,
        "description": "Hauler-class defensive shielding - Tier 2",
        "cost": 25800,
        "manufacturing_cost": 18060,
        "level_requirement": 8,
        "shield_bonus": 2.0,
    },
    "hauler_shield_generator_t3": {
        "name": "Hauler Shield Generator T3",
        "type": "shield_generator",
        "ship_type": "hauler",
        "tier": 3,
        "description": "Hauler-class defensive shielding - Tier 3",
        "cost": 77400,
        "manufacturing_cost": 54180,
        "level_requirement": 15,
        "shield_bonus": 3.0,
    },
    "hauler_thruster_array_t1": {
        "name": "Hauler Thruster Array T1",
        "type": "thruster_array",
        "ship_type": "hauler",
        "tier": 1,
        "description": "Hauler-class propulsion system - Tier 1",
        "cost": 8600,
        "manufacturing_cost": 6020,
        "level_requirement": 1,
        "speed_bonus": 1.0,
    },
    "hauler_thruster_array_t2": {
        "name": "Hauler Thruster Array T2",
        "type": "thruster_array",
        "ship_type": "hauler",
        "tier": 2,
        "description": "Hauler-class propulsion system - Tier 2",
        "cost": 25800,
        "manufacturing_cost": 18060,
        "level_requirement": 8,
        "speed_bonus": 2.0,
    },
    "hauler_thruster_array_t3": {
        "name": "Hauler Thruster Array T3",
        "type": "thruster_array",
        "ship_type": "hauler",
        "tier": 3,
        "description": "Hauler-class propulsion system - Tier 3",
        "cost": 77400,
        "manufacturing_cost": 54180,
        "level_requirement": 15,
        "speed_bonus": 3.0,
    },
    "hauler_weapon_mount_t1": {
        "name": "Hauler Weapon Mount T1",
        "type": "weapon_mount",
        "ship_type": "hauler",
        "tier": 1,
        "description": "Hauler-class weapon hardpoint - Tier 1",
        "cost": 8600,
        "manufacturing_cost": 6020,
        "level_requirement": 1,
        "weapon_bonus": 1.0,
    },
    "hauler_weapon_mount_t2": {
        "name": "Hauler Weapon Mount T2",
        "type": "weapon_mount",
        "ship_type": "hauler",
        "tier": 2,
        "description": "Hauler-class weapon hardpoint - Tier 2",
        "cost": 25800,
        "manufacturing_cost": 18060,
        "level_requirement": 8,
        "weapon_bonus": 2.0,
    },
    "hauler_weapon_mount_t3": {
        "name": "Hauler Weapon Mount T3",
        "type": "weapon_mount",
        "ship_type": "hauler",
        "tier": 3,
        "description": "Hauler-class weapon hardpoint - Tier 3",
        "cost": 77400,
        "manufacturing_cost": 54180,
        "level_requirement": 15,
        "weapon_bonus": 3.0,
    },
    "refinery_computer_system_t1": {
        "name": "Refinery Computer System T1",
        "type": "computer_system",
        "ship_type": "refinery",
        "tier": 1,
        "description": "Refinery-class AI processor - Tier 1",
        "cost": 204000,
        "manufacturing_cost": 142800,
        "level_requirement": 1,
        "computer_bonus": 1.0,
    },
    "refinery_computer_system_t2": {
        "name": "Refinery Computer System T2",
        "type": "computer_system",
        "ship_type": "refinery",
        "tier": 2,
        "description": "Refinery-class AI processor - Tier 2",
        "cost": 612000,
        "manufacturing_cost": 428400,
        "level_requirement": 8,
        "computer_bonus": 2.0,
    },
    "refinery_computer_system_t3": {
        "name": "Refinery Computer System T3",
        "type": "computer_system",
        "ship_type": "refinery",
        "tier": 3,
        "description": "Refinery-class AI processor - Tier 3",
        "cost": 1836000,
        "manufacturing_cost": 1285200,
        "level_requirement": 15,
        "computer_bonus": 3.0,
    },
    "refinery_hull_frame_t1": {
        "name": "Refinery Hull Frame T1",
        "type": "hull_frame",
        "ship_type": "refinery",
        "tier": 1,
        "description": "Refinery-class hull structure - Tier 1",
        "cost": 204000,
        "manufacturing_cost": 142800,
        "level_requirement": 1,
        "hull_bonus": 1.0,
    },
    "refinery_hull_frame_t2": {
        "name": "Refinery Hull Frame T2",
        "type": "hull_frame",
        "ship_type": "refinery",
        "tier": 2,
        "description": "Refinery-class hull structure - Tier 2",
        "cost": 612000,
        "manufacturing_cost": 428400,
        "level_requirement": 8,
        "hull_bonus": 2.0,
    },
    "refinery_hull_frame_t3": {
        "name": "Refinery Hull Frame T3",
        "type": "hull_frame",
        "ship_type": "refinery",
        "tier": 3,
        "description": "Refinery-class hull structure - Tier 3",
        "cost": 1836000,
        "manufacturing_cost": 1285200,
        "level_requirement": 15,
        "hull_bonus": 3.0,
    },
    "refinery_life_support_t1": {
        "name": "Refinery Life Support T1",
        "type": "life_support",
        "ship_type": "refinery",
        "tier": 1,
        "description": "Refinery-class crew systems - Tier 1",
        "cost": 204000,
        "manufacturing_cost": 142800,
        "level_requirement": 1,
        "life_support_bonus": 1.0,
    },
    "refinery_life_support_t2": {
        "name": "Refinery Life Support T2",
        "type": "life_support",
        "ship_type": "refinery",
        "tier": 2,
        "description": "Refinery-class crew systems - Tier 2",
        "cost": 612000,
        "manufacturing_cost": 428400,
        "level_requirement": 8,
        "life_support_bonus": 2.0,
    },
    "refinery_life_support_t3": {
        "name": "Refinery Life Support T3",
        "type": "life_support",
        "ship_type": "refinery",
        "tier": 3,
        "description": "Refinery-class crew systems - Tier 3",
        "cost": 1836000,
        "manufacturing_cost": 1285200,
        "level_requirement": 15,
        "life_support_bonus": 3.0,
    },
    "refinery_power_core_t1": {
        "name": "Refinery Power Core T1",
        "type": "power_core",
        "ship_type": "refinery",
        "tier": 1,
        "description": "Refinery-class energy generation - Tier 1",
        "cost": 204000,
        "manufacturing_cost": 142800,
        "level_requirement": 1,
        "power_bonus": 1.0,
    },
    "refinery_power_core_t2": {
        "name": "Refinery Power Core T2",
        "type": "power_core",
        "ship_type": "refinery",
        "tier": 2,
        "description": "Refinery-class energy generation - Tier 2",
        "cost": 612000,
        "manufacturing_cost": 428400,
        "level_requirement": 8,
        "power_bonus": 2.0,
    },
    "refinery_power_core_t3": {
        "name": "Refinery Power Core T3",
        "type": "power_core",
        "ship_type": "refinery",
        "tier": 3,
        "description": "Refinery-class energy generation - Tier 3",
        "cost": 1836000,
        "manufacturing_cost": 1285200,
        "level_requirement": 15,
        "power_bonus": 3.0,
    },
    "refinery_sensor_suite_t1": {
        "name": "Refinery Sensor Suite T1",
        "type": "sensor_suite",
        "ship_type": "refinery",
        "tier": 1,
        "description": "Refinery-class detection system - Tier 1",
        "cost": 204000,
        "manufacturing_cost": 142800,
        "level_requirement": 1,
        "sensor_bonus": 1.0,
    },
    "refinery_sensor_suite_t2": {
        "name": "Refinery Sensor Suite T2",
        "type": "sensor_suite",
        "ship_type": "refinery",
        "tier": 2,
        "description": "Refinery-class detection system - Tier 2",
        "cost": 612000,
        "manufacturing_cost": 428400,
        "level_requirement": 8,
        "sensor_bonus": 2.0,
    },
    "refinery_sensor_suite_t3": {
        "name": "Refinery Sensor Suite T3",
        "type": "sensor_suite",
        "ship_type": "refinery",
        "tier": 3,
        "description": "Refinery-class detection system - Tier 3",
        "cost": 1836000,
        "manufacturing_cost": 1285200,
        "level_requirement": 15,
        "sensor_bonus": 3.0,
    },
    "refinery_shield_generator_t1": {
        "name": "Refinery Shield Generator T1",
        "type": "shield_generator",
        "ship_type": "refinery",
        "tier": 1,
        "description": "Refinery-class defensive shielding - Tier 1",
        "cost": 204000,
        "manufacturing_cost": 142800,
        "level_requirement": 1,
        "shield_bonus": 1.0,
    },
    "refinery_shield_generator_t2": {
        "name": "Refinery Shield Generator T2",
        "type": "shield_generator",
        "ship_type": "refinery",
        "tier": 2,
        "description": "Refinery-class defensive shielding - Tier 2",
        "cost": 612000,
        "manufacturing_cost": 428400,
        "level_requirement": 8,
        "shield_bonus": 2.0,
    },
    "refinery_shield_generator_t3": {
        "name": "Refinery Shield Generator T3",
        "type": "shield_generator",
        "ship_type": "refinery",
        "tier": 3,
        "description": "Refinery-class defensive shielding - Tier 3",
        "cost": 1836000,
        "manufacturing_cost": 1285200,
        "level_requirement": 15,
        "shield_bonus": 3.0,
    },
    "refinery_thruster_array_t1": {
        "name": "Refinery Thruster Array T1",
        "type": "thruster_array",
        "ship_type": "refinery",
        "tier": 1,
        "description": "Refinery-class propulsion system - Tier 1",
        "cost": 204000,
        "manufacturing_cost": 142800,
        "level_requirement": 1,
        "speed_bonus": 1.0,
    },
    "refinery_thruster_array_t2": {
        "name": "Refinery Thruster Array T2",
        "type": "thruster_array",
        "ship_type": "refinery",
        "tier": 2,
        "description": "Refinery-class propulsion system - Tier 2",
        "cost": 612000,
        "manufacturing_cost": 428400,
        "level_requirement": 8,
        "speed_bonus": 2.0,
    },
    "refinery_thruster_array_t3": {
        "name": "Refinery Thruster Array T3",
        "type": "thruster_array",
        "ship_type": "refinery",
        "tier": 3,
        "description": "Refinery-class propulsion system - Tier 3",
        "cost": 1836000,
        "manufacturing_cost": 1285200,
        "level_requirement": 15,
        "speed_bonus": 3.0,
    },
    "refinery_weapon_mount_t1": {
        "name": "Refinery Weapon Mount T1",
        "type": "weapon_mount",
        "ship_type": "refinery",
        "tier": 1,
        "description": "Refinery-class weapon hardpoint - Tier 1",
        "cost": 204000,
        "manufacturing_cost": 142800,
        "level_requirement": 1,
        "weapon_bonus": 1.0,
    },
    "refinery_weapon_mount_t2": {
        "name": "Refinery Weapon Mount T2",
        "type": "weapon_mount",
        "ship_type": "refinery",
        "tier": 2,
        "description": "Refinery-class weapon hardpoint - Tier 2",
        "cost": 612000,
        "manufacturing_cost": 428400,
        "level_requirement": 8,
        "weapon_bonus": 2.0,
    },
    "refinery_weapon_mount_t3": {
        "name": "Refinery Weapon Mount T3",
        "type": "weapon_mount",
        "ship_type": "refinery",
        "tier": 3,
        "description": "Refinery-class weapon hardpoint - Tier 3",
        "cost": 1836000,
        "manufacturing_cost": 1285200,
        "level_requirement": 15,
        "weapon_bonus": 3.0,
    },
    "scout_computer_system_t1": {
        "name": "Scout Computer System T1",
        "type": "computer_system",
        "ship_type": "scout",
        "tier": 1,
        "description": "Scout-class AI processor - Tier 1",
        "cost": 2400,
        "manufacturing_cost": 1680,
        "level_requirement": 1,
        "computer_bonus": 1.0,
    },
    "scout_computer_system_t2": {
        "name": "Scout Computer System T2",
        "type": "computer_system",
        "ship_type": "scout",
        "tier": 2,
        "description": "Scout-class AI processor - Tier 2",
        "cost": 7200,
        "manufacturing_cost": 5040,
        "level_requirement": 8,
        "computer_bonus": 2.0,
    },
    "scout_computer_system_t3": {
        "name": "Scout Computer System T3",
        "type": "computer_system",
        "ship_type": "scout",
        "tier": 3,
        "description": "Scout-class AI processor - Tier 3",
        "cost": 21600,
        "manufacturing_cost": 15119,
        "level_requirement": 15,
        "computer_bonus": 3.0,
    },
    "scout_hull_frame_t1": {
        "name": "Scout Hull Frame T1",
        "type": "hull_frame",
        "ship_type": "scout",
        "tier": 1,
        "description": "Scout-class hull structure - Tier 1",
        "cost": 2400,
        "manufacturing_cost": 1680,
        "level_requirement": 1,
        "hull_bonus": 1.0,
    },
    "scout_hull_frame_t2": {
        "name": "Scout Hull Frame T2",
        "type": "hull_frame",
        "ship_type": "scout",
        "tier": 2,
        "description": "Scout-class hull structure - Tier 2",
        "cost": 7200,
        "manufacturing_cost": 5040,
        "level_requirement": 8,
        "hull_bonus": 2.0,
    },
    "scout_hull_frame_t3": {
        "name": "Scout Hull Frame T3",
        "type": "hull_frame",
        "ship_type": "scout",
        "tier": 3,
        "description": "Scout-class hull structure - Tier 3",
        "cost": 21600,
        "manufacturing_cost": 15119,
        "level_requirement": 15,
        "hull_bonus": 3.0,
    },
    "scout_life_support_t1": {
        "name": "Scout Life Support T1",
        "type": "life_support",
        "ship_type": "scout",
        "tier": 1,
        "description": "Scout-class crew systems - Tier 1",
        "cost": 2400,
        "manufacturing_cost": 1680,
        "level_requirement": 1,
        "life_support_bonus": 1.0,
    },
    "scout_life_support_t2": {
        "name": "Scout Life Support T2",
        "type": "life_support",
        "ship_type": "scout",
        "tier": 2,
        "description": "Scout-class crew systems - Tier 2",
        "cost": 7200,
        "manufacturing_cost": 5040,
        "level_requirement": 8,
        "life_support_bonus": 2.0,
    },
    "scout_life_support_t3": {
        "name": "Scout Life Support T3",
        "type": "life_support",
        "ship_type": "scout",
        "tier": 3,
        "description": "Scout-class crew systems - Tier 3",
        "cost": 21600,
        "manufacturing_cost": 15119,
        "level_requirement": 15,
        "life_support_bonus": 3.0,
    },
    "scout_power_core_t1": {
        "name": "Scout Power Core T1",
        "type": "power_core",
        "ship_type": "scout",
        "tier": 1,
        "description": "Scout-class energy generation - Tier 1",
        "cost": 2400,
        "manufacturing_cost": 1680,
        "level_requirement": 1,
        "power_bonus": 1.0,
    },
    "scout_power_core_t2": {
        "name": "Scout Power Core T2",
        "type": "power_core",
        "ship_type": "scout",
        "tier": 2,
        "description": "Scout-class energy generation - Tier 2",
        "cost": 7200,
        "manufacturing_cost": 5040,
        "level_requirement": 8,
        "power_bonus": 2.0,
    },
    "scout_power_core_t3": {
        "name": "Scout Power Core T3",
        "type": "power_core",
        "ship_type": "scout",
        "tier": 3,
        "description": "Scout-class energy generation - Tier 3",
        "cost": 21600,
        "manufacturing_cost": 15119,
        "level_requirement": 15,
        "power_bonus": 3.0,
    },
    "scout_sensor_suite_t1": {
        "name": "Scout Sensor Suite T1",
        "type": "sensor_suite",
        "ship_type": "scout",
        "tier": 1,
        "description": "Scout-class detection system - Tier 1",
        "cost": 2400,
        "manufacturing_cost": 1680,
        "level_requirement": 1,
        "sensor_bonus": 1.0,
    },
    "scout_sensor_suite_t2": {
        "name": "Scout Sensor Suite T2",
        "type": "sensor_suite",
        "ship_type": "scout",
        "tier": 2,
        "description": "Scout-class detection system - Tier 2",
        "cost": 7200,
        "manufacturing_cost": 5040,
        "level_requirement": 8,
        "sensor_bonus": 2.0,
    },
    "scout_sensor_suite_t3": {
        "name": "Scout Sensor Suite T3",
        "type": "sensor_suite",
        "ship_type": "scout",
        "tier": 3,
        "description": "Scout-class detection system - Tier 3",
        "cost": 21600,
        "manufacturing_cost": 15119,
        "level_requirement": 15,
        "sensor_bonus": 3.0,
    },
    "scout_shield_generator_t1": {
        "name": "Scout Shield Generator T1",
        "type": "shield_generator",
        "ship_type": "scout",
        "tier": 1,
        "description": "Scout-class defensive shielding - Tier 1",
        "cost": 2400,
        "manufacturing_cost": 1680,
        "level_requirement": 1,
        "shield_bonus": 1.0,
    },
    "scout_shield_generator_t2": {
        "name": "Scout Shield Generator T2",
        "type": "shield_generator",
        "ship_type": "scout",
        "tier": 2,
        "description": "Scout-class defensive shielding - Tier 2",
        "cost": 7200,
        "manufacturing_cost": 5040,
        "level_requirement": 8,
        "shield_bonus": 2.0,
    },
    "scout_shield_generator_t3": {
        "name": "Scout Shield Generator T3",
        "type": "shield_generator",
        "ship_type": "scout",
        "tier": 3,
        "description": "Scout-class defensive shielding - Tier 3",
        "cost": 21600,
        "manufacturing_cost": 15119,
        "level_requirement": 15,
        "shield_bonus": 3.0,
    },
    "scout_thruster_array_t1": {
        "name": "Scout Thruster Array T1",
        "type": "thruster_array",
        "ship_type": "scout",
        "tier": 1,
        "description": "Scout-class propulsion system - Tier 1",
        "cost": 2400,
        "manufacturing_cost": 1680,
        "level_requirement": 1,
        "speed_bonus": 1.0,
    },
    "scout_thruster_array_t2": {
        "name": "Scout Thruster Array T2",
        "type": "thruster_array",
        "ship_type": "scout",
        "tier": 2,
        "description": "Scout-class propulsion system - Tier 2",
        "cost": 7200,
        "manufacturing_cost": 5040,
        "level_requirement": 8,
        "speed_bonus": 2.0,
    },
    "scout_thruster_array_t3": {
        "name": "Scout Thruster Array T3",
        "type": "thruster_array",
        "ship_type": "scout",
        "tier": 3,
        "description": "Scout-class propulsion system - Tier 3",
        "cost": 21600,
        "manufacturing_cost": 15119,
        "level_requirement": 15,
        "speed_bonus": 3.0,
    },
    "scout_weapon_mount_t1": {
        "name": "Scout Weapon Mount T1",
        "type": "weapon_mount",
        "ship_type": "scout",
        "tier": 1,
        "description": "Scout-class weapon hardpoint - Tier 1",
        "cost": 2400,
        "manufacturing_cost": 1680,
        "level_requirement": 1,
        "weapon_bonus": 1.0,
    },
    "scout_weapon_mount_t2": {
        "name": "Scout Weapon Mount T2",
        "type": "weapon_mount",
        "ship_type": "scout",
        "tier": 2,
        "description": "Scout-class weapon hardpoint - Tier 2",
        "cost": 7200,
        "manufacturing_cost": 5040,
        "level_requirement": 8,
        "weapon_bonus": 2.0,
    },
    "scout_weapon_mount_t3": {
        "name": "Scout Weapon Mount T3",
        "type": "weapon_mount",
        "ship_type": "scout",
        "tier": 3,
        "description": "Scout-class weapon hardpoint - Tier 3",
        "cost": 21600,
        "manufacturing_cost": 15119,
        "level_requirement": 15,
        "weapon_bonus": 3.0,
    },
}

# Total components: 192


# ============= COMPONENT RECIPES =============
COMPONENT_RECIPES = {
    "battleship_computer_system_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 420, 'skill_requirement': 0},
    "battleship_computer_system_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 840, 'skill_requirement': 2},
    "battleship_computer_system_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 1260, 'skill_requirement': 5},
    "battleship_hull_frame_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 420, 'skill_requirement': 0},
    "battleship_hull_frame_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 840, 'skill_requirement': 2},
    "battleship_hull_frame_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 1260, 'skill_requirement': 5},
    "battleship_life_support_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 420, 'skill_requirement': 0},
    "battleship_life_support_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 840, 'skill_requirement': 2},
    "battleship_life_support_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 1260, 'skill_requirement': 5},
    "battleship_power_core_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 420, 'skill_requirement': 0},
    "battleship_power_core_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 840, 'skill_requirement': 2},
    "battleship_power_core_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 1260, 'skill_requirement': 5},
    "battleship_sensor_suite_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 420, 'skill_requirement': 0},
    "battleship_sensor_suite_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 840, 'skill_requirement': 2},
    "battleship_sensor_suite_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 1260, 'skill_requirement': 5},
    "battleship_shield_generator_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 420, 'skill_requirement': 0},
    "battleship_shield_generator_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 840, 'skill_requirement': 2},
    "battleship_shield_generator_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 1260, 'skill_requirement': 5},
    "battleship_thruster_array_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 420, 'skill_requirement': 0},
    "battleship_thruster_array_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 840, 'skill_requirement': 2},
    "battleship_thruster_array_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 1260, 'skill_requirement': 5},
    "battleship_weapon_mount_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 420, 'skill_requirement': 0},
    "battleship_weapon_mount_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 840, 'skill_requirement': 2},
    "battleship_weapon_mount_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 1260, 'skill_requirement': 5},
    "carrier_computer_system_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 400, 'skill_requirement': 0},
    "carrier_computer_system_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 800, 'skill_requirement': 2},
    "carrier_computer_system_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 1200, 'skill_requirement': 5},
    "carrier_hull_frame_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 400, 'skill_requirement': 0},
    "carrier_hull_frame_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 800, 'skill_requirement': 2},
    "carrier_hull_frame_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 1200, 'skill_requirement': 5},
    "carrier_life_support_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 400, 'skill_requirement': 0},
    "carrier_life_support_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 800, 'skill_requirement': 2},
    "carrier_life_support_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 1200, 'skill_requirement': 5},
    "carrier_power_core_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 400, 'skill_requirement': 0},
    "carrier_power_core_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 800, 'skill_requirement': 2},
    "carrier_power_core_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 1200, 'skill_requirement': 5},
    "carrier_sensor_suite_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 400, 'skill_requirement': 0},
    "carrier_sensor_suite_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 800, 'skill_requirement': 2},
    "carrier_sensor_suite_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 1200, 'skill_requirement': 5},
    "carrier_shield_generator_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 400, 'skill_requirement': 0},
    "carrier_shield_generator_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 800, 'skill_requirement': 2},
    "carrier_shield_generator_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 1200, 'skill_requirement': 5},
    "carrier_thruster_array_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 400, 'skill_requirement': 0},
    "carrier_thruster_array_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 800, 'skill_requirement': 2},
    "carrier_thruster_array_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 1200, 'skill_requirement': 5},
    "carrier_weapon_mount_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 400, 'skill_requirement': 0},
    "carrier_weapon_mount_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 800, 'skill_requirement': 2},
    "carrier_weapon_mount_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 1200, 'skill_requirement': 5},
    "cruiser_computer_system_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 300, 'skill_requirement': 0},
    "cruiser_computer_system_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 600, 'skill_requirement': 2},
    "cruiser_computer_system_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 900, 'skill_requirement': 5},
    "cruiser_hull_frame_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 300, 'skill_requirement': 0},
    "cruiser_hull_frame_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 600, 'skill_requirement': 2},
    "cruiser_hull_frame_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 900, 'skill_requirement': 5},
    "cruiser_life_support_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 300, 'skill_requirement': 0},
    "cruiser_life_support_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 600, 'skill_requirement': 2},
    "cruiser_life_support_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 900, 'skill_requirement': 5},
    "cruiser_power_core_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 300, 'skill_requirement': 0},
    "cruiser_power_core_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 600, 'skill_requirement': 2},
    "cruiser_power_core_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 900, 'skill_requirement': 5},
    "cruiser_sensor_suite_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 300, 'skill_requirement': 0},
    "cruiser_sensor_suite_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 600, 'skill_requirement': 2},
    "cruiser_sensor_suite_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 900, 'skill_requirement': 5},
    "cruiser_shield_generator_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 300, 'skill_requirement': 0},
    "cruiser_shield_generator_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 600, 'skill_requirement': 2},
    "cruiser_shield_generator_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 900, 'skill_requirement': 5},
    "cruiser_thruster_array_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 300, 'skill_requirement': 0},
    "cruiser_thruster_array_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 600, 'skill_requirement': 2},
    "cruiser_thruster_array_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 900, 'skill_requirement': 5},
    "cruiser_weapon_mount_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 300, 'skill_requirement': 0},
    "cruiser_weapon_mount_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 600, 'skill_requirement': 2},
    "cruiser_weapon_mount_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 900, 'skill_requirement': 5},
    "destroyer_computer_system_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 360, 'skill_requirement': 0},
    "destroyer_computer_system_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 720, 'skill_requirement': 2},
    "destroyer_computer_system_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 1080, 'skill_requirement': 5},
    "destroyer_hull_frame_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 360, 'skill_requirement': 0},
    "destroyer_hull_frame_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 720, 'skill_requirement': 2},
    "destroyer_hull_frame_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 1080, 'skill_requirement': 5},
    "destroyer_life_support_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 360, 'skill_requirement': 0},
    "destroyer_life_support_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 720, 'skill_requirement': 2},
    "destroyer_life_support_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 1080, 'skill_requirement': 5},
    "destroyer_power_core_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 360, 'skill_requirement': 0},
    "destroyer_power_core_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 720, 'skill_requirement': 2},
    "destroyer_power_core_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 1080, 'skill_requirement': 5},
    "destroyer_sensor_suite_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 360, 'skill_requirement': 0},
    "destroyer_sensor_suite_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 720, 'skill_requirement': 2},
    "destroyer_sensor_suite_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 1080, 'skill_requirement': 5},
    "destroyer_shield_generator_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 360, 'skill_requirement': 0},
    "destroyer_shield_generator_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 720, 'skill_requirement': 2},
    "destroyer_shield_generator_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 1080, 'skill_requirement': 5},
    "destroyer_thruster_array_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 360, 'skill_requirement': 0},
    "destroyer_thruster_array_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 720, 'skill_requirement': 2},
    "destroyer_thruster_array_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 1080, 'skill_requirement': 5},
    "destroyer_weapon_mount_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 360, 'skill_requirement': 0},
    "destroyer_weapon_mount_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 720, 'skill_requirement': 2},
    "destroyer_weapon_mount_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 1080, 'skill_requirement': 5},
    "fighter_computer_system_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 200, 'skill_requirement': 0},
    "fighter_computer_system_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 400, 'skill_requirement': 2},
    "fighter_computer_system_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 600, 'skill_requirement': 5},
    "fighter_hull_frame_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 200, 'skill_requirement': 0},
    "fighter_hull_frame_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 400, 'skill_requirement': 2},
    "fighter_hull_frame_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 600, 'skill_requirement': 5},
    "fighter_life_support_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 200, 'skill_requirement': 0},
    "fighter_life_support_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 400, 'skill_requirement': 2},
    "fighter_life_support_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 600, 'skill_requirement': 5},
    "fighter_power_core_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 200, 'skill_requirement': 0},
    "fighter_power_core_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 400, 'skill_requirement': 2},
    "fighter_power_core_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 600, 'skill_requirement': 5},
    "fighter_sensor_suite_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 200, 'skill_requirement': 0},
    "fighter_sensor_suite_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 400, 'skill_requirement': 2},
    "fighter_sensor_suite_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 600, 'skill_requirement': 5},
    "fighter_shield_generator_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 200, 'skill_requirement': 0},
    "fighter_shield_generator_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 400, 'skill_requirement': 2},
    "fighter_shield_generator_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 600, 'skill_requirement': 5},
    "fighter_thruster_array_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 200, 'skill_requirement': 0},
    "fighter_thruster_array_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 400, 'skill_requirement': 2},
    "fighter_thruster_array_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 600, 'skill_requirement': 5},
    "fighter_weapon_mount_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 200, 'skill_requirement': 0},
    "fighter_weapon_mount_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 400, 'skill_requirement': 2},
    "fighter_weapon_mount_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 600, 'skill_requirement': 5},
    "hauler_computer_system_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 240, 'skill_requirement': 0},
    "hauler_computer_system_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 480, 'skill_requirement': 2},
    "hauler_computer_system_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 720, 'skill_requirement': 5},
    "hauler_hull_frame_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 240, 'skill_requirement': 0},
    "hauler_hull_frame_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 480, 'skill_requirement': 2},
    "hauler_hull_frame_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 720, 'skill_requirement': 5},
    "hauler_life_support_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 240, 'skill_requirement': 0},
    "hauler_life_support_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 480, 'skill_requirement': 2},
    "hauler_life_support_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 720, 'skill_requirement': 5},
    "hauler_power_core_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 240, 'skill_requirement': 0},
    "hauler_power_core_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 480, 'skill_requirement': 2},
    "hauler_power_core_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 720, 'skill_requirement': 5},
    "hauler_sensor_suite_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 240, 'skill_requirement': 0},
    "hauler_sensor_suite_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 480, 'skill_requirement': 2},
    "hauler_sensor_suite_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 720, 'skill_requirement': 5},
    "hauler_shield_generator_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 240, 'skill_requirement': 0},
    "hauler_shield_generator_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 480, 'skill_requirement': 2},
    "hauler_shield_generator_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 720, 'skill_requirement': 5},
    "hauler_thruster_array_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 240, 'skill_requirement': 0},
    "hauler_thruster_array_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 480, 'skill_requirement': 2},
    "hauler_thruster_array_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 720, 'skill_requirement': 5},
    "hauler_weapon_mount_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 240, 'skill_requirement': 0},
    "hauler_weapon_mount_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 480, 'skill_requirement': 2},
    "hauler_weapon_mount_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 720, 'skill_requirement': 5},
    "refinery_computer_system_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 480, 'skill_requirement': 0},
    "refinery_computer_system_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 960, 'skill_requirement': 2},
    "refinery_computer_system_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 1440, 'skill_requirement': 5},
    "refinery_hull_frame_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 480, 'skill_requirement': 0},
    "refinery_hull_frame_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 960, 'skill_requirement': 2},
    "refinery_hull_frame_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 1440, 'skill_requirement': 5},
    "refinery_life_support_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 480, 'skill_requirement': 0},
    "refinery_life_support_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 960, 'skill_requirement': 2},
    "refinery_life_support_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 1440, 'skill_requirement': 5},
    "refinery_power_core_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 480, 'skill_requirement': 0},
    "refinery_power_core_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 960, 'skill_requirement': 2},
    "refinery_power_core_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 1440, 'skill_requirement': 5},
    "refinery_sensor_suite_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 480, 'skill_requirement': 0},
    "refinery_sensor_suite_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 960, 'skill_requirement': 2},
    "refinery_sensor_suite_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 1440, 'skill_requirement': 5},
    "refinery_shield_generator_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 480, 'skill_requirement': 0},
    "refinery_shield_generator_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 960, 'skill_requirement': 2},
    "refinery_shield_generator_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 1440, 'skill_requirement': 5},
    "refinery_thruster_array_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 480, 'skill_requirement': 0},
    "refinery_thruster_array_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 960, 'skill_requirement': 2},
    "refinery_thruster_array_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 1440, 'skill_requirement': 5},
    "refinery_weapon_mount_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 480, 'skill_requirement': 0},
    "refinery_weapon_mount_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 960, 'skill_requirement': 2},
    "refinery_weapon_mount_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 1440, 'skill_requirement': 5},
    "scout_computer_system_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 180, 'skill_requirement': 0},
    "scout_computer_system_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 360, 'skill_requirement': 2},
    "scout_computer_system_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 540, 'skill_requirement': 5},
    "scout_hull_frame_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 180, 'skill_requirement': 0},
    "scout_hull_frame_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 360, 'skill_requirement': 2},
    "scout_hull_frame_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 540, 'skill_requirement': 5},
    "scout_life_support_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 180, 'skill_requirement': 0},
    "scout_life_support_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 360, 'skill_requirement': 2},
    "scout_life_support_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 540, 'skill_requirement': 5},
    "scout_power_core_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 180, 'skill_requirement': 0},
    "scout_power_core_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 360, 'skill_requirement': 2},
    "scout_power_core_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 540, 'skill_requirement': 5},
    "scout_sensor_suite_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 180, 'skill_requirement': 0},
    "scout_sensor_suite_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 360, 'skill_requirement': 2},
    "scout_sensor_suite_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 540, 'skill_requirement': 5},
    "scout_shield_generator_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 180, 'skill_requirement': 0},
    "scout_shield_generator_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 360, 'skill_requirement': 2},
    "scout_shield_generator_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 540, 'skill_requirement': 5},
    "scout_thruster_array_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 180, 'skill_requirement': 0},
    "scout_thruster_array_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 360, 'skill_requirement': 2},
    "scout_thruster_array_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 540, 'skill_requirement': 5},
    "scout_weapon_mount_t1": {'materials': {'titanite': 50, 'voltium': 20, 'nexium': 10}, 'time': 180, 'skill_requirement': 0},
    "scout_weapon_mount_t2": {'materials': {'titanite': 120, 'voltium': 50, 'nexium': 30, 'neural_fiber': 20}, 'time': 360, 'skill_requirement': 2},
    "scout_weapon_mount_t3": {'materials': {'titanite': 250, 'voltium': 120, 'nexium': 80, 'neural_fiber': 50, 'chronite': 40}, 'time': 540, 'skill_requirement': 5},
}

# Total recipes: 192

# Ship recipes now use ship-specific components
# Each ship requires 8 components matching its type and tier

SHIP_RECIPES = {
    "scout_standard_mk1": {
        "components": {'scout_hull_frame_t1': 1, 'scout_power_core_t1': 1, 'scout_thruster_array_t1': 1, 'scout_shield_generator_t1': 1, 'scout_weapon_mount_t1': 1, 'scout_sensor_suite_t1': 1, 'scout_computer_system_t1': 1, 'scout_life_support_t1': 1},
        "time": 1200,
        "skill_requirement": 3
    },
    "scout_standard_mk2": {
        "components": {'scout_hull_frame_t2': 1, 'scout_power_core_t2': 1, 'scout_thruster_array_t2': 1, 'scout_shield_generator_t2': 1, 'scout_weapon_mount_t2': 1, 'scout_sensor_suite_t2': 1, 'scout_computer_system_t2': 1, 'scout_life_support_t2': 1},
        "time": 2400,
        "skill_requirement": 8
    },
    "scout_standard_mk3": {
        "components": {'scout_hull_frame_t3': 1, 'scout_power_core_t3': 1, 'scout_thruster_array_t3': 1, 'scout_shield_generator_t3': 1, 'scout_weapon_mount_t3': 1, 'scout_sensor_suite_t3': 1, 'scout_computer_system_t3': 1, 'scout_life_support_t3': 1},
        "time": 3600,
        "skill_requirement": 12
    },
    "scout_advanced_mk1": {
        "components": {'scout_hull_frame_t1': 1, 'scout_power_core_t1': 1, 'scout_thruster_array_t1': 1, 'scout_shield_generator_t1': 1, 'scout_weapon_mount_t1': 1, 'scout_sensor_suite_t1': 1, 'scout_computer_system_t1': 1, 'scout_life_support_t1': 1},
        "time": 1560,
        "skill_requirement": 3
    },
    "scout_advanced_mk2": {
        "components": {'scout_hull_frame_t2': 1, 'scout_power_core_t2': 1, 'scout_thruster_array_t2': 1, 'scout_shield_generator_t2': 1, 'scout_weapon_mount_t2': 1, 'scout_sensor_suite_t2': 1, 'scout_computer_system_t2': 1, 'scout_life_support_t2': 1},
        "time": 3120,
        "skill_requirement": 8
    },
    "scout_advanced_mk3": {
        "components": {'scout_hull_frame_t3': 1, 'scout_power_core_t3': 1, 'scout_thruster_array_t3': 1, 'scout_shield_generator_t3': 1, 'scout_weapon_mount_t3': 1, 'scout_sensor_suite_t3': 1, 'scout_computer_system_t3': 1, 'scout_life_support_t3': 1},
        "time": 4680,
        "skill_requirement": 12
    },
    "scout_elite_mk1": {
        "components": {'scout_hull_frame_t1': 1, 'scout_power_core_t1': 1, 'scout_thruster_array_t1': 1, 'scout_shield_generator_t1': 1, 'scout_weapon_mount_t1': 1, 'scout_sensor_suite_t1': 1, 'scout_computer_system_t1': 1, 'scout_life_support_t1': 1},
        "time": 2040,
        "skill_requirement": 3
    },
    "scout_elite_mk2": {
        "components": {'scout_hull_frame_t2': 1, 'scout_power_core_t2': 1, 'scout_thruster_array_t2': 1, 'scout_shield_generator_t2': 1, 'scout_weapon_mount_t2': 1, 'scout_sensor_suite_t2': 1, 'scout_computer_system_t2': 1, 'scout_life_support_t2': 1},
        "time": 4080,
        "skill_requirement": 8
    },
    "scout_elite_mk3": {
        "components": {'scout_hull_frame_t3': 1, 'scout_power_core_t3': 1, 'scout_thruster_array_t3': 1, 'scout_shield_generator_t3': 1, 'scout_weapon_mount_t3': 1, 'scout_sensor_suite_t3': 1, 'scout_computer_system_t3': 1, 'scout_life_support_t3': 1},
        "time": 6120,
        "skill_requirement": 12
    },
    "scout_specialized_mk1": {
        "components": {'scout_hull_frame_t1': 1, 'scout_power_core_t1': 1, 'scout_thruster_array_t1': 1, 'scout_shield_generator_t1': 1, 'scout_weapon_mount_t1': 1, 'scout_sensor_suite_t1': 1, 'scout_computer_system_t1': 1, 'scout_life_support_t1': 1},
        "time": 2640,
        "skill_requirement": 3
    },
    "scout_specialized_mk2": {
        "components": {'scout_hull_frame_t2': 1, 'scout_power_core_t2': 1, 'scout_thruster_array_t2': 1, 'scout_shield_generator_t2': 1, 'scout_weapon_mount_t2': 1, 'scout_sensor_suite_t2': 1, 'scout_computer_system_t2': 1, 'scout_life_support_t2': 1},
        "time": 5280,
        "skill_requirement": 8
    },
    "scout_specialized_mk3": {
        "components": {'scout_hull_frame_t3': 1, 'scout_power_core_t3': 1, 'scout_thruster_array_t3': 1, 'scout_shield_generator_t3': 1, 'scout_weapon_mount_t3': 1, 'scout_sensor_suite_t3': 1, 'scout_computer_system_t3': 1, 'scout_life_support_t3': 1},
        "time": 7920,
        "skill_requirement": 12
    },
    "fighter_standard_mk1": {
        "components": {'fighter_hull_frame_t1': 1, 'fighter_power_core_t1': 1, 'fighter_thruster_array_t1': 1, 'fighter_shield_generator_t1': 1, 'fighter_weapon_mount_t1': 1, 'fighter_sensor_suite_t1': 1, 'fighter_computer_system_t1': 1, 'fighter_life_support_t1': 1},
        "time": 1500,
        "skill_requirement": 3
    },
    "fighter_standard_mk2": {
        "components": {'fighter_hull_frame_t2': 1, 'fighter_power_core_t2': 1, 'fighter_thruster_array_t2': 1, 'fighter_shield_generator_t2': 1, 'fighter_weapon_mount_t2': 1, 'fighter_sensor_suite_t2': 1, 'fighter_computer_system_t2': 1, 'fighter_life_support_t2': 1},
        "time": 3000,
        "skill_requirement": 8
    },
    "fighter_standard_mk3": {
        "components": {'fighter_hull_frame_t3': 1, 'fighter_power_core_t3': 1, 'fighter_thruster_array_t3': 1, 'fighter_shield_generator_t3': 1, 'fighter_weapon_mount_t3': 1, 'fighter_sensor_suite_t3': 1, 'fighter_computer_system_t3': 1, 'fighter_life_support_t3': 1},
        "time": 4500,
        "skill_requirement": 12
    },
    "fighter_advanced_mk1": {
        "components": {'fighter_hull_frame_t1': 1, 'fighter_power_core_t1': 1, 'fighter_thruster_array_t1': 1, 'fighter_shield_generator_t1': 1, 'fighter_weapon_mount_t1': 1, 'fighter_sensor_suite_t1': 1, 'fighter_computer_system_t1': 1, 'fighter_life_support_t1': 1},
        "time": 1950,
        "skill_requirement": 3
    },
    "fighter_advanced_mk2": {
        "components": {'fighter_hull_frame_t2': 1, 'fighter_power_core_t2': 1, 'fighter_thruster_array_t2': 1, 'fighter_shield_generator_t2': 1, 'fighter_weapon_mount_t2': 1, 'fighter_sensor_suite_t2': 1, 'fighter_computer_system_t2': 1, 'fighter_life_support_t2': 1},
        "time": 3900,
        "skill_requirement": 8
    },
    "fighter_advanced_mk3": {
        "components": {'fighter_hull_frame_t3': 1, 'fighter_power_core_t3': 1, 'fighter_thruster_array_t3': 1, 'fighter_shield_generator_t3': 1, 'fighter_weapon_mount_t3': 1, 'fighter_sensor_suite_t3': 1, 'fighter_computer_system_t3': 1, 'fighter_life_support_t3': 1},
        "time": 5850,
        "skill_requirement": 12
    },
    "fighter_elite_mk1": {
        "components": {'fighter_hull_frame_t1': 1, 'fighter_power_core_t1': 1, 'fighter_thruster_array_t1': 1, 'fighter_shield_generator_t1': 1, 'fighter_weapon_mount_t1': 1, 'fighter_sensor_suite_t1': 1, 'fighter_computer_system_t1': 1, 'fighter_life_support_t1': 1},
        "time": 2550,
        "skill_requirement": 3
    },
    "fighter_elite_mk2": {
        "components": {'fighter_hull_frame_t2': 1, 'fighter_power_core_t2': 1, 'fighter_thruster_array_t2': 1, 'fighter_shield_generator_t2': 1, 'fighter_weapon_mount_t2': 1, 'fighter_sensor_suite_t2': 1, 'fighter_computer_system_t2': 1, 'fighter_life_support_t2': 1},
        "time": 5100,
        "skill_requirement": 8
    },
    "fighter_elite_mk3": {
        "components": {'fighter_hull_frame_t3': 1, 'fighter_power_core_t3': 1, 'fighter_thruster_array_t3': 1, 'fighter_shield_generator_t3': 1, 'fighter_weapon_mount_t3': 1, 'fighter_sensor_suite_t3': 1, 'fighter_computer_system_t3': 1, 'fighter_life_support_t3': 1},
        "time": 7650,
        "skill_requirement": 12
    },
    "fighter_specialized_mk1": {
        "components": {'fighter_hull_frame_t1': 1, 'fighter_power_core_t1': 1, 'fighter_thruster_array_t1': 1, 'fighter_shield_generator_t1': 1, 'fighter_weapon_mount_t1': 1, 'fighter_sensor_suite_t1': 1, 'fighter_computer_system_t1': 1, 'fighter_life_support_t1': 1},
        "time": 3300,
        "skill_requirement": 3
    },
    "fighter_specialized_mk2": {
        "components": {'fighter_hull_frame_t2': 1, 'fighter_power_core_t2': 1, 'fighter_thruster_array_t2': 1, 'fighter_shield_generator_t2': 1, 'fighter_weapon_mount_t2': 1, 'fighter_sensor_suite_t2': 1, 'fighter_computer_system_t2': 1, 'fighter_life_support_t2': 1},
        "time": 6600,
        "skill_requirement": 8
    },
    "fighter_specialized_mk3": {
        "components": {'fighter_hull_frame_t3': 1, 'fighter_power_core_t3': 1, 'fighter_thruster_array_t3': 1, 'fighter_shield_generator_t3': 1, 'fighter_weapon_mount_t3': 1, 'fighter_sensor_suite_t3': 1, 'fighter_computer_system_t3': 1, 'fighter_life_support_t3': 1},
        "time": 9900,
        "skill_requirement": 12
    },
    "hauler_standard_mk1": {
        "components": {'hauler_hull_frame_t1': 1, 'hauler_power_core_t1': 1, 'hauler_thruster_array_t1': 1, 'hauler_shield_generator_t1': 1, 'hauler_weapon_mount_t1': 1, 'hauler_sensor_suite_t1': 1, 'hauler_computer_system_t1': 1, 'hauler_life_support_t1': 1},
        "time": 1800,
        "skill_requirement": 3
    },
    "hauler_standard_mk2": {
        "components": {'hauler_hull_frame_t2': 1, 'hauler_power_core_t2': 1, 'hauler_thruster_array_t2': 1, 'hauler_shield_generator_t2': 1, 'hauler_weapon_mount_t2': 1, 'hauler_sensor_suite_t2': 1, 'hauler_computer_system_t2': 1, 'hauler_life_support_t2': 1},
        "time": 3600,
        "skill_requirement": 8
    },
    "hauler_standard_mk3": {
        "components": {'hauler_hull_frame_t3': 1, 'hauler_power_core_t3': 1, 'hauler_thruster_array_t3': 1, 'hauler_shield_generator_t3': 1, 'hauler_weapon_mount_t3': 1, 'hauler_sensor_suite_t3': 1, 'hauler_computer_system_t3': 1, 'hauler_life_support_t3': 1},
        "time": 5400,
        "skill_requirement": 12
    },
    "hauler_advanced_mk1": {
        "components": {'hauler_hull_frame_t1': 1, 'hauler_power_core_t1': 1, 'hauler_thruster_array_t1': 1, 'hauler_shield_generator_t1': 1, 'hauler_weapon_mount_t1': 1, 'hauler_sensor_suite_t1': 1, 'hauler_computer_system_t1': 1, 'hauler_life_support_t1': 1},
        "time": 2340,
        "skill_requirement": 3
    },
    "hauler_advanced_mk2": {
        "components": {'hauler_hull_frame_t2': 1, 'hauler_power_core_t2': 1, 'hauler_thruster_array_t2': 1, 'hauler_shield_generator_t2': 1, 'hauler_weapon_mount_t2': 1, 'hauler_sensor_suite_t2': 1, 'hauler_computer_system_t2': 1, 'hauler_life_support_t2': 1},
        "time": 4680,
        "skill_requirement": 8
    },
    "hauler_advanced_mk3": {
        "components": {'hauler_hull_frame_t3': 1, 'hauler_power_core_t3': 1, 'hauler_thruster_array_t3': 1, 'hauler_shield_generator_t3': 1, 'hauler_weapon_mount_t3': 1, 'hauler_sensor_suite_t3': 1, 'hauler_computer_system_t3': 1, 'hauler_life_support_t3': 1},
        "time": 7020,
        "skill_requirement": 12
    },
    "hauler_elite_mk1": {
        "components": {'hauler_hull_frame_t1': 1, 'hauler_power_core_t1': 1, 'hauler_thruster_array_t1': 1, 'hauler_shield_generator_t1': 1, 'hauler_weapon_mount_t1': 1, 'hauler_sensor_suite_t1': 1, 'hauler_computer_system_t1': 1, 'hauler_life_support_t1': 1},
        "time": 3060,
        "skill_requirement": 3
    },
    "hauler_elite_mk2": {
        "components": {'hauler_hull_frame_t2': 1, 'hauler_power_core_t2': 1, 'hauler_thruster_array_t2': 1, 'hauler_shield_generator_t2': 1, 'hauler_weapon_mount_t2': 1, 'hauler_sensor_suite_t2': 1, 'hauler_computer_system_t2': 1, 'hauler_life_support_t2': 1},
        "time": 6120,
        "skill_requirement": 8
    },
    "hauler_elite_mk3": {
        "components": {'hauler_hull_frame_t3': 1, 'hauler_power_core_t3': 1, 'hauler_thruster_array_t3': 1, 'hauler_shield_generator_t3': 1, 'hauler_weapon_mount_t3': 1, 'hauler_sensor_suite_t3': 1, 'hauler_computer_system_t3': 1, 'hauler_life_support_t3': 1},
        "time": 9180,
        "skill_requirement": 12
    },
    "hauler_specialized_mk1": {
        "components": {'hauler_hull_frame_t1': 1, 'hauler_power_core_t1': 1, 'hauler_thruster_array_t1': 1, 'hauler_shield_generator_t1': 1, 'hauler_weapon_mount_t1': 1, 'hauler_sensor_suite_t1': 1, 'hauler_computer_system_t1': 1, 'hauler_life_support_t1': 1},
        "time": 3960,
        "skill_requirement": 3
    },
    "hauler_specialized_mk2": {
        "components": {'hauler_hull_frame_t2': 1, 'hauler_power_core_t2': 1, 'hauler_thruster_array_t2': 1, 'hauler_shield_generator_t2': 1, 'hauler_weapon_mount_t2': 1, 'hauler_sensor_suite_t2': 1, 'hauler_computer_system_t2': 1, 'hauler_life_support_t2': 1},
        "time": 7920,
        "skill_requirement": 8
    },
    "hauler_specialized_mk3": {
        "components": {'hauler_hull_frame_t3': 1, 'hauler_power_core_t3': 1, 'hauler_thruster_array_t3': 1, 'hauler_shield_generator_t3': 1, 'hauler_weapon_mount_t3': 1, 'hauler_sensor_suite_t3': 1, 'hauler_computer_system_t3': 1, 'hauler_life_support_t3': 1},
        "time": 11880,
        "skill_requirement": 12
    },
    "cruiser_standard_mk1": {
        "components": {'cruiser_hull_frame_t1': 1, 'cruiser_power_core_t1': 1, 'cruiser_thruster_array_t1': 1, 'cruiser_shield_generator_t1': 1, 'cruiser_weapon_mount_t1': 1, 'cruiser_sensor_suite_t1': 1, 'cruiser_computer_system_t1': 1, 'cruiser_life_support_t1': 1},
        "time": 2400,
        "skill_requirement": 3
    },
    "cruiser_standard_mk2": {
        "components": {'cruiser_hull_frame_t2': 1, 'cruiser_power_core_t2': 1, 'cruiser_thruster_array_t2': 1, 'cruiser_shield_generator_t2': 1, 'cruiser_weapon_mount_t2': 1, 'cruiser_sensor_suite_t2': 1, 'cruiser_computer_system_t2': 1, 'cruiser_life_support_t2': 1},
        "time": 4800,
        "skill_requirement": 8
    },
    "cruiser_standard_mk3": {
        "components": {'cruiser_hull_frame_t3': 1, 'cruiser_power_core_t3': 1, 'cruiser_thruster_array_t3': 1, 'cruiser_shield_generator_t3': 1, 'cruiser_weapon_mount_t3': 1, 'cruiser_sensor_suite_t3': 1, 'cruiser_computer_system_t3': 1, 'cruiser_life_support_t3': 1},
        "time": 7200,
        "skill_requirement": 12
    },
    "cruiser_advanced_mk1": {
        "components": {'cruiser_hull_frame_t1': 1, 'cruiser_power_core_t1': 1, 'cruiser_thruster_array_t1': 1, 'cruiser_shield_generator_t1': 1, 'cruiser_weapon_mount_t1': 1, 'cruiser_sensor_suite_t1': 1, 'cruiser_computer_system_t1': 1, 'cruiser_life_support_t1': 1},
        "time": 3120,
        "skill_requirement": 3
    },
    "cruiser_advanced_mk2": {
        "components": {'cruiser_hull_frame_t2': 1, 'cruiser_power_core_t2': 1, 'cruiser_thruster_array_t2': 1, 'cruiser_shield_generator_t2': 1, 'cruiser_weapon_mount_t2': 1, 'cruiser_sensor_suite_t2': 1, 'cruiser_computer_system_t2': 1, 'cruiser_life_support_t2': 1},
        "time": 6240,
        "skill_requirement": 8
    },
    "cruiser_advanced_mk3": {
        "components": {'cruiser_hull_frame_t3': 1, 'cruiser_power_core_t3': 1, 'cruiser_thruster_array_t3': 1, 'cruiser_shield_generator_t3': 1, 'cruiser_weapon_mount_t3': 1, 'cruiser_sensor_suite_t3': 1, 'cruiser_computer_system_t3': 1, 'cruiser_life_support_t3': 1},
        "time": 9360,
        "skill_requirement": 12
    },
    "cruiser_elite_mk1": {
        "components": {'cruiser_hull_frame_t1': 1, 'cruiser_power_core_t1': 1, 'cruiser_thruster_array_t1': 1, 'cruiser_shield_generator_t1': 1, 'cruiser_weapon_mount_t1': 1, 'cruiser_sensor_suite_t1': 1, 'cruiser_computer_system_t1': 1, 'cruiser_life_support_t1': 1},
        "time": 4080,
        "skill_requirement": 3
    },
    "cruiser_elite_mk2": {
        "components": {'cruiser_hull_frame_t2': 1, 'cruiser_power_core_t2': 1, 'cruiser_thruster_array_t2': 1, 'cruiser_shield_generator_t2': 1, 'cruiser_weapon_mount_t2': 1, 'cruiser_sensor_suite_t2': 1, 'cruiser_computer_system_t2': 1, 'cruiser_life_support_t2': 1},
        "time": 8160,
        "skill_requirement": 8
    },
    "cruiser_elite_mk3": {
        "components": {'cruiser_hull_frame_t3': 1, 'cruiser_power_core_t3': 1, 'cruiser_thruster_array_t3': 1, 'cruiser_shield_generator_t3': 1, 'cruiser_weapon_mount_t3': 1, 'cruiser_sensor_suite_t3': 1, 'cruiser_computer_system_t3': 1, 'cruiser_life_support_t3': 1},
        "time": 12240,
        "skill_requirement": 12
    },
    "cruiser_specialized_mk1": {
        "components": {'cruiser_hull_frame_t1': 1, 'cruiser_power_core_t1': 1, 'cruiser_thruster_array_t1': 1, 'cruiser_shield_generator_t1': 1, 'cruiser_weapon_mount_t1': 1, 'cruiser_sensor_suite_t1': 1, 'cruiser_computer_system_t1': 1, 'cruiser_life_support_t1': 1},
        "time": 5280,
        "skill_requirement": 3
    },
    "cruiser_specialized_mk2": {
        "components": {'cruiser_hull_frame_t2': 1, 'cruiser_power_core_t2': 1, 'cruiser_thruster_array_t2': 1, 'cruiser_shield_generator_t2': 1, 'cruiser_weapon_mount_t2': 1, 'cruiser_sensor_suite_t2': 1, 'cruiser_computer_system_t2': 1, 'cruiser_life_support_t2': 1},
        "time": 10560,
        "skill_requirement": 8
    },
    "cruiser_specialized_mk3": {
        "components": {'cruiser_hull_frame_t3': 1, 'cruiser_power_core_t3': 1, 'cruiser_thruster_array_t3': 1, 'cruiser_shield_generator_t3': 1, 'cruiser_weapon_mount_t3': 1, 'cruiser_sensor_suite_t3': 1, 'cruiser_computer_system_t3': 1, 'cruiser_life_support_t3': 1},
        "time": 15840,
        "skill_requirement": 12
    },
    "destroyer_standard_mk1": {
        "components": {'destroyer_hull_frame_t1': 1, 'destroyer_power_core_t1': 1, 'destroyer_thruster_array_t1': 1, 'destroyer_shield_generator_t1': 1, 'destroyer_weapon_mount_t1': 1, 'destroyer_sensor_suite_t1': 1, 'destroyer_computer_system_t1': 1, 'destroyer_life_support_t1': 1},
        "time": 3000,
        "skill_requirement": 3
    },
    "destroyer_standard_mk2": {
        "components": {'destroyer_hull_frame_t2': 1, 'destroyer_power_core_t2': 1, 'destroyer_thruster_array_t2': 1, 'destroyer_shield_generator_t2': 1, 'destroyer_weapon_mount_t2': 1, 'destroyer_sensor_suite_t2': 1, 'destroyer_computer_system_t2': 1, 'destroyer_life_support_t2': 1},
        "time": 6000,
        "skill_requirement": 8
    },
    "destroyer_standard_mk3": {
        "components": {'destroyer_hull_frame_t3': 1, 'destroyer_power_core_t3': 1, 'destroyer_thruster_array_t3': 1, 'destroyer_shield_generator_t3': 1, 'destroyer_weapon_mount_t3': 1, 'destroyer_sensor_suite_t3': 1, 'destroyer_computer_system_t3': 1, 'destroyer_life_support_t3': 1},
        "time": 9000,
        "skill_requirement": 12
    },
    "destroyer_advanced_mk1": {
        "components": {'destroyer_hull_frame_t1': 1, 'destroyer_power_core_t1': 1, 'destroyer_thruster_array_t1': 1, 'destroyer_shield_generator_t1': 1, 'destroyer_weapon_mount_t1': 1, 'destroyer_sensor_suite_t1': 1, 'destroyer_computer_system_t1': 1, 'destroyer_life_support_t1': 1},
        "time": 3900,
        "skill_requirement": 3
    },
    "destroyer_advanced_mk2": {
        "components": {'destroyer_hull_frame_t2': 1, 'destroyer_power_core_t2': 1, 'destroyer_thruster_array_t2': 1, 'destroyer_shield_generator_t2': 1, 'destroyer_weapon_mount_t2': 1, 'destroyer_sensor_suite_t2': 1, 'destroyer_computer_system_t2': 1, 'destroyer_life_support_t2': 1},
        "time": 7800,
        "skill_requirement": 8
    },
    "destroyer_advanced_mk3": {
        "components": {'destroyer_hull_frame_t3': 1, 'destroyer_power_core_t3': 1, 'destroyer_thruster_array_t3': 1, 'destroyer_shield_generator_t3': 1, 'destroyer_weapon_mount_t3': 1, 'destroyer_sensor_suite_t3': 1, 'destroyer_computer_system_t3': 1, 'destroyer_life_support_t3': 1},
        "time": 11700,
        "skill_requirement": 12
    },
    "destroyer_elite_mk1": {
        "components": {'destroyer_hull_frame_t1': 1, 'destroyer_power_core_t1': 1, 'destroyer_thruster_array_t1': 1, 'destroyer_shield_generator_t1': 1, 'destroyer_weapon_mount_t1': 1, 'destroyer_sensor_suite_t1': 1, 'destroyer_computer_system_t1': 1, 'destroyer_life_support_t1': 1},
        "time": 5100,
        "skill_requirement": 3
    },
    "destroyer_elite_mk2": {
        "components": {'destroyer_hull_frame_t2': 1, 'destroyer_power_core_t2': 1, 'destroyer_thruster_array_t2': 1, 'destroyer_shield_generator_t2': 1, 'destroyer_weapon_mount_t2': 1, 'destroyer_sensor_suite_t2': 1, 'destroyer_computer_system_t2': 1, 'destroyer_life_support_t2': 1},
        "time": 10200,
        "skill_requirement": 8
    },
    "destroyer_elite_mk3": {
        "components": {'destroyer_hull_frame_t3': 1, 'destroyer_power_core_t3': 1, 'destroyer_thruster_array_t3': 1, 'destroyer_shield_generator_t3': 1, 'destroyer_weapon_mount_t3': 1, 'destroyer_sensor_suite_t3': 1, 'destroyer_computer_system_t3': 1, 'destroyer_life_support_t3': 1},
        "time": 15300,
        "skill_requirement": 12
    },
    "destroyer_specialized_mk1": {
        "components": {'destroyer_hull_frame_t1': 1, 'destroyer_power_core_t1': 1, 'destroyer_thruster_array_t1': 1, 'destroyer_shield_generator_t1': 1, 'destroyer_weapon_mount_t1': 1, 'destroyer_sensor_suite_t1': 1, 'destroyer_computer_system_t1': 1, 'destroyer_life_support_t1': 1},
        "time": 6600,
        "skill_requirement": 3
    },
    "destroyer_specialized_mk2": {
        "components": {'destroyer_hull_frame_t2': 1, 'destroyer_power_core_t2': 1, 'destroyer_thruster_array_t2': 1, 'destroyer_shield_generator_t2': 1, 'destroyer_weapon_mount_t2': 1, 'destroyer_sensor_suite_t2': 1, 'destroyer_computer_system_t2': 1, 'destroyer_life_support_t2': 1},
        "time": 13200,
        "skill_requirement": 8
    },
    "destroyer_specialized_mk3": {
        "components": {'destroyer_hull_frame_t3': 1, 'destroyer_power_core_t3': 1, 'destroyer_thruster_array_t3': 1, 'destroyer_shield_generator_t3': 1, 'destroyer_weapon_mount_t3': 1, 'destroyer_sensor_suite_t3': 1, 'destroyer_computer_system_t3': 1, 'destroyer_life_support_t3': 1},
        "time": 19800,
        "skill_requirement": 12
    },
    "battleship_standard_mk1": {
        "components": {'battleship_hull_frame_t1': 1, 'battleship_power_core_t1': 1, 'battleship_thruster_array_t1': 1, 'battleship_shield_generator_t1': 1, 'battleship_weapon_mount_t1': 1, 'battleship_sensor_suite_t1': 1, 'battleship_computer_system_t1': 1, 'battleship_life_support_t1': 1},
        "time": 4200,
        "skill_requirement": 3
    },
    "battleship_standard_mk2": {
        "components": {'battleship_hull_frame_t2': 1, 'battleship_power_core_t2': 1, 'battleship_thruster_array_t2': 1, 'battleship_shield_generator_t2': 1, 'battleship_weapon_mount_t2': 1, 'battleship_sensor_suite_t2': 1, 'battleship_computer_system_t2': 1, 'battleship_life_support_t2': 1},
        "time": 8400,
        "skill_requirement": 8
    },
    "battleship_standard_mk3": {
        "components": {'battleship_hull_frame_t3': 1, 'battleship_power_core_t3': 1, 'battleship_thruster_array_t3': 1, 'battleship_shield_generator_t3': 1, 'battleship_weapon_mount_t3': 1, 'battleship_sensor_suite_t3': 1, 'battleship_computer_system_t3': 1, 'battleship_life_support_t3': 1},
        "time": 12600,
        "skill_requirement": 12
    },
    "battleship_advanced_mk1": {
        "components": {'battleship_hull_frame_t1': 1, 'battleship_power_core_t1': 1, 'battleship_thruster_array_t1': 1, 'battleship_shield_generator_t1': 1, 'battleship_weapon_mount_t1': 1, 'battleship_sensor_suite_t1': 1, 'battleship_computer_system_t1': 1, 'battleship_life_support_t1': 1},
        "time": 5460,
        "skill_requirement": 3
    },
    "battleship_advanced_mk2": {
        "components": {'battleship_hull_frame_t2': 1, 'battleship_power_core_t2': 1, 'battleship_thruster_array_t2': 1, 'battleship_shield_generator_t2': 1, 'battleship_weapon_mount_t2': 1, 'battleship_sensor_suite_t2': 1, 'battleship_computer_system_t2': 1, 'battleship_life_support_t2': 1},
        "time": 10920,
        "skill_requirement": 8
    },
    "battleship_advanced_mk3": {
        "components": {'battleship_hull_frame_t3': 1, 'battleship_power_core_t3': 1, 'battleship_thruster_array_t3': 1, 'battleship_shield_generator_t3': 1, 'battleship_weapon_mount_t3': 1, 'battleship_sensor_suite_t3': 1, 'battleship_computer_system_t3': 1, 'battleship_life_support_t3': 1},
        "time": 16380,
        "skill_requirement": 12
    },
    "battleship_elite_mk1": {
        "components": {'battleship_hull_frame_t1': 1, 'battleship_power_core_t1': 1, 'battleship_thruster_array_t1': 1, 'battleship_shield_generator_t1': 1, 'battleship_weapon_mount_t1': 1, 'battleship_sensor_suite_t1': 1, 'battleship_computer_system_t1': 1, 'battleship_life_support_t1': 1},
        "time": 7140,
        "skill_requirement": 3
    },
    "battleship_elite_mk2": {
        "components": {'battleship_hull_frame_t2': 1, 'battleship_power_core_t2': 1, 'battleship_thruster_array_t2': 1, 'battleship_shield_generator_t2': 1, 'battleship_weapon_mount_t2': 1, 'battleship_sensor_suite_t2': 1, 'battleship_computer_system_t2': 1, 'battleship_life_support_t2': 1},
        "time": 14280,
        "skill_requirement": 8
    },
    "battleship_elite_mk3": {
        "components": {'battleship_hull_frame_t3': 1, 'battleship_power_core_t3': 1, 'battleship_thruster_array_t3': 1, 'battleship_shield_generator_t3': 1, 'battleship_weapon_mount_t3': 1, 'battleship_sensor_suite_t3': 1, 'battleship_computer_system_t3': 1, 'battleship_life_support_t3': 1},
        "time": 21420,
        "skill_requirement": 12
    },
    "battleship_specialized_mk1": {
        "components": {'battleship_hull_frame_t1': 1, 'battleship_power_core_t1': 1, 'battleship_thruster_array_t1': 1, 'battleship_shield_generator_t1': 1, 'battleship_weapon_mount_t1': 1, 'battleship_sensor_suite_t1': 1, 'battleship_computer_system_t1': 1, 'battleship_life_support_t1': 1},
        "time": 9240,
        "skill_requirement": 3
    },
    "battleship_specialized_mk2": {
        "components": {'battleship_hull_frame_t2': 1, 'battleship_power_core_t2': 1, 'battleship_thruster_array_t2': 1, 'battleship_shield_generator_t2': 1, 'battleship_weapon_mount_t2': 1, 'battleship_sensor_suite_t2': 1, 'battleship_computer_system_t2': 1, 'battleship_life_support_t2': 1},
        "time": 18480,
        "skill_requirement": 8
    },
    "battleship_specialized_mk3": {
        "components": {'battleship_hull_frame_t3': 1, 'battleship_power_core_t3': 1, 'battleship_thruster_array_t3': 1, 'battleship_shield_generator_t3': 1, 'battleship_weapon_mount_t3': 1, 'battleship_sensor_suite_t3': 1, 'battleship_computer_system_t3': 1, 'battleship_life_support_t3': 1},
        "time": 27720,
        "skill_requirement": 12
    },
    "carrier_standard_mk1": {
        "components": {'carrier_hull_frame_t1': 1, 'carrier_power_core_t1': 1, 'carrier_thruster_array_t1': 1, 'carrier_shield_generator_t1': 1, 'carrier_weapon_mount_t1': 1, 'carrier_sensor_suite_t1': 1, 'carrier_computer_system_t1': 1, 'carrier_life_support_t1': 1},
        "time": 3600,
        "skill_requirement": 3
    },
    "carrier_standard_mk2": {
        "components": {'carrier_hull_frame_t2': 1, 'carrier_power_core_t2': 1, 'carrier_thruster_array_t2': 1, 'carrier_shield_generator_t2': 1, 'carrier_weapon_mount_t2': 1, 'carrier_sensor_suite_t2': 1, 'carrier_computer_system_t2': 1, 'carrier_life_support_t2': 1},
        "time": 7200,
        "skill_requirement": 8
    },
    "carrier_standard_mk3": {
        "components": {'carrier_hull_frame_t3': 1, 'carrier_power_core_t3': 1, 'carrier_thruster_array_t3': 1, 'carrier_shield_generator_t3': 1, 'carrier_weapon_mount_t3': 1, 'carrier_sensor_suite_t3': 1, 'carrier_computer_system_t3': 1, 'carrier_life_support_t3': 1},
        "time": 10800,
        "skill_requirement": 12
    },
    "carrier_advanced_mk1": {
        "components": {'carrier_hull_frame_t1': 1, 'carrier_power_core_t1': 1, 'carrier_thruster_array_t1': 1, 'carrier_shield_generator_t1': 1, 'carrier_weapon_mount_t1': 1, 'carrier_sensor_suite_t1': 1, 'carrier_computer_system_t1': 1, 'carrier_life_support_t1': 1},
        "time": 4680,
        "skill_requirement": 3
    },
    "carrier_advanced_mk2": {
        "components": {'carrier_hull_frame_t2': 1, 'carrier_power_core_t2': 1, 'carrier_thruster_array_t2': 1, 'carrier_shield_generator_t2': 1, 'carrier_weapon_mount_t2': 1, 'carrier_sensor_suite_t2': 1, 'carrier_computer_system_t2': 1, 'carrier_life_support_t2': 1},
        "time": 9360,
        "skill_requirement": 8
    },
    "carrier_advanced_mk3": {
        "components": {'carrier_hull_frame_t3': 1, 'carrier_power_core_t3': 1, 'carrier_thruster_array_t3': 1, 'carrier_shield_generator_t3': 1, 'carrier_weapon_mount_t3': 1, 'carrier_sensor_suite_t3': 1, 'carrier_computer_system_t3': 1, 'carrier_life_support_t3': 1},
        "time": 14040,
        "skill_requirement": 12
    },
    "carrier_elite_mk1": {
        "components": {'carrier_hull_frame_t1': 1, 'carrier_power_core_t1': 1, 'carrier_thruster_array_t1': 1, 'carrier_shield_generator_t1': 1, 'carrier_weapon_mount_t1': 1, 'carrier_sensor_suite_t1': 1, 'carrier_computer_system_t1': 1, 'carrier_life_support_t1': 1},
        "time": 6120,
        "skill_requirement": 3
    },
    "carrier_elite_mk2": {
        "components": {'carrier_hull_frame_t2': 1, 'carrier_power_core_t2': 1, 'carrier_thruster_array_t2': 1, 'carrier_shield_generator_t2': 1, 'carrier_weapon_mount_t2': 1, 'carrier_sensor_suite_t2': 1, 'carrier_computer_system_t2': 1, 'carrier_life_support_t2': 1},
        "time": 12240,
        "skill_requirement": 8
    },
    "carrier_elite_mk3": {
        "components": {'carrier_hull_frame_t3': 1, 'carrier_power_core_t3': 1, 'carrier_thruster_array_t3': 1, 'carrier_shield_generator_t3': 1, 'carrier_weapon_mount_t3': 1, 'carrier_sensor_suite_t3': 1, 'carrier_computer_system_t3': 1, 'carrier_life_support_t3': 1},
        "time": 18360,
        "skill_requirement": 12
    },
    "carrier_specialized_mk1": {
        "components": {'carrier_hull_frame_t1': 1, 'carrier_power_core_t1': 1, 'carrier_thruster_array_t1': 1, 'carrier_shield_generator_t1': 1, 'carrier_weapon_mount_t1': 1, 'carrier_sensor_suite_t1': 1, 'carrier_computer_system_t1': 1, 'carrier_life_support_t1': 1},
        "time": 7920,
        "skill_requirement": 3
    },
    "carrier_specialized_mk2": {
        "components": {'carrier_hull_frame_t2': 1, 'carrier_power_core_t2': 1, 'carrier_thruster_array_t2': 1, 'carrier_shield_generator_t2': 1, 'carrier_weapon_mount_t2': 1, 'carrier_sensor_suite_t2': 1, 'carrier_computer_system_t2': 1, 'carrier_life_support_t2': 1},
        "time": 15840,
        "skill_requirement": 8
    },
    "carrier_specialized_mk3": {
        "components": {'carrier_hull_frame_t3': 1, 'carrier_power_core_t3': 1, 'carrier_thruster_array_t3': 1, 'carrier_shield_generator_t3': 1, 'carrier_weapon_mount_t3': 1, 'carrier_sensor_suite_t3': 1, 'carrier_computer_system_t3': 1, 'carrier_life_support_t3': 1},
        "time": 23760,
        "skill_requirement": 12
    },
    "refinery_standard_mk1": {
        "components": {'refinery_hull_frame_t1': 1, 'refinery_power_core_t1': 1, 'refinery_thruster_array_t1': 1, 'refinery_shield_generator_t1': 1, 'refinery_weapon_mount_t1': 1, 'refinery_sensor_suite_t1': 1, 'refinery_computer_system_t1': 1, 'refinery_life_support_t1': 1},
        "time": 4800,
        "skill_requirement": 3
    },
    "refinery_standard_mk2": {
        "components": {'refinery_hull_frame_t2': 1, 'refinery_power_core_t2': 1, 'refinery_thruster_array_t2': 1, 'refinery_shield_generator_t2': 1, 'refinery_weapon_mount_t2': 1, 'refinery_sensor_suite_t2': 1, 'refinery_computer_system_t2': 1, 'refinery_life_support_t2': 1},
        "time": 9600,
        "skill_requirement": 8
    },
    "refinery_standard_mk3": {
        "components": {'refinery_hull_frame_t3': 1, 'refinery_power_core_t3': 1, 'refinery_thruster_array_t3': 1, 'refinery_shield_generator_t3': 1, 'refinery_weapon_mount_t3': 1, 'refinery_sensor_suite_t3': 1, 'refinery_computer_system_t3': 1, 'refinery_life_support_t3': 1},
        "time": 14400,
        "skill_requirement": 12
    },
    "refinery_advanced_mk1": {
        "components": {'refinery_hull_frame_t1': 1, 'refinery_power_core_t1': 1, 'refinery_thruster_array_t1': 1, 'refinery_shield_generator_t1': 1, 'refinery_weapon_mount_t1': 1, 'refinery_sensor_suite_t1': 1, 'refinery_computer_system_t1': 1, 'refinery_life_support_t1': 1},
        "time": 6240,
        "skill_requirement": 3
    },
    "refinery_advanced_mk2": {
        "components": {'refinery_hull_frame_t2': 1, 'refinery_power_core_t2': 1, 'refinery_thruster_array_t2': 1, 'refinery_shield_generator_t2': 1, 'refinery_weapon_mount_t2': 1, 'refinery_sensor_suite_t2': 1, 'refinery_computer_system_t2': 1, 'refinery_life_support_t2': 1},
        "time": 12480,
        "skill_requirement": 8
    },
    "refinery_advanced_mk3": {
        "components": {'refinery_hull_frame_t3': 1, 'refinery_power_core_t3': 1, 'refinery_thruster_array_t3': 1, 'refinery_shield_generator_t3': 1, 'refinery_weapon_mount_t3': 1, 'refinery_sensor_suite_t3': 1, 'refinery_computer_system_t3': 1, 'refinery_life_support_t3': 1},
        "time": 18720,
        "skill_requirement": 12
    },
    "refinery_elite_mk1": {
        "components": {'refinery_hull_frame_t1': 1, 'refinery_power_core_t1': 1, 'refinery_thruster_array_t1': 1, 'refinery_shield_generator_t1': 1, 'refinery_weapon_mount_t1': 1, 'refinery_sensor_suite_t1': 1, 'refinery_computer_system_t1': 1, 'refinery_life_support_t1': 1},
        "time": 8160,
        "skill_requirement": 3
    },
    "refinery_elite_mk2": {
        "components": {'refinery_hull_frame_t2': 1, 'refinery_power_core_t2': 1, 'refinery_thruster_array_t2': 1, 'refinery_shield_generator_t2': 1, 'refinery_weapon_mount_t2': 1, 'refinery_sensor_suite_t2': 1, 'refinery_computer_system_t2': 1, 'refinery_life_support_t2': 1},
        "time": 16320,
        "skill_requirement": 8
    },
    "refinery_elite_mk3": {
        "components": {'refinery_hull_frame_t3': 1, 'refinery_power_core_t3': 1, 'refinery_thruster_array_t3': 1, 'refinery_shield_generator_t3': 1, 'refinery_weapon_mount_t3': 1, 'refinery_sensor_suite_t3': 1, 'refinery_computer_system_t3': 1, 'refinery_life_support_t3': 1},
        "time": 24480,
        "skill_requirement": 12
    },
    "refinery_specialized_mk1": {
        "components": {'refinery_hull_frame_t1': 1, 'refinery_power_core_t1': 1, 'refinery_thruster_array_t1': 1, 'refinery_shield_generator_t1': 1, 'refinery_weapon_mount_t1': 1, 'refinery_sensor_suite_t1': 1, 'refinery_computer_system_t1': 1, 'refinery_life_support_t1': 1},
        "time": 10560,
        "skill_requirement": 3
    },
    "refinery_specialized_mk2": {
        "components": {'refinery_hull_frame_t2': 1, 'refinery_power_core_t2': 1, 'refinery_thruster_array_t2': 1, 'refinery_shield_generator_t2': 1, 'refinery_weapon_mount_t2': 1, 'refinery_sensor_suite_t2': 1, 'refinery_computer_system_t2': 1, 'refinery_life_support_t2': 1},
        "time": 21120,
        "skill_requirement": 8
    },
    "refinery_specialized_mk3": {
        "components": {'refinery_hull_frame_t3': 1, 'refinery_power_core_t3': 1, 'refinery_thruster_array_t3': 1, 'refinery_shield_generator_t3': 1, 'refinery_weapon_mount_t3': 1, 'refinery_sensor_suite_t3': 1, 'refinery_computer_system_t3': 1, 'refinery_life_support_t3': 1},
        "time": 31680,
        "skill_requirement": 12
    },
}

# Total ship recipes: 96

# ============= COMMODITIES (Trading Goods) =============
# 122 commodities for market trading with dynamic prices
# Prices fluctuate based on supply/demand and player actions
COMMODITIES = {
    # Food & Nutrition (15 items)
    "protein_rations": {"name": "Protein Rations", "description": "High-protein emergency food", "base_price": 15, "category": "food", "volume": 1.0, "volatility": 0.3},
    "carb_blocks": {"name": "Carbohydrate Blocks", "description": "Energy-dense food cubes", "base_price": 12, "category": "food", "volume": 0.8, "volatility": 0.3},
    "vitamin_supplements": {"name": "Vitamin Supplements", "description": "Essential micronutrients", "base_price": 25, "category": "food", "volume": 0.2, "volatility": 0.2},
    "hydroponic_vegetables": {"name": "Hydroponic Vegetables", "description": "Fresh-grown produce", "base_price": 45, "category": "food", "volume": 2.0, "volatility": 0.5},
    "synthetic_meat": {"name": "Synthetic Meat", "description": "Lab-grown protein", "base_price": 60, "category": "food", "volume": 1.5, "volatility": 0.4},
    "freeze_dried_meals": {"name": "Freeze-Dried Meals", "description": "Long-term storage food", "base_price": 20, "category": "food", "volume": 0.5, "volatility": 0.2},
    "algae_paste": {"name": "Algae Paste", "description": "Nutritious algae product", "base_price": 8, "category": "food", "volume": 1.0, "volatility": 0.4},
    "nutrient_paste": {"name": "Nutrient Paste", "description": "Complete meal replacement", "base_price": 10, "category": "food", "volume": 0.6, "volatility": 0.3},
    "coffee_substitute": {"name": "Coffee Substitute", "description": "Stimulant beverage", "base_price": 35, "category": "food", "volume": 0.3, "volatility": 0.6},
    "flavoring_agents": {"name": "Flavoring Agents", "description": "Food taste enhancers", "base_price": 18, "category": "food", "volume": 0.1, "volatility": 0.4},
    "preserved_fruits": {"name": "Preserved Fruits", "description": "Dried and sealed fruits", "base_price": 30, "category": "food", "volume": 0.8, "volatility": 0.5},
    "grain_stores": {"name": "Grain Stores", "description": "Wheat and rice reserves", "base_price": 22, "category": "food", "volume": 5.0, "volatility": 0.3},
    "spice_packets": {"name": "Spice Packets", "description": "Flavor variety packs", "base_price": 40, "category": "food", "volume": 0.1, "volatility": 0.5},
    "honey_extract": {"name": "Honey Extract", "description": "Natural sweetener", "base_price": 55, "category": "food", "volume": 0.4, "volatility": 0.6},
    "protein_powder": {"name": "Protein Powder", "description": "Muscle-building supplement", "base_price": 28, "category": "food", "volume": 0.5, "volatility": 0.3},

    # Medical Supplies (15 items)
    "antibiotics": {"name": "Antibiotics", "description": "Infection treatment", "base_price": 80, "category": "medical", "volume": 0.2, "volatility": 0.4},
    "painkillers": {"name": "Painkillers", "description": "Pain management drugs", "base_price": 45, "category": "medical", "volume": 0.1, "volatility": 0.3},
    "stim_packs": {"name": "Stim Packs", "description": "Emergency stimulants", "base_price": 120, "category": "medical", "volume": 0.1, "volatility": 0.5},
    "surgical_kits": {"name": "Surgical Kits", "description": "Medical procedure supplies", "base_price": 200, "category": "medical", "volume": 2.0, "volatility": 0.3},
    "bandages": {"name": "Bandages", "description": "Wound dressing materials", "base_price": 15, "category": "medical", "volume": 0.5, "volatility": 0.2},
    "bio_gel": {"name": "Bio-Regeneration Gel", "description": "Tissue repair gel", "base_price": 150, "category": "medical", "volume": 0.3, "volatility": 0.5},
    "med_scanners": {"name": "Medical Scanners", "description": "Diagnostic equipment", "base_price": 300, "category": "medical", "volume": 1.0, "volatility": 0.3},
    "blood_plasma": {"name": "Blood Plasma", "description": "Transfusion supplies", "base_price": 90, "category": "medical", "volume": 0.5, "volatility": 0.6},
    "antivenom": {"name": "Antivenom Serum", "description": "Toxin neutralizer", "base_price": 110, "category": "medical", "volume": 0.2, "volatility": 0.7},
    "immunoboosters": {"name": "Immunoboosters", "description": "Immune enhancement", "base_price": 65, "category": "medical", "volume": 0.1, "volatility": 0.4},
    "radiation_meds": {"name": "Radiation Treatment", "description": "Anti-radiation drugs", "base_price": 175, "category": "medical", "volume": 0.2, "volatility": 0.5},
    "cryogenic_fluid": {"name": "Cryogenic Medical Fluid", "description": "Preservation liquid", "base_price": 250, "category": "medical", "volume": 1.0, "volatility": 0.4},
    "nano_repair_bots": {"name": "Nano Repair Bots", "description": "Cellular repair nanites", "base_price": 400, "category": "medical", "volume": 0.1, "volatility": 0.6},
    "organ_preservatives": {"name": "Organ Preservatives", "description": "Transplant storage", "base_price": 180, "category": "medical", "volume": 0.5, "volatility": 0.5},
    "anti_toxins": {"name": "Anti-Toxin Compounds", "description": "Poison countermeasures", "base_price": 95, "category": "medical", "volume": 0.2, "volatility": 0.4},

    # Scientific Equipment (14 items)
    "spectrometers": {"name": "Spectrometers", "description": "Analysis instruments", "base_price": 500, "category": "science", "volume": 2.0, "volatility": 0.3},
    "petri_dishes": {"name": "Petri Dishes", "description": "Culture containers", "base_price": 20, "category": "science", "volume": 0.5, "volatility": 0.2},
    "microscopes": {"name": "Electron Microscopes", "description": "Advanced imaging", "base_price": 800, "category": "science", "volume": 3.0, "volatility": 0.3},
    "lab_chemicals": {"name": "Laboratory Chemicals", "description": "Research reagents", "base_price": 75, "category": "science", "volume": 1.0, "volatility": 0.4},
    "test_tubes": {"name": "Test Tubes", "description": "Sample containers", "base_price": 5, "category": "science", "volume": 0.2, "volatility": 0.2},
    "centrifuges": {"name": "Centrifuges", "description": "Sample separation", "base_price": 350, "category": "science", "volume": 2.5, "volatility": 0.3},
    "dna_sequencers": {"name": "DNA Sequencers", "description": "Genetic analysis", "base_price": 1200, "category": "science", "volume": 2.0, "volatility": 0.4},
    "research_computers": {"name": "Research Computers", "description": "Data processing units", "base_price": 600, "category": "science", "volume": 1.5, "volatility": 0.3},
    "specimen_slides": {"name": "Specimen Slides", "description": "Microscopy samples", "base_price": 15, "category": "science", "volume": 0.1, "volatility": 0.2},
    "pipettes": {"name": "Precision Pipettes", "description": "Liquid measurement", "base_price": 40, "category": "science", "volume": 0.2, "volatility": 0.2},
    "autoclave_supplies": {"name": "Autoclave Supplies", "description": "Sterilization materials", "base_price": 85, "category": "science", "volume": 1.0, "volatility": 0.3},
    "oscilloscopes": {"name": "Oscilloscopes", "description": "Wave measurement", "base_price": 450, "category": "science", "volume": 1.5, "volatility": 0.3},
    "chromatography_kits": {"name": "Chromatography Kits", "description": "Compound separation", "base_price": 320, "category": "science", "volume": 1.0, "volatility": 0.3},
    "radiation_detectors": {"name": "Radiation Detectors", "description": "Safety monitoring", "base_price": 280, "category": "science", "volume": 0.5, "volatility": 0.4},

    # Life Support (12 items)
    "oxygen_canisters": {"name": "Oxygen Canisters", "description": "Breathable air supply", "base_price": 50, "category": "life_support", "volume": 2.0, "volatility": 0.4},
    "co2_scrubbers": {"name": "CO2 Scrubbers", "description": "Air purification", "base_price": 150, "category": "life_support", "volume": 1.5, "volatility": 0.3},
    "water_filters": {"name": "Water Filters", "description": "Purification membranes", "base_price": 90, "category": "life_support", "volume": 0.5, "volatility": 0.3},
    "air_recyclers": {"name": "Air Recyclers", "description": "Atmosphere processing", "base_price": 400, "category": "life_support", "volume": 3.0, "volatility": 0.3},
    "thermal_regulators": {"name": "Thermal Regulators", "description": "Temperature control", "base_price": 180, "category": "life_support", "volume": 1.0, "volatility": 0.3},
    "humidity_controllers": {"name": "Humidity Controllers", "description": "Moisture management", "base_price": 110, "category": "life_support", "volume": 0.8, "volatility": 0.3},
    "emergency_suits": {"name": "Emergency EVA Suits", "description": "Survival gear", "base_price": 500, "category": "life_support", "volume": 5.0, "volatility": 0.4},
    "life_support_cores": {"name": "Life Support Cores", "description": "Critical systems", "base_price": 1000, "category": "life_support", "volume": 4.0, "volatility": 0.5},
    "breathing_masks": {"name": "Breathing Masks", "description": "Personal filtration", "base_price": 35, "category": "life_support", "volume": 0.3, "volatility": 0.3},
    "pressure_seals": {"name": "Pressure Seals", "description": "Airlock components", "base_price": 75, "category": "life_support", "volume": 0.5, "volatility": 0.3},
    "atmosphere_sensors": {"name": "Atmosphere Sensors", "description": "Air quality monitoring", "base_price": 120, "category": "life_support", "volume": 0.3, "volatility": 0.3},
    "oxygen_generators": {"name": "Oxygen Generators", "description": "O2 production units", "base_price": 650, "category": "life_support", "volume": 4.0, "volatility": 0.4},

    # Luxury Goods (13 items)
    "fine_wines": {"name": "Fine Wines", "description": "Aged alcoholic beverages", "base_price": 200, "category": "luxury", "volume": 0.5, "volatility": 0.7},
    "cigars": {"name": "Premium Cigars", "description": "Tobacco products", "base_price": 150, "category": "luxury", "volume": 0.1, "volatility": 0.6},
    "jewelry": {"name": "Jewelry", "description": "Ornamental accessories", "base_price": 500, "category": "luxury", "volume": 0.1, "volatility": 0.8},
    "artwork": {"name": "Artwork", "description": "Cultural pieces", "base_price": 800, "category": "luxury", "volume": 1.0, "volatility": 0.9},
    "perfumes": {"name": "Exotic Perfumes", "description": "Fragrance compounds", "base_price": 180, "category": "luxury", "volume": 0.1, "volatility": 0.6},
    "silk_fabrics": {"name": "Silk Fabrics", "description": "Premium textiles", "base_price": 250, "category": "luxury", "volume": 0.5, "volatility": 0.7},
    "chocolate": {"name": "Chocolate", "description": "Cacao confections", "base_price": 120, "category": "luxury", "volume": 0.2, "volatility": 0.8},
    "musical_instruments": {"name": "Musical Instruments", "description": "Entertainment tools", "base_price": 400, "category": "luxury", "volume": 2.0, "volatility": 0.6},
    "rare_books": {"name": "Rare Books", "description": "Historical texts", "base_price": 350, "category": "luxury", "volume": 0.5, "volatility": 0.7},
    "gemstones": {"name": "Gemstones", "description": "Decorative minerals", "base_price": 1000, "category": "luxury", "volume": 0.1, "volatility": 1.0},
    "designer_clothing": {"name": "Designer Clothing", "description": "Fashion items", "base_price": 300, "category": "luxury", "volume": 0.5, "volatility": 0.7},
    "holographic_art": {"name": "Holographic Art", "description": "Digital displays", "base_price": 600, "category": "luxury", "volume": 0.3, "volatility": 0.8},
    "exotic_pets": {"name": "Exotic Pets", "description": "Companion animals", "base_price": 450, "category": "luxury", "volume": 1.0, "volatility": 0.9},

    # Research Materials (13 items)
    "stellar_samples": {"name": "Stellar Material Samples", "description": "Star matter", "base_price": 2000, "category": "research", "volume": 0.1, "volatility": 0.8},
    "asteroid_cores": {"name": "Asteroid Core Samples", "description": "Rare minerals", "base_price": 800, "category": "research", "volume": 1.0, "volatility": 0.6},
    "alien_artifacts": {"name": "Alien Artifacts", "description": "Unknown technology", "base_price": 5000, "category": "research", "volume": 0.5, "volatility": 1.2},
    "dark_matter_traces": {"name": "Dark Matter Traces", "description": "Exotic particles", "base_price": 3500, "category": "research", "volume": 0.1, "volatility": 1.0},
    "antimatter_samples": {"name": "Antimatter Samples", "description": "High-energy matter", "base_price": 4000, "category": "research", "volume": 0.1, "volatility": 0.9},
    "exotic_isotopes": {"name": "Exotic Isotopes", "description": "Rare elements", "base_price": 1500, "category": "research", "volume": 0.2, "volatility": 0.7},
    "crystalline_formations": {"name": "Crystalline Formations", "description": "Natural structures", "base_price": 600, "category": "research", "volume": 0.5, "volatility": 0.5},
    "bio_samples": {"name": "Biological Samples", "description": "Living specimens", "base_price": 400, "category": "research", "volume": 0.3, "volatility": 0.6},
    "geological_samples": {"name": "Geological Samples", "description": "Planet core materials", "base_price": 250, "category": "research", "volume": 2.0, "volatility": 0.4},
    "atmospheric_samples": {"name": "Atmospheric Samples", "description": "Gas mixtures", "base_price": 180, "category": "research", "volume": 0.5, "volatility": 0.5},
    "radiation_samples": {"name": "Radiation Samples", "description": "Energetic particles", "base_price": 900, "category": "research", "volume": 0.2, "volatility": 0.6},
    "plasma_samples": {"name": "Plasma Samples", "description": "Ionized matter", "base_price": 700, "category": "research", "volume": 0.3, "volatility": 0.6},
    "nebula_dust": {"name": "Nebula Dust", "description": "Interstellar particles", "base_price": 1200, "category": "research", "volume": 0.2, "volatility": 0.7},

    # Technology & Electronics (10 items)
    "memory_chips": {"name": "Memory Chips", "description": "Data storage", "base_price": 100, "category": "technology", "volume": 0.1, "volatility": 0.4},
    "processors": {"name": "Quantum Processors", "description": "Computing cores", "base_price": 500, "category": "technology", "volume": 0.1, "volatility": 0.5},
    "power_cells": {"name": "Power Cells", "description": "Energy storage", "base_price": 80, "category": "technology", "volume": 0.5, "volatility": 0.3},
    "holographic_displays": {"name": "Holographic Displays", "description": "Projection tech", "base_price": 350, "category": "technology", "volume": 0.5, "volatility": 0.4},
    "communication_arrays": {"name": "Communication Arrays", "description": "Signal equipment", "base_price": 600, "category": "technology", "volume": 1.0, "volatility": 0.4},
    "sensor_packages": {"name": "Sensor Packages", "description": "Detection systems", "base_price": 400, "category": "technology", "volume": 0.5, "volatility": 0.4},
    "encryption_keys": {"name": "Encryption Keys", "description": "Security hardware", "base_price": 250, "category": "technology", "volume": 0.1, "volatility": 0.6},
    "ai_cores": {"name": "AI Cores", "description": "Artificial intelligence", "base_price": 2000, "category": "technology", "volume": 0.3, "volatility": 0.7},
    "neural_interfaces": {"name": "Neural Interfaces", "description": "Brain-computer links", "base_price": 1500, "category": "technology", "volume": 0.2, "volatility": 0.6},
    "gravity_generators": {"name": "Gravity Generators", "description": "Artificial gravity", "base_price": 3000, "category": "technology", "volume": 5.0, "volatility": 0.5},

    # Energy Products (6 items)
    "fusion_pellets": {"name": "Fusion Pellets", "description": "Reactor fuel", "base_price": 200, "category": "energy", "volume": 0.5, "volatility": 0.5},
    "antimatter_cells": {"name": "Antimatter Cells", "description": "High-density energy", "base_price": 5000, "category": "energy", "volume": 0.2, "volatility": 0.8},
    "plasma_batteries": {"name": "Plasma Batteries", "description": "Energy storage", "base_price": 300, "category": "energy", "volume": 1.0, "volatility": 0.4},
    "solar_arrays": {"name": "Solar Arrays", "description": "Energy collectors", "base_price": 800, "category": "energy", "volume": 3.0, "volatility": 0.4},
    "thermal_cores": {"name": "Thermal Cores", "description": "Heat batteries", "base_price": 150, "category": "energy", "volume": 1.0, "volatility": 0.3},
    "hydrogen_fuel": {"name": "Hydrogen Fuel", "description": "Chemical energy", "base_price": 60, "category": "energy", "volume": 2.0, "volatility": 0.4},

    # Textiles & Materials (6 items)
    "carbon_fiber": {"name": "Carbon Fiber", "description": "Strong lightweight material", "base_price": 120, "category": "materials", "volume": 1.0, "volatility": 0.3},
    "smart_fabrics": {"name": "Smart Fabrics", "description": "Adaptive textiles", "base_price": 200, "category": "materials", "volume": 0.5, "volatility": 0.4},
    "insulation_foam": {"name": "Insulation Foam", "description": "Thermal protection", "base_price": 45, "category": "materials", "volume": 2.0, "volatility": 0.3},
    "protective_clothing": {"name": "Protective Clothing", "description": "Work gear", "base_price": 90, "category": "materials", "volume": 1.0, "volatility": 0.3},
    "blankets": {"name": "Thermal Blankets", "description": "Heat retention", "base_price": 25, "category": "materials", "volume": 0.5, "volatility": 0.3},
    "rope_cables": {"name": "Rope & Cables", "description": "Utility lines", "base_price": 30, "category": "materials", "volume": 1.0, "volatility": 0.2},

    # Entertainment & Culture (6 items)
    "virtual_reality_games": {"name": "VR Games", "description": "Entertainment software", "base_price": 80, "category": "entertainment", "volume": 0.1, "volatility": 0.5},
    "music_libraries": {"name": "Music Libraries", "description": "Digital collections", "base_price": 60, "category": "entertainment", "volume": 0.1, "volatility": 0.4},
    "movie_databases": {"name": "Movie Databases", "description": "Video entertainment", "base_price": 70, "category": "entertainment", "volume": 0.1, "volatility": 0.4},
    "board_games": {"name": "Board Games", "description": "Physical games", "base_price": 40, "category": "entertainment", "volume": 0.5, "volatility": 0.4},
    "sports_equipment": {"name": "Sports Equipment", "description": "Physical activity gear", "base_price": 100, "category": "entertainment", "volume": 2.0, "volatility": 0.4},
    "books_digital": {"name": "Digital Books", "description": "E-literature", "base_price": 20, "category": "entertainment", "volume": 0.1, "volatility": 0.3},

    # Agricultural (6 items)
    "seeds_variety": {"name": "Seed Variety Packs", "description": "Crop starters", "base_price": 50, "category": "agricultural", "volume": 0.2, "volatility": 0.4},
    "fertilizers": {"name": "Fertilizers", "description": "Growth enhancers", "base_price": 35, "category": "agricultural", "volume": 2.0, "volatility": 0.3},
    "soil_supplements": {"name": "Soil Supplements", "description": "Nutrient additives", "base_price": 40, "category": "agricultural", "volume": 1.5, "volatility": 0.3},
    "growth_hormones": {"name": "Growth Hormones", "description": "Plant accelerators", "base_price": 120, "category": "agricultural", "volume": 0.3, "volatility": 0.5},
    "pest_control": {"name": "Pest Control Agents", "description": "Crop protection", "base_price": 65, "category": "agricultural", "volume": 0.5, "volatility": 0.4},
    "hydroponics_solution": {"name": "Hydroponics Solution", "description": "Soilless nutrients", "base_price": 55, "category": "agricultural", "volume": 1.0, "volatility": 0.3},

    # Data & Information (6 items)
    "star_charts": {"name": "Star Charts", "description": "Navigation data", "base_price": 150, "category": "data", "volume": 0.1, "volatility": 0.4},
    "research_papers": {"name": "Research Papers", "description": "Scientific knowledge", "base_price": 200, "category": "data", "volume": 0.1, "volatility": 0.5},
    "encrypted_data": {"name": "Encrypted Data", "description": "Secure information", "base_price": 500, "category": "data", "volume": 0.1, "volatility": 0.7},
    "market_intelligence": {"name": "Market Intelligence", "description": "Trading data", "base_price": 300, "category": "data", "volume": 0.1, "volatility": 0.8},
    "military_schematics": {"name": "Military Schematics", "description": "Restricted designs", "base_price": 1000, "category": "data", "volume": 0.1, "volatility": 0.9},
    "cultural_databases": {"name": "Cultural Databases", "description": "Historical records", "base_price": 180, "category": "data", "volume": 0.1, "volatility": 0.4},
}

# Commodity category characteristics for market behavior
COMMODITY_CATEGORIES = {
    "food": {"demand_volatility": 0.3, "supply_stability": 0.7, "universal_need": True},
    "medical": {"demand_volatility": 0.4, "supply_stability": 0.6, "universal_need": True},
    "science": {"demand_volatility": 0.3, "supply_stability": 0.8, "universal_need": False},
    "life_support": {"demand_volatility": 0.4, "supply_stability": 0.7, "universal_need": True},
    "luxury": {"demand_volatility": 0.7, "supply_stability": 0.5, "universal_need": False},
    "research": {"demand_volatility": 0.6, "supply_stability": 0.4, "universal_need": False},
    "technology": {"demand_volatility": 0.4, "supply_stability": 0.6, "universal_need": False},
    "energy": {"demand_volatility": 0.5, "supply_stability": 0.6, "universal_need": True},
    "materials": {"demand_volatility": 0.3, "supply_stability": 0.7, "universal_need": False},
    "entertainment": {"demand_volatility": 0.5, "supply_stability": 0.6, "universal_need": False},
    "agricultural": {"demand_volatility": 0.4, "supply_stability": 0.6, "universal_need": False},
    "data": {"demand_volatility": 0.6, "supply_stability": 0.5, "universal_need": False},
}

# ============= MODULES (Expanded) =============
MODULES = {
    # Tier 1 Weapons
    "pulse_cannon_t1": {
        "name": "Pulse Cannon T1",
        "type": "weapon",
        "tier": 1,
        "description": "Basic energy weapon",
        "cost": 9000,
        "manufacturing_cost": 6500,
        "damage": 80,
        "accuracy": 0.80,
        "fire_rate": 3.0,
        "power_usage": 40,
        "required_level": 1,
        "level_requirement": 1
    },
    "plasma_lance_t1": {
        "name": "Plasma Lance T1",
        "type": "weapon",
        "tier": 1,
        "description": "Focused beam weapon",
        "cost": 18000,
        "manufacturing_cost": 13000,
        "damage": 200,
        "accuracy": 0.92,
        "fire_rate": 1.5,
        "power_usage": 120,
        "required_level": 3,
        "level_requirement": 3
    },
    # Tier 2 Weapons
    "pulse_cannon_t2": {
        "name": "Pulse Cannon T2",
        "type": "weapon",
        "tier": 2,
        "description": "Improved energy weapon",
        "cost": 160000,
        "manufacturing_cost": 115000,
        "damage": 160,
        "accuracy": 0.85,
        "fire_rate": 3.5,
        "power_usage": 60,
        "required_level": 5,
        "level_requirement": 5
    },
    "void_torpedo_t1": {
        "name": "Void Torpedo T1",
        "type": "weapon",
        "tier": 1,
        "description": "Explosive projectile",
        "cost": 24000,
        "manufacturing_cost": 17000,
        "damage": 400,
        "accuracy": 0.65,
        "fire_rate": 0.5,
        "power_usage": 80,
        "required_level": 4,
        "level_requirement": 4
    },
    # Defense Modules
    "aegis_shield_t1": {
        "name": "Aegis Shield T1",
        "type": "defense",
        "tier": 1,
        "description": "Basic shield system",
        "cost": 14000,
        "manufacturing_cost": 10000,
        "shield_boost": 300,
        "recharge_rate": 30,
        "power_usage": 50,
        "required_level": 1,
        "level_requirement": 1
    },
    "aegis_shield_t2": {
        "name": "Aegis Shield T2",
        "type": "defense",
        "tier": 2,
        "description": "Advanced shield system",
        "cost": 240000,
        "manufacturing_cost": 170000,
        "shield_boost": 700,
        "recharge_rate": 70,
        "power_usage": 90,
        "required_level": 5,
        "level_requirement": 5
    },
    "fortress_plating_t1": {
        "name": "Fortress Plating T1",
        "type": "defense",
        "tier": 1,
        "description": "Reinforced armor",
        "cost": 10000,
        "manufacturing_cost": 7000,
        "armor_boost": 120,
        "damage_reduction": 0.12,
        "power_usage": 20,
        "required_level": 2,
        "level_requirement": 2
    },
    "phantom_cloak_t1": {
        "name": "Phantom Cloak T1",
        "type": "defense",
        "tier": 1,
        "description": "Stealth system",
        "cost": 24000,
        "manufacturing_cost": 17000,
        "evasion_boost": 0.25,
        "power_usage": 150,
        "required_level": 6,
        "level_requirement": 6
    },
    # Utility Modules
    "quantum_scanner_t1": {
        "name": "Quantum Scanner T1",
        "type": "utility",
        "tier": 1,
        "description": "Basic sensor array",
        "cost": 10000,
        "manufacturing_cost": 7000,
        "scan_range": 800,
        "detection_boost": 0.20,
        "power_usage": 40,
        "required_level": 1,
        "level_requirement": 1
    },
    "harvester_drill_t1": {
        "name": "Harvester Drill T1",
        "type": "utility",
        "tier": 1,
        "description": "Basic mining equipment - Can mine basic ores (common/uncommon)",
        "cost": 18000,
        "manufacturing_cost": 13000,
        "mining_yield": 1.3,
        "mining_speed": 1.1,
        "mining_tier": 1,  # Can mine tier 1 ores only
        "ship_tier_max": 2,  # T1 and T2 ships only
        "power_usage": 80,
        "required_level": 2,
        "level_requirement": 2
    },
    "harvester_drill_t2": {
        "name": "Harvester Drill T2",
        "type": "utility",
        "tier": 2,
        "description": "Advanced mining equipment - Can mine basic and mid-tier ores (rare)",
        "cost": 180000,
        "manufacturing_cost": 130000,
        "mining_yield": 1.8,
        "mining_speed": 1.4,
        "mining_tier": 2,  # Can mine tier 1-2 ores
        "ship_tier_max": 2,  # T1 and T2 ships only
        "power_usage": 120,
        "required_level": 7,
        "level_requirement": 7
    },
    "harvester_drill_t3": {
        "name": "Harvester Drill T3",
        "type": "utility",
        "tier": 3,
        "description": "Elite mining equipment - Can mine all ores including very rare and legendary",
        "cost": 900000,
        "manufacturing_cost": 650000,
        "mining_yield": 2.5,
        "mining_speed": 1.8,
        "mining_tier": 3,  # Can mine all tiers (1-3)
        "ship_tier_min": 2,  # T2 ships and above
        "power_usage": 180,
        "required_level": 12,
        "level_requirement": 12
    },
    "warp_drive_t1": {
        "name": "Warp Drive T1",
        "type": "utility",
        "tier": 1,
        "description": "Faster travel",
        "cost": 18000,
        "manufacturing_cost": 13000,
        "speed_boost": 0.40,
        "power_usage": 100,
        "required_level": 3,
        "level_requirement": 3
    },
    "refinery_module_t1": {
        "name": "Compact Refinery T1",
        "type": "utility",
        "tier": 1,
        "description": "Process raw resources into refined materials",
        "cost": 30000,
        "manufacturing_cost": 21000,
        "refining_speed": 1.0,
        "refining_efficiency": 0.9,  # 90% of normal refine ratio
        "power_usage": 200,
        "required_level": 8,
        "level_requirement": 8
    },
    "refinery_module_t2": {
        "name": "Industrial Refinery T2",
        "type": "utility",
        "tier": 2,
        "description": "Advanced refining system",
        "cost": 500000,
        "manufacturing_cost": 360000,
        "refining_speed": 1.5,
        "refining_efficiency": 1.0,  # 100% of normal refine ratio
        "power_usage": 300,
        "required_level": 12,
        "level_requirement": 12
    },
    "manufacturing_bay_t1": {
        "name": "Manufacturing Bay T1",
        "type": "utility",
        "tier": 1,
        "description": "Build modules and components",
        "cost": 30000,
        "manufacturing_cost": 21000,
        "manufacturing_speed": 1.0,
        "power_usage": 250,
        "required_level": 10,
        "level_requirement": 10
    },
    # Engine Modules
    "basic_thruster_t1": {
        "name": "Basic Thruster T1",
        "type": "engine",
        "tier": 1,
        "description": "Standard propulsion system for small vessels",
        "cost": 5000,
        "manufacturing_cost": 3500,
        "speed_boost": 0.15,
        "agility_boost": 0.10,
        "power_generation": 200,
        "required_level": 1,
        "level_requirement": 1
    },
    "nova_engine_t1": {
        "name": "Nova Engine T1",
        "type": "engine",
        "tier": 1,
        "description": "High-performance propulsion for combat vessels",
        "cost": 14000,
        "manufacturing_cost": 10000,
        "speed_boost": 0.35,
        "agility_boost": 0.25,
        "power_generation": 400,
        "required_level": 4,
        "level_requirement": 4
    },
    "cargo_drive_t1": {
        "name": "Cargo Drive T1",
        "type": "engine",
        "tier": 1,
        "description": "Efficient engine optimized for haulers",
        "cost": 8000,
        "manufacturing_cost": 6000,
        "speed_boost": 0.20,
        "agility_boost": 0.05,
        "power_generation": 500,
        "required_level": 3,
        "level_requirement": 3
    },
    "nova_engine_t2": {
        "name": "Nova Engine T2",
        "type": "engine",
        "tier": 2,
        "description": "Advanced military-grade propulsion",
        "cost": 240000,
        "manufacturing_cost": 170000,
        "speed_boost": 0.60,
        "agility_boost": 0.40,
        "power_generation": 700,
        "required_level": 10,
        "level_requirement": 10
    },
    "cargo_drive_t2": {
        "name": "Cargo Drive T2",
        "type": "engine",
        "tier": 2,
        "description": "Heavy-duty engine for large cargo vessels",
        "cost": 180000,
        "manufacturing_cost": 125000,
        "speed_boost": 0.40,
        "agility_boost": 0.15,
        "power_generation": 900,
        "required_level": 9,
        "level_requirement": 9
    },
    "nova_engine_t3": {
        "name": "Nova Engine T3",
        "type": "engine",
        "tier": 3,
        "description": "Cutting-edge propulsion technology",
        "cost": 450000,
        "manufacturing_cost": 320000,
        "speed_boost": 0.90,
        "agility_boost": 0.60,
        "power_generation": 1200,
        "required_level": 16,
        "level_requirement": 16
    },
    "cargo_drive_t3": {
        "name": "Cargo Drive T3",
        "type": "engine",
        "tier": 3,
        "description": "Industrial-grade engine for massive haulers",
        "cost": 350000,
        "manufacturing_cost": 240000,
        "speed_boost": 0.65,
        "agility_boost": 0.25,
        "power_generation": 1500,
        "required_level": 15,
        "level_requirement": 15
    }
}

# Map old module names to new tier 1 versions for backward compatibility
MODULE_COMPATIBILITY = {
    "pulse_cannon": "pulse_cannon_t1",
    "plasma_lance": "plasma_lance_t1",
    "void_torpedo": "void_torpedo_t1",
    "aegis_shield": "aegis_shield_t1",
    "fortress_plating": "fortress_plating_t1",
    "phantom_cloak": "phantom_cloak_t1",
    "quantum_scanner": "quantum_scanner_t1",
    "harvester_drill": "harvester_drill_t1",
    "warp_drive": "warp_drive_t1",
    "nova_engine": "nova_engine_t1",
    "basic_thruster": "basic_thruster_t1",
    "cargo_drive": "cargo_drive_t1"
}

# ============= MODULE COMPONENTS =============
# These are intermediate components used to manufacture modules
# Made from refined materials, used to create modules
MODULE_COMPONENTS = {
    # Weapon Components
    "energy_cell_t1": {
        "name": "Energy Cell T1",
        "type": "power_component",
        "tier": 1,
        "description": "Basic power cell for energy weapons",
        "volume": 5,
    },
    "energy_cell_t2": {
        "name": "Energy Cell T2",
        "type": "power_component",
        "tier": 2,
        "description": "Advanced power cell for energy weapons",
        "volume": 5,
    },
    "targeting_chip_t1": {
        "name": "Targeting Chip T1",
        "type": "electronics",
        "tier": 1,
        "description": "Basic targeting computer chip",
        "volume": 2,
    },
    "targeting_chip_t2": {
        "name": "Targeting Chip T2",
        "type": "electronics",
        "tier": 2,
        "description": "Advanced targeting computer chip",
        "volume": 2,
    },
    "weapon_barrel": {
        "name": "Weapon Barrel",
        "type": "mechanical",
        "tier": 1,
        "description": "Reinforced weapon barrel assembly",
        "volume": 8,
    },
    "focusing_lens": {
        "name": "Focusing Lens",
        "type": "optics",
        "tier": 1,
        "description": "High-grade optical focusing lens",
        "volume": 3,
    },
    "explosive_warhead": {
        "name": "Explosive Warhead",
        "type": "ordnance",
        "tier": 1,
        "description": "Shaped explosive charge",
        "volume": 6,
    },

    # Defense Components
    "shield_emitter_t1": {
        "name": "Shield Emitter T1",
        "type": "defense_component",
        "tier": 1,
        "description": "Basic shield projection unit",
        "volume": 10,
    },
    "shield_emitter_t2": {
        "name": "Shield Emitter T2",
        "type": "defense_component",
        "tier": 2,
        "description": "Advanced shield projection unit",
        "volume": 10,
    },
    "armor_plate_t1": {
        "name": "Armor Plate T1",
        "type": "structural",
        "tier": 1,
        "description": "Reinforced armor plating",
        "volume": 12,
    },
    "armor_plate_t2": {
        "name": "Armor Plate T2",
        "type": "structural",
        "tier": 2,
        "description": "Heavy-duty armor plating",
        "volume": 12,
    },
    "stealth_core": {
        "name": "Stealth Core",
        "type": "electronics",
        "tier": 1,
        "description": "Cloaking field generator core",
        "volume": 8,
    },

    # Utility Components
    "sensor_array_t1": {
        "name": "Sensor Array T1",
        "type": "electronics",
        "tier": 1,
        "description": "Basic sensor package",
        "volume": 6,
    },
    "sensor_array_t2": {
        "name": "Sensor Array T2",
        "type": "electronics",
        "tier": 2,
        "description": "Advanced sensor package",
        "volume": 6,
    },
    "mining_laser": {
        "name": "Mining Laser",
        "type": "industrial",
        "tier": 1,
        "description": "High-powered mining laser assembly",
        "volume": 15,
    },
    "warp_coil": {
        "name": "Warp Coil",
        "type": "propulsion",
        "tier": 1,
        "description": "Warp field generation coil",
        "volume": 20,
    },
    "processor_unit_t1": {
        "name": "Processor Unit T1",
        "type": "electronics",
        "tier": 1,
        "description": "Basic processing unit",
        "volume": 4,
    },
    "processor_unit_t2": {
        "name": "Processor Unit T2",
        "type": "electronics",
        "tier": 2,
        "description": "Advanced processing unit",
        "volume": 4,
    },
    "refinery_core": {
        "name": "Refinery Core",
        "type": "industrial",
        "tier": 1,
        "description": "Resource refining core module",
        "volume": 25,
    },
    "manufacturing_core": {
        "name": "Manufacturing Core",
        "type": "industrial",
        "tier": 1,
        "description": "Automated manufacturing core",
        "volume": 30,
    },
}

# ============= MODULE COMPONENT RECIPES =============
# Recipes to manufacture module components from refined materials
MODULE_COMPONENT_RECIPES = {
    # Weapon Components
    "energy_cell_t1": {
        "materials": {
            "voltium": 2,
            "plasmic_fuel": 1
        },
        "time": 30,
        "skill_requirement": 0
    },
    "energy_cell_t2": {
        "materials": {
            "voltium": 5,
            "plasmic_fuel": 3,
            "chronite": 1
        },
        "time": 60,
        "skill_requirement": 2
    },
    "targeting_chip_t1": {
        "materials": {
            "neural_fiber": 1,
            "voltium": 1
        },
        "time": 40,
        "skill_requirement": 0
    },
    "targeting_chip_t2": {
        "materials": {
            "neural_fiber": 3,
            "chronite": 2
        },
        "time": 80,
        "skill_requirement": 2
    },
    "weapon_barrel": {
        "materials": {
            "titanite": 3,
            "nexium": 1
        },
        "time": 45,
        "skill_requirement": 0
    },
    "focusing_lens": {
        "materials": {
            "synthcrystal": 2,
            "voltium": 1
        },
        "time": 50,
        "skill_requirement": 1
    },
    "explosive_warhead": {
        "materials": {
            "plasmic_fuel": 3,
            "titanite": 2,
            "darkwater": 1
        },
        "time": 55,
        "skill_requirement": 1
    },

    # Defense Components
    "shield_emitter_t1": {
        "materials": {
            "voltium": 3,
            "synthcrystal": 2,
            "nexium": 1
        },
        "time": 60,
        "skill_requirement": 0
    },
    "shield_emitter_t2": {
        "materials": {
            "voltium": 7,
            "synthcrystal": 5,
            "chronite": 3,
            "quantum_dust": 2
        },
        "time": 120,
        "skill_requirement": 2
    },
    "armor_plate_t1": {
        "materials": {
            "titanite": 5,
            "nexium": 2
        },
        "time": 50,
        "skill_requirement": 0
    },
    "armor_plate_t2": {
        "materials": {
            "titanite": 10,
            "nexium": 5,
            "chronite": 3
        },
        "time": 100,
        "skill_requirement": 2
    },
    "stealth_core": {
        "materials": {
            "quantum_dust": 5,
            "neural_fiber": 3,
            "darkwater": 2
        },
        "time": 90,
        "skill_requirement": 3
    },

    # Utility Components
    "sensor_array_t1": {
        "materials": {
            "neural_fiber": 2,
            "synthcrystal": 2,
            "voltium": 1
        },
        "time": 50,
        "skill_requirement": 0
    },
    "sensor_array_t2": {
        "materials": {
            "neural_fiber": 5,
            "quantum_dust": 3,
            "chronite": 2
        },
        "time": 100,
        "skill_requirement": 2
    },
    "mining_laser": {
        "materials": {
            "voltium": 4,
            "titanite": 3,
            "synthcrystal": 2
        },
        "time": 70,
        "skill_requirement": 1
    },
    "warp_coil": {
        "materials": {
            "chronite": 5,
            "voltium": 4,
            "quantum_dust": 3
        },
        "time": 90,
        "skill_requirement": 2
    },
    "processor_unit_t1": {
        "materials": {
            "neural_fiber": 2,
            "voltium": 1
        },
        "time": 40,
        "skill_requirement": 0
    },
    "processor_unit_t2": {
        "materials": {
            "neural_fiber": 5,
            "quantum_dust": 3,
            "chronite": 1
        },
        "time": 80,
        "skill_requirement": 2
    },
    "refinery_core": {
        "materials": {
            "titanite": 10,
            "voltium": 8,
            "neural_fiber": 5,
            "plasmic_fuel": 5
        },
        "time": 150,
        "skill_requirement": 4
    },
    "manufacturing_core": {
        "materials": {
            "titanite": 15,
            "neural_fiber": 8,
            "chronite": 5,
            "quantum_dust": 3
        },
        "time": 180,
        "skill_requirement": 5
    },
}

# ============= MANUFACTURING RECIPES =============
# Now modules are made from components (not raw materials)
# Components are made from refined materials
MANUFACTURING_RECIPES = {
    # Weapons
    "pulse_cannon_t1": {
        "components": {
            "energy_cell_t1": 2,
            "targeting_chip_t1": 1,
            "weapon_barrel": 1
        },
        "time": 120,  # 2 minutes
        "skill_requirement": 0
    },
    "plasma_lance_t1": {
        "components": {
            "energy_cell_t1": 3,
            "targeting_chip_t1": 2,
            "focusing_lens": 2
        },
        "time": 180,  # 3 minutes
        "skill_requirement": 1
    },
    "pulse_cannon_t2": {
        "components": {
            "energy_cell_t2": 2,
            "targeting_chip_t2": 1,
            "weapon_barrel": 2
        },
        "time": 240,  # 4 minutes
        "skill_requirement": 2
    },
    "void_torpedo_t1": {
        "components": {
            "explosive_warhead": 3,
            "targeting_chip_t1": 1,
            "processor_unit_t1": 1
        },
        "time": 300,  # 5 minutes
        "skill_requirement": 2
    },
    # Defense Modules
    "aegis_shield_t1": {
        "components": {
            "shield_emitter_t1": 2,
            "energy_cell_t1": 1,
            "processor_unit_t1": 1
        },
        "time": 150,  # 2.5 minutes
        "skill_requirement": 0
    },
    "aegis_shield_t2": {
        "components": {
            "shield_emitter_t2": 2,
            "energy_cell_t2": 2,
            "processor_unit_t2": 1
        },
        "time": 300,  # 5 minutes
        "skill_requirement": 2
    },
    "fortress_plating_t1": {
        "components": {
            "armor_plate_t1": 3,
            "processor_unit_t1": 1
        },
        "time": 180,  # 3 minutes
        "skill_requirement": 1
    },
    "phantom_cloak_t1": {
        "components": {
            "stealth_core": 1,
            "energy_cell_t1": 2,
            "processor_unit_t1": 2
        },
        "time": 420,  # 7 minutes
        "skill_requirement": 3
    },
    # Utility Modules
    "quantum_scanner_t1": {
        "components": {
            "sensor_array_t1": 2,
            "processor_unit_t1": 1
        },
        "time": 180,  # 3 minutes
        "skill_requirement": 0
    },
    "harvester_drill_t1": {
        "components": {
            "mining_laser": 1,
            "energy_cell_t1": 2,
            "processor_unit_t1": 1
        },
        "time": 210,  # 3.5 minutes
        "skill_requirement": 1
    },
    "harvester_drill_t2": {
        "components": {
            "mining_laser": 2,
            "energy_cell_t2": 3,
            "processor_unit_t2": 2
        },
        "time": 480,  # 8 minutes
        "skill_requirement": 4
    },
    "harvester_drill_t3": {
        "components": {
            "mining_laser": 4,
            "energy_cell_t3": 4,
            "processor_unit_t3": 3,
            "shield_emitter": 2
        },
        "time": 720,  # 12 minutes
        "skill_requirement": 6
    },
    "warp_drive_t1": {
        "components": {
            "warp_coil": 2,
            "energy_cell_t1": 3,
            "processor_unit_t1": 2
        },
        "time": 360,  # 6 minutes
        "skill_requirement": 2
    },
    "refinery_module_t1": {
        "components": {
            "refinery_core": 1,
            "energy_cell_t1": 3,
            "processor_unit_t1": 3
        },
        "time": 600,  # 10 minutes
        "skill_requirement": 5
    },
    "refinery_module_t2": {
        "components": {
            "refinery_core": 2,
            "energy_cell_t2": 5,
            "processor_unit_t2": 4
        },
        "time": 900,  # 15 minutes
        "skill_requirement": 7
    },
    "manufacturing_bay_t1": {
        "components": {
            "manufacturing_core": 1,
            "energy_cell_t1": 4,
            "processor_unit_t1": 4
        },
        "time": 720,  # 12 minutes
        "skill_requirement": 6
    },
    # Engine Modules
    "basic_thruster_t1": {
        "materials": {
            "titanite": 10,
            "plasmic_fuel": 5,
            "voltium": 3
        },
        "time": 240,  # 4 minutes
        "skill_requirement": 1
    },
    "nova_engine_t1": {
        "materials": {
            "titanite": 20,
            "plasmic_fuel": 12,
            "voltium": 8,
            "nexium": 5
        },
        "time": 420,  # 7 minutes
        "skill_requirement": 2
    },
    "cargo_drive_t1": {
        "materials": {
            "titanite": 15,
            "plasmic_fuel": 10,
            "voltium": 5,
            "nexium": 3
        },
        "time": 360,  # 6 minutes
        "skill_requirement": 2
    },
    "nova_engine_t2": {
        "materials": {
            "titanite": 45,
            "plasmic_fuel": 30,
            "voltium": 20,
            "nexium": 15,
            "chronite": 8
        },
        "time": 840,  # 14 minutes
        "skill_requirement": 6
    },
    "cargo_drive_t2": {
        "materials": {
            "titanite": 35,
            "plasmic_fuel": 25,
            "voltium": 15,
            "nexium": 12,
            "chronite": 6
        },
        "time": 720,  # 12 minutes
        "skill_requirement": 5
    },
    "nova_engine_t3": {
        "materials": {
            "titanite": 80,
            "plasmic_fuel": 60,
            "voltium": 40,
            "nexium": 30,
            "chronite": 20,
            "voidstone": 10
        },
        "time": 1440,  # 24 minutes
        "skill_requirement": 9
    },
    "cargo_drive_t3": {
        "materials": {
            "titanite": 65,
            "plasmic_fuel": 50,
            "voltium": 30,
            "nexium": 25,
            "chronite": 15,
            "voidstone": 8
        },
        "time": 1200,  # 20 minutes
        "skill_requirement": 8
    }
}

# ============= EXPANDED SKILLS =============
SKILLS = {
    # Combat Skills
    "weapons_mastery": {
        "name": "Weapons Mastery",
        "category": "combat",
        "description": "Increases weapon damage and accuracy",
        "max_level": 10,
        "bonus_per_level": {"damage": 0.05, "accuracy": 0.02}
    },
    "tactical_warfare": {
        "name": "Tactical Warfare",
        "category": "combat",
        "description": "Improves combat maneuvering and strategy",
        "max_level": 10,
        "bonus_per_level": {"evasion": 0.03, "crit_chance": 0.02}
    },
    "shield_operations": {
        "name": "Shield Operations",
        "category": "combat",
        "description": "Enhances shield capacity and recharge",
        "max_level": 10,
        "bonus_per_level": {"shield_capacity": 0.05, "shield_recharge": 0.04}
    },
    # Industrial Skills
    "mining_operations": {
        "name": "Mining Operations",
        "category": "industrial",
        "description": "Increases mining yield and efficiency",
        "max_level": 10,
        "bonus_per_level": {"mining_yield": 0.06, "mining_speed": 0.03}
    },
    "refining": {
        "name": "Refining",
        "category": "industrial",
        "description": "Improves resource refining efficiency",
        "max_level": 10,
        "bonus_per_level": {"refining_efficiency": 0.05, "refining_speed": 0.04}
    },
    "module_manufacturing": {
        "name": "Module Manufacturing",
        "category": "industrial",
        "description": "Build ship modules and components faster",
        "max_level": 10,
        "bonus_per_level": {"manufacturing_speed": 0.06, "cost_reduction": 0.03}
    },
    "ship_construction": {
        "name": "Ship Construction",
        "category": "industrial",
        "description": "Build and upgrade vessels",
        "max_level": 10,
        "bonus_per_level": {"construction_speed": 0.05, "cost_reduction": 0.04}
    },
    "salvaging": {
        "name": "Salvaging",
        "category": "industrial",
        "description": "Improves salvage from wrecks and debris",
        "max_level": 10,
        "bonus_per_level": {"salvage_yield": 0.08}
    },
    # Trading Skills
    "trade_proficiency": {
        "name": "Trade Proficiency",
        "category": "trading",
        "description": "Better market prices and reduced taxes",
        "max_level": 10,
        "bonus_per_level": {"buy_discount": 0.02, "sell_bonus": 0.02, "tax_reduction": 0.005}
    },
    "market_analysis": {
        "name": "Market Analysis",
        "category": "trading",
        "description": "Reveals market trends and predictions",
        "max_level": 10,
        "bonus_per_level": {"market_insight": 0.10}
    },
    "logistics_management": {
        "name": "Logistics Management",
        "category": "trading",
        "description": "Manage cargo across locations. Level 5+ allows remote station access",
        "max_level": 10,
        "bonus_per_level": {"cargo_efficiency": 0.03, "transfer_speed": 0.05}
    },
    # Navigation Skills
    "navigation": {
        "name": "Navigation",
        "category": "navigation",
        "description": "Faster travel between sectors",
        "max_level": 10,
        "bonus_per_level": {"travel_speed": 0.05, "fuel_efficiency": 0.03}
    },
    "scanning": {
        "name": "Scanning",
        "category": "navigation",
        "description": "Detect resources, threats, and anomalies",
        "max_level": 10,
        "bonus_per_level": {"scan_range": 0.08, "scan_accuracy": 0.05}
    },
    # Engineering Skills
    "vessel_engineering": {
        "name": "Vessel Engineering",
        "category": "engineering",
        "description": "Unlocks advanced modules and upgrades",
        "max_level": 10,
        "bonus_per_level": {"module_efficiency": 0.04, "repair_speed": 0.05}
    },
    "power_management": {
        "name": "Power Management",
        "category": "engineering",
        "description": "Better energy distribution and capacity",
        "max_level": 10,
        "bonus_per_level": {"power_capacity": 0.05, "power_efficiency": 0.03}
    },
    # Leadership Skills
    "command": {
        "name": "Command",
        "category": "leadership",
        "description": "Lead fleets and improve crew effectiveness",
        "max_level": 10,
        "bonus_per_level": {"fleet_bonus": 0.05, "crew_efficiency": 0.04}
    },
    "diplomacy": {
        "name": "Diplomacy",
        "category": "leadership",
        "description": "Improve faction relations and negotiations",
        "max_level": 10,
        "bonus_per_level": {"reputation_gain": 0.06, "contract_rewards": 0.04}
    },
    # Training Skills
    "multi_tasking": {
        "name": "Multi-Tasking",
        "category": "training",
        "description": "Train multiple skills simultaneously. Each level unlocks an additional training slot (max 5 slots at level 5)",
        "max_level": 5,
        "bonus_per_level": {"training_slots": 1.0}
    }
}

# To be continued in next part...

# ============= LOCATIONS (10+ Stations, Planets, Asteroids) =============
LOCATIONS = {
    # === STATIONS ===
    "nexus_prime": {
        "name": "Nexus Prime Station",
        "type": "station",
        "description": "Central hub station and trade capital of the Nebular Expanse",
        "faction": "meridian_collective",
        "services": ["market", "shipyard", "contracts", "refinery", "manufacturing"],
        "resources": [],  # Stations don't have raw resources
        "danger_level": 0.05,
        "connections": ["meridian_gates", "forge_station", "outer_belts", "titan_alpha"]
    },
    "forge_station": {
        "name": "Forge Station",
        "type": "station",
        "description": "Industrial manufacturing hub specializing in ship components",
        "faction": "technocrat_union",
        "services": ["market", "manufacturing", "refinery", "shipyard"],
        "resources": [],
        "danger_level": 0.1,
        "connections": ["nexus_prime", "synthesis_planet", "ironhold_sectors"]
    },
    "meridian_gates": {
        "name": "Meridian Gates Outpost",
        "type": "station",
        "description": "Fortified border checkpoint with military presence",
        "faction": "meridian_collective",
        "services": ["market", "contracts", "shipyard"],
        "resources": [],
        "danger_level": 0.2,
        "connections": ["nexus_prime", "outer_belts", "crimson_expanse"]
    },
    "corsair_haven": {
        "name": "Corsair Haven",
        "type": "station",
        "description": "Hidden pirate station operating in the shadows",
        "faction": "void_corsairs",
        "services": ["black_market", "contracts", "shipyard"],
        "resources": [],
        "danger_level": 0.75,
        "connections": ["shadow_nebula", "dead_zone_asteroids", "blackmarket_dock"]
    },
    "blackmarket_dock": {
        "name": "Blackmarket Docking Bay",
        "type": "station",
        "description": "Illicit trading post for questionable goods",
        "faction": "void_corsairs",
        "services": ["black_market"],
        "resources": [],
        "danger_level": 0.7,
        "connections": ["corsair_haven", "shadow_nebula"]
    },
    
    # === PLANETS ===
    "titan_alpha": {
        "name": "Titan Alpha Colony",
        "type": "planet",
        "description": "Temperate colony world with agricultural exports",
        "faction": "meridian_collective",
        "services": ["market", "contracts", "refinery"],
        "resources": [],  # Planets don't have raw resources to mine
        "danger_level": 0.1,
        "connections": ["nexus_prime", "outer_belts", "harvest_fields"]
    },
    "synthesis_planet": {
        "name": "Synthesis Prime",
        "type": "planet",
        "description": "High-tech research world with advanced laboratories",
        "faction": "technocrat_union",
        "services": ["market", "research", "refinery", "manufacturing", "shipyard"],
        "resources": [],
        "danger_level": 0.15,
        "connections": ["forge_station", "neural_network", "axiom_labs"]
    },
    "ironhold_world": {
        "name": "Ironhold Industrial World",
        "type": "planet",
        "description": "Heavy industrial planet with massive foundries",
        "faction": "cipher_dominion",
        "services": ["market", "manufacturing", "refinery", "shipyard"],
        "resources": [],
        "danger_level": 0.5,
        "connections": ["ironhold_sectors", "forge_station", "crimson_expanse"]
    },
    "neural_network": {
        "name": "Neural Network Nexus",
        "type": "planet",
        "description": "Planet-wide AI computing megastructure",
        "faction": "technocrat_union",
        "services": ["market", "research", "contracts"],
        "resources": [],
        "danger_level": 0.2,
        "connections": ["synthesis_planet", "axiom_labs"]
    },
    
    # === ASTEROID BELTS (Mining Locations) ===
    "outer_belts": {
        "name": "Outer Belt Clusters",
        "type": "asteroid",
        "description": "Rich asteroid field with common ores",
        "faction": None,
        "services": [],
        "resources": ["raw_voltium", "raw_titanite", "raw_neuralfiber"],
        "danger_level": 0.3,
        "connections": ["nexus_prime", "meridian_gates", "titan_alpha", "shadow_nebula"]
    },
    "harvest_fields": {
        "name": "Harvest Fields Belt",
        "type": "asteroid",
        "description": "Dense asteroid belt with diverse materials",
        "faction": None,
        "services": [],
        "resources": ["raw_voltium", "raw_nexium", "raw_titanite", "raw_neuralfiber"],
        "danger_level": 0.4,
        "connections": ["titan_alpha", "outer_belts"]
    },
    "chronos_expanse": {
        "name": "Chronos Expanse",
        "type": "asteroid",
        "description": "Anomalous belt with rare time-dilated crystals",
        "faction": None,
        "services": [],
        "resources": ["raw_chronite", "raw_quantum_dust", "raw_nexium"],
        "anomalies": True,  # Has scannable anomalies for research contracts
        "danger_level": 0.6,
        "connections": ["axiom_labs", "neural_network", "synthesis_planet"]
    },
    "dead_zone_asteroids": {
        "name": "Dead Zone Asteroids",
        "type": "asteroid",
        "description": "Dangerous belt with high-value materials",
        "faction": None,
        "services": [],
        "resources": ["raw_synthcrystal", "raw_darkwater", "raw_quantum_dust", "raw_chronite"],
        "anomalies": True,  # Has scannable anomalies for research contracts
        "danger_level": 0.85,
        "connections": ["corsair_haven", "shadow_nebula"]
    },
    "pristine_fields": {
        "name": "Pristine Mineral Fields",
        "type": "asteroid",
        "description": "Untouched asteroid belt rich in resources",
        "faction": None,
        "services": [],
        "resources": ["raw_voltium", "raw_titanite", "raw_nexium", "raw_chronite", "raw_neuralfiber"],
        "danger_level": 0.5,
        "connections": ["forge_station", "ironhold_sectors"]
    },
    
    # === COMBAT/CONFLICT ZONES ===
    "crimson_expanse": {
        "name": "Crimson Expanse War Zone",
        "type": "space",
        "description": "Active combat zone between factions",
        "faction": "cipher_dominion",
        "services": [],
        "resources": [],
        "danger_level": 0.9,
        "connections": ["meridian_gates", "ironhold_world", "ironhold_sectors"]
    },
    "shadow_nebula": {
        "name": "Shadow Nebula",
        "type": "space",
        "description": "Dense nebula concealing pirate operations",
        "faction": "void_corsairs",
        "services": [],
        "resources": [],
        "anomalies": True,  # Has scannable anomalies for research contracts
        "danger_level": 0.8,
        "connections": ["outer_belts", "dead_zone_asteroids", "corsair_haven", "blackmarket_dock"]
    },

    # === RESEARCH/SPECIAL ===
    "axiom_labs": {
        "name": "Axiom Research Laboratories",
        "type": "station",
        "description": "Experimental weapons and technology testing facility",
        "faction": "technocrat_union",
        "services": ["research", "market", "shipyard"],
        "resources": [],
        "anomalies": True,  # Research station with experimental anomalies
        "danger_level": 0.35,
        "connections": ["neural_network", "synthesis_planet", "chronos_expanse"]
    },
    "ironhold_sectors": {
        "name": "Ironhold Manufacturing Sectors",
        "type": "space",
        "description": "Heavy industrial zone with factory complexes",
        "faction": "cipher_dominion",
        "services": ["market", "manufacturing"],
        "resources": [],
        "danger_level": 0.55,
        "connections": ["forge_station", "ironhold_world", "crimson_expanse", "pristine_fields"]
    },

    # ========== NEUTRAL ZONE (Safe Starting Area) ==========
    "starlight_waystation": {
        "name": "Starlight Waystation",
        "type": "station",
        "description": "Peaceful rest stop offering repairs and supplies to weary travelers",
        "faction": None,
        "services": ["market", "repair", "refinery"],
        "resources": [],
        "danger_level": 0.05,
        "connections": ["nexus_prime", "outer_belts", "tranquil_belt"]
    },
    "tranquil_belt": {
        "name": "Tranquil Belt",
        "type": "asteroid",
        "description": "Calm asteroid field perfect for novice miners",
        "faction": None,
        "services": [],
        "resources": ["raw_voltium", "raw_titanite"],
        "danger_level": 0.1,
        "connections": ["starlight_waystation", "nexus_prime", "harvest_fields"]
    },
    "freeport_exchange": {
        "name": "Freeport Exchange",
        "type": "station",
        "description": "Independent trading hub where all factions are welcome",
        "faction": None,
        "services": ["market", "contracts", "shipyard"],
        "resources": [],
        "danger_level": 0.08,
        "connections": ["nexus_prime", "titan_alpha", "aurora_reach"]
    },

    # ========== MERIDIAN COLLECTIVE TERRITORY (Trade & Exploration) ==========
    "aurora_reach": {
        "name": "Aurora Reach Station",
        "type": "station",
        "description": "Gleaming trade station at the edge of Meridian space, its transparent domes showcase bustling markets beneath auroral skies",
        "faction": "meridian_collective",
        "services": ["market", "contracts", "shipyard", "refinery"],
        "resources": [],
        "danger_level": 0.15,
        "connections": ["freeport_exchange", "titan_alpha", "sapphire_fields", "merchant_corridor"]
    },
    "sapphire_fields": {
        "name": "Sapphire Fields",
        "type": "asteroid",
        "description": "Beautiful blue-tinted asteroids rich in voltium crystals",
        "faction": None,
        "services": [],
        "resources": ["raw_voltium", "raw_nexium", "raw_neuralfiber"],
        "danger_level": 0.2,
        "connections": ["aurora_reach", "harvest_fields", "titan_alpha"]
    },
    "merchant_corridor": {
        "name": "Merchant's Corridor",
        "type": "space",
        "description": "Well-patrolled shipping lane where Meridian merchants conduct their lucrative trade routes",
        "faction": "meridian_collective",
        "services": [],
        "resources": [],
        "danger_level": 0.12,
        "connections": ["aurora_reach", "prosperity_hub", "meridian_gates"]
    },
    "prosperity_hub": {
        "name": "Prosperity Hub",
        "type": "station",
        "description": "Luxurious commercial station featuring high-end shops and exclusive contracts for loyal Meridian traders",
        "faction": "meridian_collective",
        "services": ["market", "contracts", "manufacturing", "shipyard"],
        "resources": [],
        "danger_level": 0.18,
        "connections": ["merchant_corridor", "eden_prime", "crystal_gardens"]
    },
    "eden_prime": {
        "name": "Eden Prime",
        "type": "planet",
        "description": "Lush garden world serving as the cultural heart of the Meridian Collective, where art and commerce flourish",
        "faction": "meridian_collective",
        "services": ["market", "contracts", "refinery"],
        "resources": [],
        "danger_level": 0.1,
        "connections": ["prosperity_hub", "titan_alpha", "verdant_belt"]
    },
    "verdant_belt": {
        "name": "Verdant Belt",
        "type": "asteroid",
        "description": "Mineral-rich belt with organic ice formations",
        "faction": None,
        "services": [],
        "resources": ["raw_titanite", "raw_neuralfiber", "raw_voltium"],
        "danger_level": 0.25,
        "connections": ["eden_prime", "sapphire_fields"]
    },
    "crystal_gardens": {
        "name": "Crystal Gardens",
        "type": "asteroid",
        "description": "Stunning crystalline formations that shimmer in the starlight",
        "faction": None,
        "services": [],
        "resources": ["raw_chronite", "raw_nexium", "raw_quantum_dust"],
        "anomalies": True,
        "danger_level": 0.35,
        "connections": ["prosperity_hub", "explorer_outpost"]
    },
    "explorer_outpost": {
        "name": "Explorer's Outpost",
        "type": "station",
        "description": "Remote station dedicated to charting unknown regions, offering generous rewards for exploration contracts",
        "faction": "meridian_collective",
        "services": ["contracts", "market", "repair"],
        "resources": [],
        "danger_level": 0.3,
        "connections": ["crystal_gardens", "uncharted_expanse", "meridian_gates", "aurora_reach"]
    },
    "uncharted_expanse": {
        "name": "Uncharted Expanse",
        "type": "asteroid",
        "description": "Mysterious belt at the frontier of Meridian territory",
        "faction": None,
        "services": [],
        "resources": ["raw_nexium", "raw_chronite", "raw_quantum_dust"],
        "anomalies": True,
        "danger_level": 0.4,
        "connections": ["explorer_outpost", "meridian_gates"]
    },
    "horizon_vista": {
        "name": "Horizon Vista",
        "type": "planet",
        "description": "Scenic colony world with breathtaking views, popular among Meridian's wealthiest citizens seeking respite from trade politics",
        "faction": "meridian_collective",
        "services": ["market", "refinery"],
        "resources": [],
        "danger_level": 0.15,
        "connections": ["eden_prime", "prosperity_hub"]
    },

    # ========== TECHNOCRAT UNION TERRITORY (Technology & Research) ==========
    "datacore_prime": {
        "name": "Datacore Prime",
        "type": "station",
        "description": "Massive computing station housing the Union's central AI networks, where algorithmic perfection guides every decision",
        "faction": "technocrat_union",
        "services": ["research", "market", "contracts", "manufacturing"],
        "resources": [],
        "danger_level": 0.2,
        "connections": ["neural_network", "synthesis_planet", "binary_belt", "protocol_labs"]
    },
    "binary_belt": {
        "name": "Binary Belt",
        "type": "asteroid",
        "description": "Asteroid field optimized by Union algorithms for maximum efficiency",
        "faction": None,
        "services": [],
        "resources": ["raw_titanite", "raw_neuralfiber", "raw_voltium"],
        "danger_level": 0.25,
        "connections": ["datacore_prime", "forge_station"]
    },
    "protocol_labs": {
        "name": "Protocol Laboratories",
        "type": "station",
        "description": "Sterile research facility where Technocrat scientists push the boundaries of quantum mechanics and neural interfaces",
        "faction": "technocrat_union",
        "services": ["research", "market", "manufacturing", "shipyard"],
        "resources": [],
        "anomalies": True,
        "danger_level": 0.28,
        "connections": ["datacore_prime", "axiom_labs", "quantum_drift"]
    },
    "quantum_drift": {
        "name": "Quantum Drift",
        "type": "asteroid",
        "description": "Unstable belt exhibiting quantum fluctuations, perfect for exotic research",
        "faction": None,
        "services": [],
        "resources": ["raw_quantum_dust", "raw_chronite", "raw_synthcrystal"],
        "anomalies": True,
        "danger_level": 0.45,
        "connections": ["protocol_labs", "chronos_expanse", "singularity_reach"]
    },
    "singularity_reach": {
        "name": "Singularity Reach",
        "type": "station",
        "description": "Experimental station studying artificial singularities, protected by Union's most advanced defensive systems",
        "faction": "technocrat_union",
        "services": ["research", "contracts", "shipyard"],
        "resources": [],
        "anomalies": True,
        "danger_level": 0.5,
        "connections": ["quantum_drift", "axiom_labs", "void_forge"]
    },
    "void_forge": {
        "name": "Void Forge",
        "type": "planet",
        "description": "Dark industrial world where the Union manufactures its most advanced technology, hidden from prying eyes",
        "faction": "technocrat_union",
        "services": ["manufacturing", "market", "refinery", "shipyard"],
        "resources": [],
        "danger_level": 0.35,
        "connections": ["singularity_reach", "synthesis_planet", "circuit_fields"]
    },
    "circuit_fields": {
        "name": "Circuit Fields",
        "type": "asteroid",
        "description": "Metallic asteroids arranged in perfect geometric patterns by Union drones",
        "faction": None,
        "services": [],
        "resources": ["raw_titanite", "raw_voltium", "raw_neuralfiber"],
        "danger_level": 0.3,
        "connections": ["void_forge", "binary_belt"]
    },
    "recursion_point": {
        "name": "Recursion Point",
        "type": "asteroid",
        "description": "Bizarre belt where asteroids seem to repeat in fractal patterns",
        "faction": None,
        "services": [],
        "resources": ["raw_synthcrystal", "raw_quantum_dust", "raw_chronite"],
        "anomalies": True,
        "danger_level": 0.55,
        "connections": ["singularity_reach", "quantum_drift"]
    },
    "silicon_spire": {
        "name": "Silicon Spire Station",
        "type": "station",
        "description": "Towering vertical station resembling a crystalline needle, serving as the Union's outpost for consciousness upload research",
        "faction": "technocrat_union",
        "services": ["research", "market", "contracts"],
        "resources": [],
        "danger_level": 0.32,
        "connections": ["datacore_prime", "neural_network", "algorithm_expanse"]
    },
    "algorithm_expanse": {
        "name": "Algorithm Expanse",
        "type": "space",
        "description": "Space sector filled with Union monitoring arrays, tracking every vessel's movement with cold precision",
        "faction": "technocrat_union",
        "services": [],
        "resources": [],
        "danger_level": 0.4,
        "connections": ["silicon_spire", "protocol_labs"]
    },
    "convergence_nexus": {
        "name": "Convergence Nexus",
        "type": "planet",
        "description": "Entirely mechanized world where organic life has been replaced by perfect machine efficiency under Union control",
        "faction": "technocrat_union",
        "services": ["manufacturing", "market", "research", "shipyard"],
        "resources": [],
        "danger_level": 0.38,
        "connections": ["void_forge", "silicon_spire"]
    },

    # ========== CIPHER DOMINION TERRITORY (Military & Industry) ==========
    "bastion_prime": {
        "name": "Bastion Prime",
        "type": "station",
        "description": "Imposing military fortress bristling with weapons, serving as the Dominion's forward command center",
        "faction": "cipher_dominion",
        "services": ["market", "contracts", "shipyard", "repair"],
        "resources": [],
        "danger_level": 0.5,
        "connections": ["crimson_expanse", "ironhold_world", "warforge_belt", "garrison_outpost"]
    },
    "warforge_belt": {
        "name": "Warforge Belt",
        "type": "asteroid",
        "description": "Heavily mined belt supplying the Dominion war machine",
        "faction": None,
        "services": [],
        "resources": ["raw_titanite", "raw_voltium", "raw_nexium"],
        "danger_level": 0.55,
        "connections": ["bastion_prime", "ironhold_sectors"]
    },
    "garrison_outpost": {
        "name": "Garrison Outpost",
        "type": "station",
        "description": "Stark military installation where Dominion soldiers drill endlessly, preparing for the next conquest",
        "faction": "cipher_dominion",
        "services": ["contracts", "market", "shipyard"],
        "resources": [],
        "danger_level": 0.58,
        "connections": ["bastion_prime", "crimson_expanse", "bloodstone_fields"]
    },
    "bloodstone_fields": {
        "name": "Bloodstone Fields",
        "type": "asteroid",
        "description": "Red-hued asteroids marking the boundary of Dominion aggression",
        "faction": None,
        "services": [],
        "resources": ["raw_chronite", "raw_nexium", "raw_titanite"],
        "danger_level": 0.62,
        "connections": ["garrison_outpost", "conquest_reach"]
    },
    "conquest_reach": {
        "name": "Conquest Reach",
        "type": "station",
        "description": "Battle-scarred station serving as the Dominion's staging ground for territorial expansion into contested space",
        "faction": "cipher_dominion",
        "services": ["contracts", "manufacturing", "market", "shipyard"],
        "resources": [],
        "danger_level": 0.65,
        "connections": ["bloodstone_fields", "vanguard_citadel", "contested_zone"]
    },
    "contested_zone": {
        "name": "Contested Zone",
        "type": "space",
        "description": "Active warzone where Dominion forces clash with resistance fighters",
        "faction": "cipher_dominion",
        "services": [],
        "resources": [],
        "danger_level": 0.75,
        "connections": ["conquest_reach", "crimson_expanse"]
    },
    "vanguard_citadel": {
        "name": "Vanguard Citadel",
        "type": "planet",
        "description": "Fortress world encased in armor plating, representing the Dominion's military might and ruthless efficiency",
        "faction": "cipher_dominion",
        "services": ["manufacturing", "market", "shipyard", "contracts"],
        "resources": [],
        "danger_level": 0.6,
        "connections": ["conquest_reach", "ironhold_world", "sovereign_belt", "garrison_outpost"]
    },
    "sovereign_belt": {
        "name": "Sovereign Belt",
        "type": "asteroid",
        "description": "Dominion-controlled mining belt operated by forced labor",
        "faction": None,
        "services": [],
        "resources": ["raw_neuralfiber", "raw_voltium", "raw_titanite"],
        "danger_level": 0.53,
        "connections": ["vanguard_citadel", "warforge_belt"]
    },
    "dreadnought_yards": {
        "name": "Dreadnought Yards",
        "type": "station",
        "description": "Massive shipyard complex where the Dominion constructs its fearsome capital ships, each vessel a testament to overwhelming force",
        "faction": "cipher_dominion",
        "services": ["shipyard", "manufacturing", "market", "contracts"],
        "resources": [],
        "danger_level": 0.63,
        "connections": ["vanguard_citadel", "bastion_prime", "iron_expanse", "garrison_outpost"]
    },
    "iron_expanse": {
        "name": "Iron Expanse",
        "type": "asteroid",
        "description": "Vast belt of pure metallic asteroids, jealously guarded by Dominion patrols",
        "faction": None,
        "services": [],
        "resources": ["raw_titanite", "raw_chronite", "raw_nexium"],
        "danger_level": 0.58,
        "connections": ["dreadnought_yards", "ironhold_sectors"]
    },
    "supremacy_throne": {
        "name": "Supremacy Throne",
        "type": "planet",
        "description": "Capital world of the Cipher Dominion, where absolute loyalty is demanded and dissent is crushed beneath iron rule",
        "faction": "cipher_dominion",
        "services": ["market", "contracts", "manufacturing", "shipyard", "refinery"],
        "resources": [],
        "danger_level": 0.68,
        "connections": ["vanguard_citadel", "dreadnought_yards", "bastion_prime"]
    },

    # ========== VOID CORSAIRS TERRITORY (Pirate Haven - Most Dangerous) ==========
    "phantom_reach": {
        "name": "Phantom Reach",
        "type": "station",
        "description": "Ghostly station materializing from the void, where Corsair captains trade in stolen goods and forbidden technology",
        "faction": "void_corsairs",
        "services": ["black_market", "contracts", "repair"],
        "resources": [],
        "danger_level": 0.8,
        "connections": ["shadow_nebula", "corsair_haven", "reaver_belt"]
    },
    "reaver_belt": {
        "name": "Reaver's Belt",
        "type": "asteroid",
        "description": "Treacherous field littered with wreckage from Corsair raids",
        "faction": None,
        "services": [],
        "resources": ["raw_darkwater", "raw_synthcrystal", "raw_quantum_dust"],
        "anomalies": True,
        "danger_level": 0.85,
        "connections": ["phantom_reach", "dead_zone_asteroids", "dread_maw"]
    },
    "dread_maw": {
        "name": "Dread Maw",
        "type": "station",
        "description": "Nightmarish station built from salvaged warships, its corridors echo with the tales of the Void's most infamous pirates",
        "faction": "void_corsairs",
        "services": ["black_market", "shipyard", "contracts"],
        "resources": [],
        "danger_level": 0.88,
        "connections": ["reaver_belt", "abyss_edge", "corsair_haven"]
    },
    "abyss_edge": {
        "name": "Abyss Edge",
        "type": "asteroid",
        "description": "Darkest reaches of known space, where reality itself seems to fray",
        "faction": None,
        "services": [],
        "resources": ["raw_darkwater", "raw_synthcrystal", "raw_chronite"],
        "anomalies": True,
        "danger_level": 0.92,
        "connections": ["dread_maw", "oblivion_gate"]
    },
    "oblivion_gate": {
        "name": "Oblivion Gate",
        "type": "space",
        "description": "Mysterious void phenomenon where Corsair warlords reign supreme, far beyond the reach of civilized law",
        "faction": "void_corsairs",
        "services": [],
        "resources": [],
        "anomalies": True,
        "danger_level": 0.95,
        "connections": ["abyss_edge", "dread_maw", "shadow_nebula"]
    }
}

# Fix bidirectional connections - Part 1
LOCATIONS["axiom_labs"]["connections"].extend(["protocol_labs", "singularity_reach"])
LOCATIONS["bastion_prime"]["connections"].extend(["dreadnought_yards", "supremacy_throne"])
LOCATIONS["binary_belt"]["connections"].extend(["circuit_fields"])
LOCATIONS["chronos_expanse"]["connections"].extend(["quantum_drift"])
LOCATIONS["corsair_haven"]["connections"].extend(["phantom_reach", "dread_maw"])
LOCATIONS["crimson_expanse"]["connections"].extend(["bastion_prime", "garrison_outpost", "contested_zone"])
LOCATIONS["datacore_prime"]["connections"].extend(["silicon_spire"])
LOCATIONS["dead_zone_asteroids"]["connections"].extend(["reaver_belt"])
LOCATIONS["dread_maw"]["connections"].extend(["oblivion_gate"])
LOCATIONS["dreadnought_yards"]["connections"].extend(["supremacy_throne"])
LOCATIONS["eden_prime"]["connections"].extend(["horizon_vista"])
LOCATIONS["forge_station"]["connections"].extend(["ironhold_world", "pristine_fields", "binary_belt"])
LOCATIONS["harvest_fields"]["connections"].extend(["tranquil_belt", "sapphire_fields"])
LOCATIONS["ironhold_sectors"]["connections"].extend(["warforge_belt", "iron_expanse"])
LOCATIONS["ironhold_world"]["connections"].extend(["bastion_prime", "vanguard_citadel"])
LOCATIONS["meridian_gates"]["connections"].extend(["merchant_corridor", "explorer_outpost", "uncharted_expanse"])
LOCATIONS["neural_network"]["connections"].extend(["chronos_expanse", "datacore_prime", "silicon_spire"])
LOCATIONS["nexus_prime"]["connections"].extend(["starlight_waystation", "tranquil_belt", "freeport_exchange"])
LOCATIONS["outer_belts"]["connections"].extend(["harvest_fields", "starlight_waystation"])
LOCATIONS["prosperity_hub"]["connections"].extend(["horizon_vista"])
LOCATIONS["protocol_labs"]["connections"].extend(["algorithm_expanse"])
LOCATIONS["quantum_drift"]["connections"].extend(["recursion_point"])
LOCATIONS["sapphire_fields"]["connections"].extend(["verdant_belt"])
LOCATIONS["shadow_nebula"]["connections"].extend(["phantom_reach", "oblivion_gate"])
LOCATIONS["silicon_spire"]["connections"].extend(["convergence_nexus"])
LOCATIONS["singularity_reach"]["connections"].extend(["recursion_point"])
LOCATIONS["synthesis_planet"]["connections"].extend(["chronos_expanse", "datacore_prime", "void_forge"])
LOCATIONS["titan_alpha"]["connections"].extend(["freeport_exchange", "aurora_reach", "sapphire_fields", "eden_prime"])
LOCATIONS["aurora_reach"]["connections"].extend(["merchant_corridor", "explorer_outpost"])
LOCATIONS["garrison_outpost"]["connections"].extend(["vanguard_citadel", "dreadnought_yards"])
LOCATIONS["vanguard_citadel"]["connections"].extend(["dreadnought_yards", "supremacy_throne"])
LOCATIONS["void_forge"]["connections"].extend(["convergence_nexus"])
LOCATIONS["warforge_belt"]["connections"].extend(["sovereign_belt"])

# ============= FACTIONS (Updated with Loyalty System) =============
FACTIONS = {
    "meridian_collective": {
        "name": "Meridian Collective",
        "description": "Democratic alliance of outer colonies focused on trade and exploration",
        "territory": [
            "nexus_prime", "meridian_gates", "titan_alpha", "aurora_reach", "prosperity_hub",
            "eden_prime", "explorer_outpost", "horizon_vista", "merchant_corridor"
        ],
        "standing": "neutral",
        "relations": {"cipher_dominion": -0.3, "void_corsairs": -0.5, "technocrat_union": 0.4},
        "bonuses": {"trade": 0.15, "exploration": 0.10}
    },
    "cipher_dominion": {
        "name": "Cipher Dominion",
        "description": "Militaristic empire seeking territorial expansion through force",
        "territory": [
            "crimson_expanse", "ironhold_sectors", "ironhold_world", "bastion_prime", "garrison_outpost",
            "conquest_reach", "vanguard_citadel", "dreadnought_yards", "supremacy_throne", "contested_zone"
        ],
        "standing": "hostile",
        "relations": {"meridian_collective": -0.3, "void_corsairs": 0.2, "technocrat_union": -0.6},
        "bonuses": {"combat": 0.20, "territory_control": 0.15}
    },
    "technocrat_union": {
        "name": "Technocrat Union",
        "description": "Scientific cabal pursuing technological supremacy and innovation",
        "territory": [
            "axiom_labs", "synthesis_planet", "neural_network", "forge_station", "datacore_prime",
            "protocol_labs", "singularity_reach", "void_forge", "silicon_spire", "convergence_nexus"
        ],
        "standing": "friendly",
        "relations": {"meridian_collective": 0.4, "cipher_dominion": -0.6, "void_corsairs": -0.2},
        "bonuses": {"research": 0.25, "manufacturing": 0.15, "refining": 0.10}
    },
    "void_corsairs": {
        "name": "Void Corsairs",
        "description": "Pirate syndicate and outlaws operating from hidden bases",
        "territory": [
            "shadow_nebula", "corsair_haven", "blackmarket_dock", "phantom_reach", "dread_maw", "oblivion_gate"
        ],
        "standing": "hostile",
        "relations": {"meridian_collective": -0.5, "cipher_dominion": 0.2, "technocrat_union": -0.2},
        "bonuses": {"stealth": 0.20, "black_market": 0.30}
    }
}

# ============= FACTION LOYALTY SYSTEM =============
# Loyalty ranges: -100 to 100
# Completing faction contracts increases loyalty
# Attacking faction members decreases loyalty
FACTION_LOYALTY_TIERS = {
    "reviled": {"min": -100, "max": -50, "loot_multiplier": 0.0, "contract_multiplier": 0.5, "description": "Kill on sight"},
    "hostile": {"min": -49, "max": -10, "loot_multiplier": 0.0, "contract_multiplier": 0.7, "description": "Unwelcome"},
    "neutral": {"min": -9, "max": 9, "loot_multiplier": 0.5, "contract_multiplier": 1.0, "description": "Unknown"},
    "friendly": {"min": 10, "max": 29, "loot_multiplier": 0.7, "contract_multiplier": 1.2, "description": "Accepted"},
    "honored": {"min": 30, "max": 59, "loot_multiplier": 0.9, "contract_multiplier": 1.5, "description": "Respected"},
    "revered": {"min": 60, "max": 89, "loot_multiplier": 1.2, "contract_multiplier": 2.0, "description": "Esteemed ally"},
    "exalted": {"min": 90, "max": 100, "loot_multiplier": 1.5, "contract_multiplier": 2.5, "description": "Legendary hero"}
}

# ============= CONTRACT TYPES (Updated) =============
CONTRACT_TYPES = {
    "mining_contract": {
        "name": "Resource Extraction",
        "description": "Mine and deliver specific raw resources",
        "requirements": {"skill": "mining_operations", "min_level": 1},
        "reward_range": (10000, 50000),
        "time_limit": 3600
    },
    "refining_contract": {
        "name": "Resource Refining",
        "description": "Refine raw materials into processed resources",
        "requirements": {"skill": "refining", "min_level": 1},
        "reward_range": (15000, 60000),
        "time_limit": 2400
    },
    "manufacturing_contract": {
        "name": "Component Manufacturing",
        "description": "Build specified ship modules",
        "requirements": {"skill": "module_manufacturing", "min_level": 2},
        "reward_range": (25000, 100000),
        "time_limit": 3600
    },
    "combat_patrol": {
        "name": "Combat Patrol",
        "description": "Eliminate hostile targets in a sector",
        "requirements": {"skill": "weapons_mastery", "min_level": 2},
        "reward_range": (25000, 100000),
        "time_limit": 1800
    },
    "cargo_transport": {
        "name": "Cargo Transport",
        "description": "Deliver goods between locations",
        "requirements": {"vessel_cargo": 500},
        "reward_range": (15000, 75000),
        "time_limit": 2400
    },
    "reconnaissance": {
        "name": "Reconnaissance Mission",
        "description": "Scout and scan designated areas",
        "requirements": {"skill": "scanning", "min_level": 1},
        "reward_range": (20000, 60000),
        "time_limit": 1800
    },
    "research_data": {
        "name": "Research Data Collection",
        "description": "Gather scientific data from anomalies",
        "requirements": {"skill": "scanning", "min_level": 3},
        "reward_range": (40000, 150000),
        "time_limit": 4800
    }
}

# ============= NPC ENEMY TEMPLATES BY LEVEL =============
NPC_ENEMY_TEMPLATES = {
    "level_1_5": {
        "names": ["Pirate Scout", "Raider Probe", "Outlaw Runner", "Scavenger"],
        "ship_types": ["scout_standard_mk1", "scout_standard_mk2"],
        "weapon_setups": ["pulse_cannon_t1"],
        "defense_setups": ["aegis_shield_t1"],
        "credits_reward": (500, 2000),
        "xp_reward": (50, 150)
    },
    "level_6_10": {
        "names": ["Pirate Frigate", "Raider Destroyer", "Corsair Hunter", "Marauder"],
        "ship_types": ["fighter_standard_mk2", "fighter_advanced_mk1", "scout_advanced_mk2"],
        "weapon_setups": ["pulse_cannon_t1", "pulse_cannon_t2"],
        "defense_setups": ["aegis_shield_t1", "fortress_plating_t1"],
        "credits_reward": (2000, 5000),
        "xp_reward": (150, 400)
    },
    "level_11_15": {
        "names": ["Pirate Cruiser", "Void Marauder", "Corsair Battlecruiser", "Elite Raider"],
        "ship_types": ["cruiser_standard_mk2", "cruiser_advanced_mk1", "fighter_elite_mk1"],
        "weapon_setups": ["pulse_cannon_t2", "plasma_lance_t1", "void_torpedo_t1"],
        "defense_setups": ["aegis_shield_t2", "fortress_plating_t1"],
        "credits_reward": (5000, 15000),
        "xp_reward": (400, 1000)
    },
    "level_16_20": {
        "names": ["Pirate Dreadnought", "Void Destroyer", "Corsair Capital", "Warlord"],
        "ship_types": ["destroyer_standard_mk2", "cruiser_advanced_mk2", "battleship_standard_mk1"],
        "weapon_setups": ["plasma_lance_t1", "void_torpedo_t1"],
        "defense_setups": ["aegis_shield_t2", "phantom_cloak_t1"],
        "credits_reward": (15000, 40000),
        "xp_reward": (1000, 2500)
    },
    "level_21_plus": {
        "names": ["Elite Warlord", "Corsair Admiral", "Void Commander", "Pirate Lord"],
        "ship_types": ["battleship_advanced_mk2", "battleship_elite_mk1", "destroyer_advanced_mk2"],
        "weapon_setups": ["plasma_lance_t1", "void_torpedo_t1"],
        "defense_setups": ["aegis_shield_t2", "fortress_plating_t1", "phantom_cloak_t1"],
        "credits_reward": (40000, 100000),
        "xp_reward": (2500, 5000)
    }
}



# ============= FACTION ITEMS (Uncraftable - Mission/Combat Rewards Only) =============
from faction_items import FACTION_SHIPS, FACTION_COMPONENTS, FACTION_MISSION_REWARDS, FACTION_COMBAT_LOOT

# Integrate faction ships into VESSEL_CLASSES
VESSEL_CLASSES.update(FACTION_SHIPS)

# Integrate faction components into SHIP_COMPONENTS  
SHIP_COMPONENTS.update(FACTION_COMPONENTS)

