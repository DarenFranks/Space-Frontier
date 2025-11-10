"""
Combat System
Handles tactical vessel combat
"""

import random
from typing import Dict, List, Optional
from vessels import Vessel
from data import MODULES, RAW_RESOURCES, RESOURCES, COMMODITIES


class CombatEncounter:
    """Represents a combat engagement"""

    def __init__(self, player_vessel: Vessel, enemy_vessel: Vessel, enemy_name: str, player_level: int = 1):
        self.player_vessel = player_vessel
        self.enemy_vessel = enemy_vessel
        self.enemy_name = enemy_name
        self.player_level = player_level

        self.turn_number = 0
        self.combat_log: List[str] = []
        self.is_active = True

        self.player_actions_used = 0
        self.enemy_actions_used = 0

        # Calculate rewards based on player level
        self.rewards = self._calculate_rewards()

    def _calculate_rewards(self) -> Dict:
        """Calculate credits and XP rewards based on player level"""
        from data import NPC_ENEMY_TEMPLATES

        # Determine which template based on player level
        if self.player_level <= 5:
            template_key = "level_1_5"
        elif self.player_level <= 10:
            template_key = "level_6_10"
        elif self.player_level <= 15:
            template_key = "level_11_15"
        elif self.player_level <= 20:
            template_key = "level_16_20"
        else:
            template_key = "level_21_plus"

        template = NPC_ENEMY_TEMPLATES[template_key]

        # Random reward within range
        credits = random.randint(*template["credits_reward"])
        xp = random.randint(*template["xp_reward"])

        # Generate loot drops
        loot = self._generate_loot()

        return {"credits": credits, "xp": xp, "loot": loot}

    def _generate_loot(self) -> Dict[str, int]:
        """Generate random loot drops from defeated enemy"""
        loot = {}

        # Loot drop chances based on player level (higher level = better loot chance)
        base_chance = 0.3 + (self.player_level * 0.02)  # 30% at level 1, up to 70% at level 20+
        base_chance = min(base_chance, 0.7)  # Cap at 70%

        # 1. Modules (lowest drop rate - 15-25% chance)
        module_chance = base_chance * 0.3
        if random.random() < module_chance:
            # Get appropriate tier modules based on player level
            tier = "t1"
            if self.player_level >= 10:
                tier = "t2"

            # Get all modules of this tier
            available_modules = [m_id for m_id, m_data in MODULES.items()
                               if tier in m_id and m_data.get("tier", 1) <= 2]

            if available_modules:
                module_id = random.choice(available_modules)
                loot[module_id] = 1

        # 2. Raw ore (40-50% chance)
        ore_chance = base_chance * 0.6
        if random.random() < ore_chance:
            ore_list = list(RAW_RESOURCES.keys())
            ore_id = random.choice(ore_list)
            quantity = random.randint(3, 10 + self.player_level)
            loot[ore_id] = quantity

        # 3. Refined ore (30-40% chance)
        refined_chance = base_chance * 0.5
        if random.random() < refined_chance:
            # Get refined resources
            refined_list = [r_id for r_id in RESOURCES.keys() if r_id not in RAW_RESOURCES]
            if refined_list:
                refined_id = random.choice(refined_list)
                quantity = random.randint(2, 5 + int(self.player_level / 2))
                loot[refined_id] = quantity

        # 4. Commodities (50-60% chance)
        commodity_chance = base_chance * 0.8
        if random.random() < commodity_chance:
            # Pick random commodity - prefer lower cost items
            commodity_list = list(COMMODITIES.keys())

            # Weight selection toward cheaper items (more common loot)
            commodity_id = random.choice(commodity_list)
            commodity_data = COMMODITIES[commodity_id]

            # Less expensive = more quantity
            if commodity_data["base_price"] < 50:
                quantity = random.randint(5, 20)
            elif commodity_data["base_price"] < 200:
                quantity = random.randint(2, 10)
            elif commodity_data["base_price"] < 1000:
                quantity = random.randint(1, 5)
            else:
                quantity = random.randint(1, 2)

            loot[commodity_id] = quantity

        return loot

    def player_attack(self, weapon_index: int = 0, skill_bonus: float = 0.0) -> Dict:
        """Player attacks enemy with ALL installed weapons"""
        if not self.is_active:
            return {"success": False, "message": "Combat has ended"}

        # Get player weapons
        player_weapons = self.player_vessel.installed_modules.get("weapon", [])

        if not player_weapons:
            return {"success": False, "message": "No weapons installed"}

        total_damage = 0
        hits = 0
        misses = 0
        critical_hits = 0
        weapon_details = []
        enemy_evasion = self.enemy_vessel.get_evasion_chance()

        # Fire ALL weapons
        for weapon_id in player_weapons:
            weapon_data = MODULES[weapon_id]

            # Calculate hit chance
            base_accuracy = weapon_data.get("accuracy", 0.85)
            hit_chance = base_accuracy * (1 - enemy_evasion) * (1 + skill_bonus)

            # Determine if hit
            if random.random() > hit_chance:
                misses += 1
                weapon_details.append(f"{weapon_data['name']}: MISS")
                continue

            # Calculate damage for this weapon
            base_damage = weapon_data.get("damage", 100)
            damage_multiplier = 1.0 + skill_bonus

            # Critical hit chance (per weapon)
            is_crit = random.random() < 0.15
            if is_crit:
                damage_multiplier *= 2.0
                critical_hits += 1

            weapon_damage = base_damage * damage_multiplier
            total_damage += weapon_damage
            hits += 1

            # Track weapon performance
            crit_label = " [CRIT]" if is_crit else ""
            weapon_details.append(f"{weapon_data['name']}: {weapon_damage:.0f}{crit_label}")

        # Check if all weapons missed
        if hits == 0:
            msg = f"All weapons missed! ({misses} weapons)"
            self.combat_log.append(msg)
            return {"success": True, "message": msg, "hit": False}

        # Apply total damage to enemy
        damage_report = self.enemy_vessel.take_damage(total_damage)

        # Generate detailed message
        weapon_count = len(player_weapons)
        msg = f"{'CRITICAL! ' if critical_hits > 0 else ''}{hits}/{weapon_count} weapons hit for {total_damage:.0f} total damage!"

        if damage_report["shield_damage"] > 0:
            msg += f"\n  └─ {damage_report['shield_damage']:.0f} to shields"

        if damage_report["hull_damage"] > 0:
            msg += f"\n  └─ {damage_report['hull_damage']:.0f} to hull"

        # Add weapon breakdown
        msg += f"\n  Weapons: {', '.join(weapon_details)}"

        self.combat_log.append(msg)

        # Check if enemy destroyed
        if damage_report["destroyed"]:
            self.is_active = False
            destroy_msg = f"Enemy {self.enemy_name} destroyed!"
            self.combat_log.append(destroy_msg)

        return {
            "success": True,
            "message": msg,
            "hit": True,
            "damage": total_damage,
            "critical": critical_hits > 0,
            "enemy_destroyed": damage_report["destroyed"],
            "hits": hits,
            "misses": misses
        }

    def enemy_attack(self, skill_bonus: float = 0.0) -> Dict:
        """Enemy attacks player with ALL installed weapons"""
        if not self.is_active:
            return {"success": False, "message": "Combat has ended"}

        # Get enemy weapons
        enemy_weapons = self.enemy_vessel.installed_modules.get("weapon", [])

        if not enemy_weapons:
            return {"success": False, "message": "Enemy has no weapons"}

        total_damage = 0
        hits = 0
        misses = 0
        weapon_details = []
        player_evasion = self.player_vessel.get_evasion_chance()

        # Fire ALL weapons
        for weapon_id in enemy_weapons:
            weapon_data = MODULES[weapon_id]

            # Calculate hit chance
            base_accuracy = weapon_data.get("accuracy", 0.85)
            hit_chance = base_accuracy * (1 - player_evasion)

            # Determine if hit
            if random.random() > hit_chance:
                misses += 1
                weapon_details.append(f"{weapon_data['name']}: MISS")
                continue

            # Calculate damage for this weapon (reduced by 20% for pirates)
            base_damage = weapon_data.get("damage", 100) * 0.8
            total_damage += base_damage
            hits += 1

            # Track weapon performance
            weapon_details.append(f"{weapon_data['name']}: {base_damage:.0f}")

        # Check if all weapons missed
        if hits == 0:
            msg = f"Enemy {self.enemy_name}'s weapons all missed! ({misses} weapons)"
            self.combat_log.append(msg)
            return {"success": True, "message": msg, "hit": False}

        # Apply total damage to player
        damage_report = self.player_vessel.take_damage(total_damage)

        # Generate detailed message
        weapon_count = len(enemy_weapons)
        msg = f"Enemy {self.enemy_name} fired {hits}/{weapon_count} weapons for {total_damage:.0f} total damage!"

        if damage_report["shield_damage"] > 0:
            msg += f"\n  └─ {damage_report['shield_damage']:.0f} to shields"

        if damage_report["hull_damage"] > 0:
            msg += f"\n  └─ {damage_report['hull_damage']:.0f} to hull"

        # Add weapon breakdown
        msg += f"\n  Weapons: {', '.join(weapon_details)}"

        self.combat_log.append(msg)

        # Check if player destroyed
        if damage_report["destroyed"]:
            self.is_active = False
            destroy_msg = f"Your vessel has been destroyed!"
            self.combat_log.append(destroy_msg)

        return {
            "success": True,
            "message": msg,
            "hit": True,
            "damage": total_damage,
            "player_destroyed": damage_report["destroyed"],
            "hits": hits,
            "misses": misses
        }

    def attempt_retreat(self) -> Dict:
        """Player attempts to retreat from combat"""
        # Success chance based on speed difference
        player_speed = self.player_vessel.get_effective_speed()
        enemy_speed = self.enemy_vessel.get_effective_speed()

        speed_ratio = player_speed / max(enemy_speed, 1)
        retreat_chance = min(0.9, 0.4 + (speed_ratio * 0.3))

        if random.random() < retreat_chance:
            self.is_active = False
            msg = "Successfully retreated from combat!"
            self.combat_log.append(msg)
            return {"success": True, "message": msg, "retreated": True}
        else:
            msg = "Retreat failed! Enemy blocked your escape."
            self.combat_log.append(msg)

            # Enemy gets free attack
            enemy_result = self.enemy_attack()

            return {"success": True, "message": msg, "retreated": False,
                   "enemy_attack": enemy_result}

    def repair_hull(self, amount: float) -> Dict:
        """Use repair systems"""
        self.player_vessel.repair(hull_amount=amount)
        msg = f"Repaired {amount:.0f} hull damage"
        self.combat_log.append(msg)
        return {"success": True, "message": msg}

    def next_turn(self):
        """Advance to next combat turn"""
        self.turn_number += 1

        # Shields regenerate slightly each turn
        player_shield_regen = 0
        for module_id in self.player_vessel.installed_modules.get("defense", []):
            module_data = MODULES.get(module_id, {})
            player_shield_regen += module_data.get("recharge_rate", 0)

        if player_shield_regen > 0:
            self.player_vessel.recharge_shields(player_shield_regen)

        # Enemy shields also regen
        enemy_shield_regen = 50  # Basic regen
        self.enemy_vessel.recharge_shields(enemy_shield_regen)

    def get_combat_status(self) -> Dict:
        """Get current combat state"""
        return {
            "turn": self.turn_number,
            "active": self.is_active,
            "player": {
                "hull": f"{self.player_vessel.current_hull_hp:.0f}/{self.player_vessel.max_hull_hp:.0f}",
                "hull_pct": self.player_vessel.get_hull_percentage(),
                "shields": f"{self.player_vessel.current_shields:.0f}/{self.player_vessel.get_total_shield_capacity():.0f}",
                "shield_pct": self.player_vessel.get_shield_percentage()
            },
            "enemy": {
                "name": self.enemy_name,
                "hull": f"{self.enemy_vessel.current_hull_hp:.0f}/{self.enemy_vessel.max_hull_hp:.0f}",
                "hull_pct": self.enemy_vessel.get_hull_percentage(),
                "shields": f"{self.enemy_vessel.current_shields:.0f}/{self.enemy_vessel.get_total_shield_capacity():.0f}",
                "shield_pct": self.enemy_vessel.get_shield_percentage()
            }
        }

    def get_combat_log(self, last_n: int = 5) -> List[str]:
        """Get recent combat log entries"""
        return self.combat_log[-last_n:]


