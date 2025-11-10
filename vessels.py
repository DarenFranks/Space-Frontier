"""
Vessel (Ship) System
Handles ship stats, modules, damage, and upgrades
"""

from typing import Dict, List, Optional
from data import VESSEL_CLASSES, MODULES
import copy


class Vessel:
    """Represents a player's vessel (ship)"""

    def __init__(self, vessel_class_id: str, custom_name: Optional[str] = None):
        if vessel_class_id not in VESSEL_CLASSES:
            raise ValueError(f"Invalid vessel class: {vessel_class_id}")

        self.vessel_class_id = vessel_class_id
        vessel_data = VESSEL_CLASSES[vessel_class_id]

        # Basic info
        self.name = custom_name or vessel_data["name"]
        self.class_name = vessel_data["name"]
        self.description = vessel_data["description"]
        self.class_type = vessel_data["class_type"]
        self.tier_num = vessel_data.get("tier_num", 1)  # Ship tier (MK1=1, MK2=2, etc.)

        # Stats
        self.max_hull_hp = vessel_data["hull_hp"]
        self.current_hull_hp = self.max_hull_hp
        self.max_shield_capacity = vessel_data["shield_capacity"]
        self.current_shields = self.max_shield_capacity
        self.armor_rating = vessel_data["armor_rating"]
        self.cargo_capacity = vessel_data["cargo_capacity"]
        self.base_speed = vessel_data["base_speed"]

        # Module system
        self.module_slots = copy.deepcopy(vessel_data["module_slots"])
        self.installed_modules: Dict[str, List[str]] = {
            "weapon": [],
            "defense": [],
            "utility": [],
            "engine": []
        }

    def install_module(self, module_id: str, replace_module_id: Optional[str] = None) -> tuple[bool, str, Optional[str]]:
        """
        Install a module in available slot
        Returns: (success, message, replaced_module_id)
        """
        if module_id not in MODULES:
            return False, "Invalid module", None

        module_data = MODULES[module_id]
        module_type = module_data["type"]

        # Check ship tier restrictions
        ship_tier_min = module_data.get("ship_tier_min", 1)
        ship_tier_max = module_data.get("ship_tier_max", 99)

        if self.tier_num < ship_tier_min:
            return False, f"{module_data['name']} requires a Tier {ship_tier_min}+ ship (your ship is Tier {self.tier_num})", None

        if self.tier_num > ship_tier_max:
            return False, f"{module_data['name']} can only be installed on Tier {ship_tier_max} or lower ships (your ship is Tier {self.tier_num})", None

        # Check if slot available
        current_count = len(self.installed_modules[module_type])
        max_slots = self.module_slots[module_type]

        replaced_module = None

        if current_count >= max_slots:
            # Slots are full, need to replace
            if replace_module_id is None:
                return False, f"No available {module_type} slots", None

            # Verify the module to replace exists and is correct type
            if replace_module_id not in self.installed_modules[module_type]:
                return False, f"Module to replace not found in {module_type} slots", None

            # Replace the module
            self.installed_modules[module_type].remove(replace_module_id)
            replaced_module = replace_module_id

        self.installed_modules[module_type].append(module_id)

        if replaced_module:
            replaced_name = MODULES[replaced_module]["name"]
            return True, f"Installed {module_data['name']}, replaced {replaced_name}", replaced_module
        else:
            return True, f"Installed {module_data['name']}", None

    def uninstall_module(self, module_id: str, module_type: str) -> tuple[bool, str]:
        """Uninstall a module"""
        if module_id in self.installed_modules[module_type]:
            self.installed_modules[module_type].remove(module_id)
            return True, f"Uninstalled module"
        return False, "Module not found"

    def get_total_weapon_damage(self) -> float:
        """Calculate total weapon damage"""
        total_damage = 0
        for module_id in self.installed_modules["weapon"]:
            module_data = MODULES[module_id]
            total_damage += module_data.get("damage", 0)
        return total_damage

    def get_total_shield_capacity(self) -> float:
        """Calculate total shield capacity with bonuses"""
        total = self.max_shield_capacity
        for module_id in self.installed_modules["defense"]:
            module_data = MODULES[module_id]
            total += module_data.get("shield_boost", 0)
        return total

    def get_total_armor(self) -> float:
        """Calculate total armor rating"""
        total = self.armor_rating
        for module_id in self.installed_modules["defense"]:
            module_data = MODULES[module_id]
            total += module_data.get("armor_boost", 0)
        return total

    def get_evasion_chance(self) -> float:
        """Calculate evasion chance"""
        evasion = 0.1  # Base 10%
        for module_id in self.installed_modules["defense"]:
            module_data = MODULES[module_id]
            evasion += module_data.get("evasion_boost", 0)
        return min(evasion, 0.75)  # Cap at 75%

    def get_effective_speed(self) -> float:
        """Calculate effective speed with modules"""
        speed = self.base_speed
        speed_multiplier = 1.0

        # Engine modules
        for module_id in self.installed_modules["engine"]:
            module_data = MODULES[module_id]
            speed_multiplier += module_data.get("speed_boost", 0)

        # Utility modules
        for module_id in self.installed_modules["utility"]:
            module_data = MODULES[module_id]
            speed_multiplier += module_data.get("speed_boost", 0)

        return speed * speed_multiplier

    def get_mining_efficiency(self) -> float:
        """Calculate mining yield multiplier"""
        efficiency = 1.0
        for module_id in self.installed_modules["utility"]:
            module_data = MODULES[module_id]
            if "mining_yield" in module_data:
                efficiency *= module_data["mining_yield"]
        return efficiency

    def get_mining_tier(self) -> int:
        """Get the highest mining tier available from installed modules"""
        max_tier = 0
        for module_id in self.installed_modules["utility"]:
            module_data = MODULES[module_id]
            if "mining_tier" in module_data:
                max_tier = max(max_tier, module_data["mining_tier"])
        return max_tier

    def get_scan_range(self) -> float:
        """Calculate sensor scan range"""
        scan_range = 500  # Base range
        for module_id in self.installed_modules["utility"]:
            module_data = MODULES[module_id]
            scan_range += module_data.get("scan_range", 0)
        return scan_range

    def take_damage(self, damage: float, damage_type: str = "normal") -> Dict:
        """Apply damage to vessel. Returns damage report."""
        original_damage = damage

        # Shields absorb damage first
        if self.current_shields > 0:
            shield_damage = min(damage, self.current_shields)
            self.current_shields -= shield_damage
            damage -= shield_damage
        else:
            shield_damage = 0

        # Remaining damage goes to hull, reduced by armor
        armor_reduction = 1.0 - (self.get_total_armor() / (self.get_total_armor() + 1000))
        hull_damage = damage * armor_reduction

        self.current_hull_hp -= hull_damage
        self.current_hull_hp = max(0, self.current_hull_hp)

        return {
            "total_damage": original_damage,
            "shield_damage": shield_damage,
            "hull_damage": hull_damage,
            "shields_remaining": self.current_shields,
            "hull_remaining": self.current_hull_hp,
            "destroyed": self.is_destroyed()
        }

    def repair(self, hull_amount: float = 0, shield_amount: float = 0):
        """Repair hull and recharge shields"""
        self.current_hull_hp = min(self.max_hull_hp, self.current_hull_hp + hull_amount)
        self.current_shields = min(self.get_total_shield_capacity(),
                                   self.current_shields + shield_amount)

    def recharge_shields(self, amount: float):
        """Recharge shields"""
        max_shields = self.get_total_shield_capacity()
        self.current_shields = min(max_shields, self.current_shields + amount)

    def is_destroyed(self) -> bool:
        """Check if vessel is destroyed"""
        return self.current_hull_hp <= 0

    def get_hull_percentage(self) -> float:
        """Get hull integrity as percentage"""
        return (self.current_hull_hp / self.max_hull_hp) * 100

    def get_shield_percentage(self) -> float:
        """Get shield strength as percentage"""
        max_shields = self.get_total_shield_capacity()
        if max_shields == 0:
            return 0
        return (self.current_shields / max_shields) * 100

    def get_total_cargo_volume(self) -> float:
        """Calculate used cargo volume"""
        # This would be calculated from actual cargo in a full implementation
        return 0

    def get_available_cargo(self) -> float:
        """Get available cargo space"""
        return self.cargo_capacity - self.get_total_cargo_volume()

    def get_status_report(self) -> Dict:
        """Get comprehensive vessel status"""
        return {
            "name": self.name,
            "class": self.class_name,
            "hull_hp": f"{self.current_hull_hp:.0f}/{self.max_hull_hp:.0f} ({self.get_hull_percentage():.1f}%)",
            "shields": f"{self.current_shields:.0f}/{self.get_total_shield_capacity():.0f} ({self.get_shield_percentage():.1f}%)",
            "armor": f"{self.get_total_armor():.0f}",
            "speed": f"{self.get_effective_speed():.0f}",
            "cargo": f"{self.get_total_cargo_volume():.0f}/{self.cargo_capacity:.0f}",
            "weapon_damage": f"{self.get_total_weapon_damage():.0f}",
            "modules": {
                "weapon": f"{len(self.installed_modules['weapon'])}/{self.module_slots['weapon']}",
                "defense": f"{len(self.installed_modules['defense'])}/{self.module_slots['defense']}",
                "utility": f"{len(self.installed_modules['utility'])}/{self.module_slots['utility']}",
                "engine": f"{len(self.installed_modules['engine'])}/{self.module_slots['engine']}"
            }
        }

    def to_dict(self) -> Dict:
        """Convert vessel to dictionary for saving"""
        return {
            "vessel_class_id": self.vessel_class_id,
            "custom_name": self.name if self.name != self.class_name else None,
            "current_hull_hp": self.current_hull_hp,
            "current_shields": self.current_shields,
            "installed_modules": self.installed_modules
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Vessel':
        """Create vessel from dictionary"""
        vessel = cls(data["vessel_class_id"], data.get("custom_name"))
        vessel.current_hull_hp = data["current_hull_hp"]
        vessel.current_shields = data["current_shields"]
        vessel.installed_modules = data["installed_modules"]
        return vessel
