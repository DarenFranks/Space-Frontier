"""
Manufacturing System
Handles crafting modules, ship components, and complete ships from resources
"""

import time
from typing import Dict, List, Optional, Tuple
from data import (
    MODULES, RESOURCES, MANUFACTURING_RECIPES,
    SHIP_COMPONENTS, COMPONENT_RECIPES,
    MODULE_COMPONENTS, MODULE_COMPONENT_RECIPES,
    VESSEL_CLASSES, SHIP_RECIPES
)


class ManufacturingJob:
    """Represents an active manufacturing job"""

    def __init__(self, item_id: str, quantity: int, duration: float, item_type: str = "module"):
        self.item_id = item_id
        self.quantity = quantity
        self.duration = duration
        self.item_type = item_type  # "module", "module_component", "ship_component", or "ship"
        self.start_time = time.time()
        self.completed = 0

    def get_progress(self) -> float:
        """Get progress percentage (0-100)"""
        elapsed = time.time() - self.start_time
        return min(100.0, (elapsed / self.duration) * 100.0)

    def is_complete(self) -> bool:
        """Check if manufacturing is complete"""
        return self.get_progress() >= 100.0

    def get_remaining_time(self) -> float:
        """Get remaining time in seconds"""
        elapsed = time.time() - self.start_time
        remaining = max(0, self.duration - elapsed)
        return remaining

    def to_dict(self) -> Dict:
        """Convert to dictionary for saving"""
        return {
            "item_id": self.item_id,
            "quantity": self.quantity,
            "duration": self.duration,
            "item_type": self.item_type,
            "start_time": self.start_time,
            "completed": self.completed,
            # Backwards compatibility
            "module_id": self.item_id
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'ManufacturingJob':
        """Create from dictionary"""
        # Backwards compatibility - check for old "module_id" key
        item_id = data.get("item_id", data.get("module_id"))
        item_type = data.get("item_type", "module")
        job = cls(item_id, data["quantity"], data["duration"], item_type)
        job.start_time = data["start_time"]
        job.completed = data.get("completed", 0)
        return job


class ManufacturingManager:
    """Manages manufacturing operations"""

    def __init__(self):
        self.active_jobs: List[ManufacturingJob] = []

    def detect_item_type(self, item_id: str) -> Optional[str]:
        """Detect what type of item this is"""
        if item_id in MODULES:
            return "module"
        elif item_id in MODULE_COMPONENTS:
            return "module_component"
        elif item_id in SHIP_COMPONENTS:
            return "ship_component"
        elif item_id in VESSEL_CLASSES:
            return "ship"
        return None

    def get_item_name(self, item_id: str) -> str:
        """Get display name for any item"""
        item_type = self.detect_item_type(item_id)
        if item_type == "module":
            return MODULES[item_id].get("name", item_id)
        elif item_type == "module_component":
            return MODULE_COMPONENTS[item_id].get("name", item_id)
        elif item_type == "ship_component":
            return SHIP_COMPONENTS[item_id].get("name", item_id)
        elif item_type == "ship":
            return VESSEL_CLASSES[item_id].get("name", item_id)
        return item_id

    def can_manufacture(self, item_id: str, location_services: List[str]) -> bool:
        """Check if player can manufacture at current location"""
        return "manufacturing" in location_services

    def get_recipe(self, item_id: str) -> Optional[Dict]:
        """Get manufacturing recipe for any item"""
        # Check module recipes
        if item_id in MANUFACTURING_RECIPES:
            return MANUFACTURING_RECIPES[item_id]
        # Check module component recipes
        elif item_id in MODULE_COMPONENT_RECIPES:
            return MODULE_COMPONENT_RECIPES[item_id]
        # Check ship component recipes
        elif item_id in COMPONENT_RECIPES:
            return COMPONENT_RECIPES[item_id]
        # Check ship recipes
        elif item_id in SHIP_RECIPES:
            return SHIP_RECIPES[item_id]
        return None

    def check_requirements(
        self,
        item_id: str,
        player_inventory: Dict[str, int],
        player_level: int,
        skill_level: int
    ) -> Tuple[bool, str]:
        """
        Check if player meets requirements to manufacture
        Returns: (can_manufacture, message)
        """
        item_type = self.detect_item_type(item_id)
        if not item_type:
            return False, "Invalid item"

        # Get item data based on type
        if item_type == "module":
            item_data = MODULES[item_id]
        elif item_type == "module_component":
            item_data = MODULE_COMPONENTS[item_id]
        elif item_type == "ship_component":
            item_data = SHIP_COMPONENTS[item_id]
        elif item_type == "ship":
            item_data = VESSEL_CLASSES[item_id]
        else:
            return False, "Unknown item type"

        # Check level requirement
        level_req = item_data.get("level_requirement", 1)
        if player_level < level_req:
            return False, f"Requires player level {level_req}"

        # Check if recipe exists
        recipe = self.get_recipe(item_id)
        if not recipe:
            return False, "No manufacturing recipe available"

        # Check skill requirement
        skill_req = recipe.get("skill_requirement", 0)
        if skill_level < skill_req:
            skill_name = "Ship Construction" if item_type == "ship" else "Module Manufacturing"
            return False, f"Requires {skill_name} skill level {skill_req}"

        # Check materials (for modules and components)
        if "materials" in recipe:
            required_materials = recipe["materials"]
            missing_materials = []

            for material_id, quantity in required_materials.items():
                if material_id not in player_inventory or player_inventory[material_id] < quantity:
                    material_name = RESOURCES.get(material_id, {}).get("name", material_id)
                    have = player_inventory.get(material_id, 0)
                    missing_materials.append(f"{material_name}: {have}/{quantity}")

            if missing_materials:
                return False, f"Missing materials: {', '.join(missing_materials)}"

        # Check components (for modules and ships)
        if "components" in recipe:
            required_components = recipe["components"]
            missing_components = []

            for component_id, quantity in required_components.items():
                if component_id not in player_inventory or player_inventory[component_id] < quantity:
                    # Check both MODULE_COMPONENTS and SHIP_COMPONENTS
                    if component_id in MODULE_COMPONENTS:
                        component_name = MODULE_COMPONENTS[component_id].get("name", component_id)
                    elif component_id in SHIP_COMPONENTS:
                        component_name = SHIP_COMPONENTS[component_id].get("name", component_id)
                    else:
                        component_name = component_id
                    have = player_inventory.get(component_id, 0)
                    missing_components.append(f"{component_name}: {have}/{quantity}")

            if missing_components:
                return False, f"Missing components: {', '.join(missing_components)}"

        return True, "Requirements met"

    def calculate_manufacturing_time(
        self,
        item_id: str,
        quantity: int,
        skill_level: int,
        skill_bonus: float
    ) -> float:
        """Calculate time required to manufacture in seconds"""
        recipe = self.get_recipe(item_id)
        if not recipe:
            return 0

        base_time = recipe.get("time", 60)  # Default 60 seconds

        # Skill bonus reduces time
        time_multiplier = 1.0 - (skill_bonus * 0.5)  # Max 50% reduction

        total_time = base_time * quantity * time_multiplier

        return max(10, total_time)  # Minimum 10 seconds

    def start_manufacturing(
        self,
        item_id: str,
        quantity: int,
        player_inventory: Dict[str, int],
        player_level: int,
        skill_level: int,
        skill_bonus: float,
        remove_items_func
    ) -> Tuple[bool, str]:
        """
        Start a manufacturing job
        Returns: (success, message)
        """
        # Detect item type
        item_type = self.detect_item_type(item_id)
        if not item_type:
            return False, "Invalid item"

        # Check requirements
        can_make, msg = self.check_requirements(item_id, player_inventory, player_level, skill_level)
        if not can_make:
            return False, msg

        # Check if already manufacturing
        if len(self.active_jobs) >= 1:  # Limit to 1 job at a time for now
            return False, "Already manufacturing. Complete current job first."

        recipe = self.get_recipe(item_id)

        # Remove materials from inventory (for modules and components)
        if "materials" in recipe:
            for material_id, mat_quantity in recipe["materials"].items():
                total_needed = mat_quantity * quantity
                remove_items_func(material_id, total_needed)

        # Remove components from inventory (for ships)
        if "components" in recipe:
            for component_id, comp_quantity in recipe["components"].items():
                total_needed = comp_quantity * quantity
                remove_items_func(component_id, total_needed)

        # Calculate time
        duration = self.calculate_manufacturing_time(item_id, quantity, skill_level, skill_bonus)

        # Create job
        job = ManufacturingJob(item_id, quantity, duration, item_type)
        self.active_jobs.append(job)

        item_name = self.get_item_name(item_id)
        return True, f"Started manufacturing {quantity}x {item_name} (ETA: {int(duration)}s)"

    def check_completed_jobs(self) -> List[Tuple[str, int, str]]:
        """
        Check for completed jobs and return completed items
        Returns: List of (item_id, quantity, item_type) tuples
        """
        completed = []

        for job in self.active_jobs[:]:
            if job.is_complete():
                completed.append((job.item_id, job.quantity, job.item_type))
                self.active_jobs.remove(job)

        return completed

    def get_active_job(self) -> Optional[ManufacturingJob]:
        """Get current active manufacturing job"""
        if self.active_jobs:
            return self.active_jobs[0]
        return None

    def get_job_progress(self) -> Optional[Dict]:
        """Get progress of active job"""
        job = self.get_active_job()
        if not job:
            return None

        item_name = self.get_item_name(job.item_id)

        return {
            "item_name": item_name,
            "item_id": job.item_id,
            "item_type": job.item_type,
            "quantity": job.quantity,
            "progress": job.get_progress(),
            "remaining_seconds": job.get_remaining_time(),
            # Backwards compatibility
            "module_name": item_name,
            "module_id": job.item_id
        }

    def cancel_job(self) -> Tuple[bool, str]:
        """Cancel active manufacturing job (loses materials)"""
        if not self.active_jobs:
            return False, "No active manufacturing job"

        job = self.active_jobs[0]
        item_name = self.get_item_name(job.item_id)

        self.active_jobs.clear()

        return True, f"Cancelled manufacturing of {job.quantity}x {item_name}"

    def to_dict(self) -> Dict:
        """Convert to dictionary for saving"""
        return {
            "active_jobs": [job.to_dict() for job in self.active_jobs]
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'ManufacturingManager':
        """Create from dictionary"""
        manager = cls()
        manager.active_jobs = [ManufacturingJob.from_dict(job_data)
                              for job_data in data.get("active_jobs", [])]
        return manager
