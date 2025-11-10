"""
Faction-Specific Ships and Components
These items cannot be crafted - only obtained through missions and combat
"""

# Faction Ships - Superior to standard ships of same class
FACTION_SHIPS = {
    # Meridian Collective - Trade and Exploration focus
    "meridian_envoy": {
        "name": "Meridian Envoy",
        "class": "cruiser",
        "class_type": "cruiser",
        "variant": "faction",
        "tier": "mk2",
        "tier_num": 2,
        "faction": "meridian_collective",
        "description": "Diplomatic vessel with enhanced cargo and speed",
        "level_requirement": 10,
        "hull_hp": 18000,  # +20% vs standard cruiser mk2
        "shield_capacity": 10000,
        "armor_rating": 180,
        "cargo_capacity": 2400,  # +50% cargo
        "base_speed": 65,  # +30% speed
        "module_slots": {"weapon": 2, "defense": 2, "utility": 3, "engine": 2}
    },
    "meridian_pathfinder": {
        "name": "Meridian Pathfinder",
        "class": "scout",
        "class_type": "scout",
        "variant": "faction",
        "tier": "mk3",
        "tier_num": 3,
        "faction": "meridian_collective",
        "description": "Advanced exploration ship with superior sensors",
        "level_requirement": 15,
        "hull_hp": 14000,
        "shield_capacity": 8000,
        "armor_rating": 150,
        "cargo_capacity": 1000,
        "base_speed": 95,  # Very fast
        "module_slots": {"weapon": 1, "defense": 2, "utility": 4, "engine": 3}
    },

    # Cipher Dominion - Military focus
    "cipher_destroyer": {
        "name": "Cipher Destroyer",
        "class": "destroyer",
        "class_type": "destroyer",
        "variant": "faction",
        "tier": "mk2",
        "tier_num": 2,
        "faction": "cipher_dominion",
        "description": "Heavy assault vessel with devastating firepower",
        "level_requirement": 14,
        "hull_hp": 35000,  # +25% vs standard
        "shield_capacity": 18000,  # +25% vs standard
        "armor_rating": 420,  # +20% vs standard
        "cargo_capacity": 800,
        "base_speed": 35,
        "module_slots": {"weapon": 5, "defense": 3, "utility": 1, "engine": 2}
    },
    "cipher_interceptor": {
        "name": "Cipher Interceptor",
        "class": "fighter",
        "class_type": "fighter",
        "variant": "faction",
        "tier": "mk2",
        "tier_num": 2,
        "faction": "cipher_dominion",
        "description": "Elite combat fighter with enhanced weapons",
        "level_requirement": 10,
        "hull_hp": 10000,  # +25% vs standard
        "shield_capacity": 6000,
        "armor_rating": 160,
        "cargo_capacity": 200,
        "base_speed": 75,
        "module_slots": {"weapon": 4, "defense": 2, "utility": 1, "engine": 2}
    },

    # Technocrat Union - Technology focus
    "technocrat_innovator": {
        "name": "Technocrat Innovator",
        "class": "refinery",
        "class_type": "refinery",
        "variant": "faction",
        "tier": "mk2",
        "tier_num": 2,
        "faction": "technocrat_union",
        "description": "Advanced industrial ship with superior efficiency",
        "level_requirement": 12,
        "hull_hp": 22000,
        "shield_capacity": 12000,
        "armor_rating": 280,
        "cargo_capacity": 3200,  # +60% cargo
        "base_speed": 30,
        "module_slots": {"weapon": 1, "defense": 2, "utility": 5, "engine": 1}
    },
    "technocrat_vanguard": {
        "name": "Technocrat Vanguard",
        "class": "battleship",
        "class_type": "battleship",
        "variant": "faction",
        "tier": "mk2",
        "tier_num": 2,
        "faction": "technocrat_union",
        "description": "Experimental warship with advanced shielding",
        "level_requirement": 16,
        "hull_hp": 40000,
        "shield_capacity": 28000,  # +40% shields
        "armor_rating": 450,
        "cargo_capacity": 1200,
        "base_speed": 25,
        "module_slots": {"weapon": 4, "defense": 4, "utility": 2, "engine": 2}
    },

    # Void Corsairs - Pirate/Raider focus
    "corsair_marauder": {
        "name": "Corsair Marauder",
        "class": "hauler",
        "class_type": "hauler",
        "variant": "faction",
        "tier": "mk2",
        "tier_num": 2,
        "faction": "void_corsairs",
        "description": "Stolen and modified cargo vessel for raids",
        "level_requirement": 10,
        "hull_hp": 16000,
        "shield_capacity": 9000,
        "armor_rating": 200,
        "cargo_capacity": 2800,  # Large cargo
        "base_speed": 45,  # Fast for a hauler
        "module_slots": {"weapon": 3, "defense": 2, "utility": 2, "engine": 2}
    },
    "corsair_reaver": {
        "name": "Corsair Reaver",
        "class": "carrier",
        "class_type": "carrier",
        "variant": "faction",
        "tier": "mk2",
        "tier_num": 2,
        "faction": "void_corsairs",
        "description": "Pirate command ship with hidden weapon bays",
        "level_requirement": 14,
        "hull_hp": 32000,
        "shield_capacity": 16000,
        "armor_rating": 340,
        "cargo_capacity": 2000,
        "base_speed": 32,
        "module_slots": {"weapon": 4, "defense": 3, "utility": 3, "engine": 2}
    }
}