def create_enemy_vessel(difficulty: str = "normal", player_level: int = 1) -> tuple[Vessel, str]:
    """Create an enemy vessel based on difficulty and player level"""
    # Map difficulty to level-based templates
    from data import NPC_ENEMY_TEMPLATES

    # Determine which template to use based on player level
    if player_level <= 5:
        template_key = "level_1_5"
    elif player_level <= 10:
        template_key = "level_6_10"
    elif player_level <= 15:
        template_key = "level_11_15"
    elif player_level <= 20:
        template_key = "level_16_20"
    else:
        template_key = "level_21_plus"

    template = NPC_ENEMY_TEMPLATES[template_key]

    # Choose random enemy name and ship
    enemy_name = random.choice(template["names"])
    vessel_class = random.choice(template["ship_types"])

    enemy_vessel = Vessel(vessel_class)

    # Reduce hull and shields by 20%
    enemy_vessel.max_hull_hp *= 0.8
    enemy_vessel.current_hull_hp *= 0.8

    # Equip weapons
    for weapon_id in template["weapon_setups"]:
        enemy_vessel.install_module(weapon_id)

    # Equip defenses
    for defense_id in template["defense_setups"]:
        enemy_vessel.install_module(defense_id)

    # Reduce current shields by 20% after modules are installed
    enemy_vessel.current_shields *= 0.8

    return enemy_vessel, enemy_name