# Faction Components - Better than T3 standard components
FACTION_COMPONENTS = {
    # Meridian Collective - Trade & Exploration bonuses
    "meridian_advanced_scanner": {
        "name": "Meridian Advanced Scanner Suite",
        "type": "sensor_suite",
        "faction": "meridian_collective",
        "tier": "faction",
        "description": "State-of-the-art sensor array - Faction grade",
        "level_requirement": 12,
        "sensor_bonus": 5.0,  # vs 3.0 for T3
        "special_bonus": {"cargo_scan_range": 2.0, "anomaly_detection": 1.5}
    },
    "meridian_efficient_core": {
        "name": "Meridian Efficient Power Core",
        "type": "power_core",
        "faction": "meridian_collective",
        "tier": "faction",
        "description": "Highly efficient power generation - Faction grade",
        "level_requirement": 12,
        "power_bonus": 4.5,  # vs 3.0 for T3
        "special_bonus": {"fuel_efficiency": 1.5, "power_stability": 1.3}
    },

    # Cipher Dominion - Combat bonuses
    "cipher_assault_mount": {
        "name": "Cipher Assault Weapon Mount",
        "type": "weapon_mount",
        "faction": "cipher_dominion",
        "tier": "faction",
        "description": "Military-grade weapon hardpoint - Faction grade",
        "level_requirement": 13,
        "weapon_bonus": 5.0,  # vs 3.0 for T3
        "special_bonus": {"weapon_damage": 1.4, "fire_rate": 1.2}
    },
    "cipher_fortified_hull": {
        "name": "Cipher Fortified Hull Frame",
        "type": "hull_frame",
        "faction": "cipher_dominion",
        "tier": "faction",
        "description": "Reinforced military hull - Faction grade",
        "level_requirement": 13,
        "hull_bonus": 5.0,  # vs 3.0 for T3
        "special_bonus": {"armor_rating": 1.3, "hull_repair": 1.2}
    },

    # Technocrat Union - Tech bonuses
    "technocrat_quantum_shield": {
        "name": "Technocrat Quantum Shield Generator",
        "type": "shield_generator",
        "faction": "technocrat_union",
        "tier": "faction",
        "description": "Experimental shield technology - Faction grade",
        "level_requirement": 14,
        "shield_bonus": 5.5,  # vs 3.0 for T3
        "special_bonus": {"shield_recharge": 1.5, "shield_efficiency": 1.3}
    },
    "technocrat_ai_system": {
        "name": "Technocrat AI Computer System",
        "type": "computer_system",
        "faction": "technocrat_union",
        "tier": "faction",
        "description": "Advanced AI processor - Faction grade",
        "level_requirement": 14,
        "computer_bonus": 5.0,  # vs 3.0 for T3
        "special_bonus": {"auto_targeting": 1.4, "system_optimization": 1.3}
    },

    # Void Corsairs - Raider bonuses
    "corsair_stealth_thruster": {
        "name": "Corsair Stealth Thruster Array",
        "type": "thruster_array",
        "faction": "void_corsairs",
        "tier": "faction",
        "description": "Modified for speed and evasion - Faction grade",
        "level_requirement": 11,
        "speed_bonus": 5.5,  # vs 3.0 for T3
        "special_bonus": {"evasion": 1.4, "stealth": 1.2}
    },
    "corsair_survival_system": {
        "name": "Corsair Survival Life Support",
        "type": "life_support",
        "faction": "void_corsairs",
        "tier": "faction",
        "description": "Rugged life support for harsh conditions - Faction grade",
        "level_requirement": 11,
        "life_support_bonus": 4.5,  # vs 3.0 for T3
        "special_bonus": {"crew_survival": 1.3, "environmental_resist": 1.4}
    }
}

# Mission reward tables - chances to get faction items
FACTION_MISSION_REWARDS = {
    "meridian_collective": {
        "ships": ["meridian_envoy", "meridian_pathfinder"],
        "components": ["meridian_advanced_scanner", "meridian_efficient_core"],
        "min_reputation": 75,  # Need good rep
        "reward_chance": 0.15  # 15% chance on high-level missions
    },
    "cipher_dominion": {
        "ships": ["cipher_destroyer", "cipher_interceptor"],
        "components": ["cipher_assault_mount", "cipher_fortified_hull"],
        "min_reputation": 70,
        "reward_chance": 0.15
    },
    "technocrat_union": {
        "ships": ["technocrat_innovator", "technocrat_vanguard"],
        "components": ["technocrat_quantum_shield", "technocrat_ai_system"],
        "min_reputation": 80,  # Higher rep needed
        "reward_chance": 0.12  # Rarer
    },
    "void_corsairs": {
        "ships": ["corsair_marauder", "corsair_reaver"],
        "components": ["corsair_stealth_thruster", "corsair_survival_system"],
        "min_reputation": -50,  # Need negative rep (pirate faction)
        "reward_chance": 0.10  # Rare from pirate missions
    }
}

# Combat loot tables - drop chances from faction enemies
FACTION_COMBAT_LOOT = {
    "meridian_collective": {
        "component_drop_chance": 0.08,  # 8% chance
        "component_pool": ["meridian_advanced_scanner", "meridian_efficient_core"],
        "ship_drop_chance": 0.02  # 2% chance - very rare
    },
    "cipher_dominion": {
        "component_drop_chance": 0.10,  # 10% chance (military loot)
        "component_pool": ["cipher_assault_mount", "cipher_fortified_hull"],
        "ship_drop_chance": 0.03
    },
    "technocrat_union": {
        "component_drop_chance": 0.06,  # 6% chance (rare tech)
        "component_pool": ["technocrat_quantum_shield", "technocrat_ai_system"],
        "ship_drop_chance": 0.01  # 1% - experimental ships rare
    },
    "void_corsairs": {
        "component_drop_chance": 0.12,  # 12% chance (pirates have loot)
        "component_pool": ["corsair_stealth_thruster", "corsair_survival_system"],
        "ship_drop_chance": 0.04  # 4% - stolen ships
    }
}
