"""
Text-based User Interface and Command Parser
Handles all user input and output formatting
"""

from typing import Optional
from game_engine import GameEngine
from data import LOCATIONS, RESOURCES, MODULES, SKILLS, FACTIONS, VESSEL_CLASSES, RAW_RESOURCES
from combat import create_enemy_vessel
from vessels import Vessel


class GameUI:
    """Manages text-based user interface"""

    def __init__(self, engine: GameEngine):
        self.engine = engine
        self.running = True

    def print_header(self, text: str):
        """Print formatted header"""
        print(f"\n{'=' * 60}")
        print(f"  {text}")
        print(f"{'=' * 60}\n")

    def print_section(self, text: str):
        """Print section divider"""
        print(f"\n--- {text} ---")

    def format_credits(self, amount: int) -> str:
        """Format credits with commas"""
        return f"{amount:,} CR"

    def show_status(self):
        """Show player and vessel status"""
        if not self.engine.player or not self.engine.vessel:
            print("No active game")
            return

        player = self.engine.player
        vessel = self.engine.vessel

        self.print_header("STATUS")

        print(f"Commander: {player.name}")
        print(f"Credits: {self.format_credits(player.credits)}")
        print(f"Location: {LOCATIONS[player.location]['name']}")

        print(f"\nVessel: {vessel.name}")
        print(f"  Hull: {vessel.current_hull_hp:.0f}/{vessel.max_hull_hp:.0f} ({vessel.get_hull_percentage():.1f}%)")
        print(f"  Shields: {vessel.current_shields:.0f}/{vessel.get_total_shield_capacity():.0f} ({vessel.get_shield_percentage():.1f}%)")
        print(f"  Armor: {vessel.get_total_armor():.0f}")
        print(f"  Speed: {vessel.get_effective_speed():.0f}")
        print(f"  Cargo: {vessel.get_total_cargo_volume():.0f}/{vessel.cargo_capacity:.0f}")

        # Show skill training
        training = player.get_training_progress()
        if training:
            print(f"\nTraining: {training['skill_name']} -> Level {training['target_level']}")
            print(f"  Progress: {training['progress']:.1f}% ({training['remaining_seconds']:.0f}s remaining)")

    def show_inventory(self):
        """Show player inventory"""
        player = self.engine.player

        self.print_header("INVENTORY")

        if not player.inventory:
            print("Inventory is empty")
            return

        print(f"{'Item':<30} {'Quantity':>10} {'Value':>15}")
        print("-" * 60)

        total_value = 0
        for item_id, quantity in sorted(player.inventory.items()):
            if item_id in RESOURCES:
                resource = RESOURCES[item_id]
                value = resource["base_price"] * quantity
                total_value += value
                print(f"{resource['name']:<30} {quantity:>10} {self.format_credits(int(value)):>15}")

        print("-" * 60)
        print(f"{'Total Value:':<30} {' ':>10} {self.format_credits(int(total_value)):>15}")

    def show_skills(self):
        """Show player skills"""
        player = self.engine.player

        self.print_header("SKILLS")

        skills_by_category = {}
        for skill_id, level in player.skills.items():
            skill_data = SKILLS[skill_id]
            category = skill_data["category"]

            if category not in skills_by_category:
                skills_by_category[category] = []

            skills_by_category[category].append((skill_id, skill_data, level))

        for category, skills in sorted(skills_by_category.items()):
            self.print_section(category.upper())

            for skill_id, skill_data, level in skills:
                progress_bar = "█" * level + "░" * (skill_data["max_level"] - level)
                print(f"{skill_data['name']:<25} [{progress_bar}] {level}/{skill_data['max_level']}")

    def show_market(self):
        """Show market at current location"""
        location_data = LOCATIONS[self.engine.player.location]

        if "market" not in location_data.get("services", []) and "black_market" not in location_data.get("services", []):
            print("No market available at this location")
            return

        market = self.engine.economy.get_market(self.engine.player.location)

        if not market:
            print("Market data unavailable")
            return

        self.print_header(f"MARKET - {location_data['name']}")

        listings = market.get_market_listing()

        print(f"{'Resource':<30} {'Buy Price':>12} {'Sell Price':>12} {'Stock':>10}")
        print("-" * 70)

        for listing in listings:
            print(f"{listing['name']:<30} "
                  f"{self.format_credits(listing['buy_price']):>12} "
                  f"{self.format_credits(listing['sell_price']):>12} "
                  f"{listing['stock']:>10}")

    def show_ships_for_sale(self):
        """Show ships for sale at current station"""
        location_data = LOCATIONS[self.engine.player.location]

        if "shipyard" not in location_data.get("services", []):
            print("No shipyard available at this location")
            return

        available_ships = self.engine.ship_market.get_available_ships(
            self.engine.player.location,
            self.engine.player.level,
            self.engine.player.credits
        )

        if not available_ships:
            print("No ships for sale at this station")
            return

        self.print_header(f"SHIPS FOR SALE - {location_data['name']}")
        print(f"Your Credits: {self.format_credits(self.engine.player.credits)} | Level: {self.engine.player.level}")
        print()

        print(f"{'Ship':<35} {'Tier':>4} {'Cost':>15} {'Stock':>6} {'Status':<20}")
        print("-" * 90)

        for ship in available_ships:
            # Determine status
            if ship["can_purchase"]:
                status = "✓ Can Buy"
                status_color = ""
            elif not ship["can_pilot"]:
                status = f"🔒 Req Lv{ship['level_req']}"
                status_color = ""
            elif not ship["can_afford"]:
                status = "💰 Insufficient CR"
                status_color = ""
            else:
                status = "-"
                status_color = ""

            tier_text = f"T{ship['tier_num']}"

            print(f"{ship['name']:<35} "
                  f"{tier_text:>4} "
                  f"{self.format_credits(ship['cost']):>15} "
                  f"{ship['stock']:>6} "
                  f"{status:<20}")

            # Show stats
            stats = ship['stats']
            print(f"  └─ Hull: {stats['hull_hp']} | Shield: {stats['shield_capacity']} | "
                  f"Speed: {stats['base_speed']} | Cargo: {stats['cargo_capacity']}")
            print()

    def show_contracts(self):
        """Show available contracts"""
        self.print_header("AVAILABLE CONTRACTS")

        available = self.engine.contract_board.available_contracts

        if not available:
            print("No contracts available. Travel to a station with contract services.")
            return

        for i, contract in enumerate(available, 1):
            print(f"\n{i}. {contract.name} (Difficulty: {contract.difficulty})")
            print(f"   {contract.description}")
            print(f"   Reward: {self.format_credits(contract.reward)}")
            print(f"   Time Limit: {contract.time_limit // 60} minutes")
            print(f"   Objective: {contract.get_progress_text()}")

    def show_active_contracts(self):
        """Show active contracts"""
        self.print_header("ACTIVE CONTRACTS")

        active = self.engine.contract_board.get_active_contracts()

        if not active:
            print("No active contracts")
            return

        for i, contract in enumerate(active, 1):
            time_remaining = contract.get_time_remaining()
            print(f"\n{i}. {contract.name}")
            print(f"   Progress: {contract.get_progress_text()}")
            print(f"   Reward: {self.format_credits(contract.reward)}")
            print(f"   Time Remaining: {int(time_remaining // 60)}m {int(time_remaining % 60)}s")

    def show_factions(self):
        """Show faction information"""
        self.print_header("FACTIONS")

        summaries = self.engine.faction_manager.get_all_factions_summary(
            self.engine.player.faction_standings
        )

        for faction in summaries:
            print(f"\n{faction['name']} - {faction['status']}")
            print(f"  {faction['description']}")
            print(f"  Territory: {faction['territory_count']} sectors")
            print(f"  Standing: {faction['player_standing']:.2f}")

    def show_vessel_info(self):
        """Show detailed vessel information"""
        vessel = self.engine.vessel

        self.print_header(f"VESSEL - {vessel.name}")

        print(f"Class: {vessel.class_name}")
        print(f"Type: {vessel.class_type}")
        print(f"\nStatus:")
        print(f"  Hull: {vessel.current_hull_hp:.0f}/{vessel.max_hull_hp:.0f} ({vessel.get_hull_percentage():.1f}%)")
        print(f"  Shields: {vessel.current_shields:.0f}/{vessel.get_total_shield_capacity():.0f}")
        print(f"  Armor: {vessel.get_total_armor():.0f}")
        print(f"  Speed: {vessel.get_effective_speed():.0f}")

        print(f"\nModule Slots:")
        for mod_type, slots in vessel.module_slots.items():
            installed = len(vessel.installed_modules[mod_type])
            print(f"  {mod_type.capitalize()}: {installed}/{slots}")

        print(f"\nInstalled Modules:")
        for mod_type, modules in vessel.installed_modules.items():
            if modules:
                print(f"  {mod_type.capitalize()}:")
                for mod_id in modules:
                    print(f"    - {MODULES[mod_id]['name']}")

    def show_map(self):
        """Show location map"""
        self.print_header("GALACTIC MAP")

        current_loc = self.engine.player.location
        current_data = LOCATIONS[current_loc]

        print(f"Current Location: {current_data['name']}")
        print(f"Controlled by: {FACTIONS[current_data['faction']]['name'] if current_data.get('faction') else 'Independent'}")
        print(f"\nConnected Locations:")

        for conn_id in current_data.get("connections", []):
            conn_data = LOCATIONS[conn_id]
            danger = int(conn_data.get("danger_level", 0) * 100)
            print(f"  -> {conn_data['name']} (Danger: {danger}%)")

    def show_help(self):
        """Show help text"""
        self.print_header("COMMANDS")

        commands = {
            "Game": [
                ("status", "Show player and vessel status"),
                ("stats", "Show game statistics"),
                ("save", "Save game"),
                ("quit", "Save and quit game")
            ],
            "Navigation": [
                ("map", "Show connected locations"),
                ("travel <location>", "Travel to location"),
                ("scan", "Scan current area"),
                ("mine", "Mine resources at current location"),
                ("refine", "Refine raw ore into refined resources (interactive)"),
                ("anomaly", "Scan anomalies for research data")
            ],
            "Character": [
                ("inventory", "Show inventory"),
                ("skills", "Show skills"),
                ("train <skill>", "Train a skill")
            ],
            "Trading": [
                ("market", "Show market prices"),
                ("buy <resource> <amount>", "Buy from market"),
                ("sell <resource> <amount>", "Sell to market"),
                ("ships", "Show ships for sale at station")
            ],
            "Contracts": [
                ("contracts", "Show available contracts"),
                ("active", "Show active contracts"),
                ("accept <number>", "Accept a contract"),
                ("abandon <number>", "Abandon active contract"),
                ("deliver", "Deliver cargo for transport contracts")
            ],
            "Combat": [
                ("attack", "Attack enemy in combat"),
                ("retreat", "Attempt to flee combat")
            ],
            "Vessel": [
                ("vessel", "Show vessel details"),
                ("repair", "Repair vessel at station")
            ],
            "Other": [
                ("factions", "Show faction information"),
                ("help", "Show this help text")
            ]
        }

        for category, cmds in commands.items():
            self.print_section(category)
            for cmd, desc in cmds:
                print(f"  {cmd:<30} {desc}")

    def handle_refine_interactive(self, parts):
        """Handle interactive ore refining"""
        # Get all raw ores in player inventory
        raw_ores_available = {}
        for item_id, quantity in self.engine.player.inventory.items():
            if item_id in RAW_RESOURCES:
                raw_ores_available[item_id] = quantity

        if not raw_ores_available:
            print("You don't have any raw ore to refine. Go mining to collect raw ores!")
            return

        # If command was "refine <ore> <amount>" (old format), handle it
        if len(parts) >= 3:
            try:
                ore_name = " ".join(parts[1:-1])
                quantity = int(parts[-1])

                # Find raw ore resource
                ore_id = None
                for res_id, res_data in RAW_RESOURCES.items():
                    if ore_name.lower() in res_data["name"].lower():
                        ore_id = res_id
                        break

                if ore_id:
                    if ore_id in raw_ores_available:
                        success, message = self.engine.refine_ore(ore_id, quantity)
                        print(message)
                    else:
                        print("You don't have that raw ore.")
                else:
                    print("Raw ore not found.")
                return
            except ValueError:
                print("Invalid quantity. Usage: refine <ore> <amount>")
                return

        # Interactive mode - show available ores
        self.print_section("Available Raw Ores")
        ore_list = []
        for i, (ore_id, quantity) in enumerate(sorted(raw_ores_available.items()), 1):
            ore_data = RAW_RESOURCES[ore_id]
            refined_data = RESOURCES[ore_data.get("refines_to")]
            rarity = ore_data.get("rarity", "common")
            from data import REFINING_YIELD_RANGES
            min_yield, max_yield = REFINING_YIELD_RANGES.get(rarity, (0.7, 0.9))

            print(f"  {i}. {ore_data['name']} (x{quantity})")
            print(f"     → {refined_data['name']} | Yield: {int(min_yield*100)}-{int(max_yield*100)}% | Rarity: {rarity.replace('_', ' ').title()}")
            ore_list.append(ore_id)

        # Prompt for selection
        try:
            selection = input("\nSelect ore number to refine (or 'cancel'): ").strip().lower()

            if selection == 'cancel' or selection == 'c':
                print("Refining cancelled.")
                return

            ore_index = int(selection) - 1
            if ore_index < 0 or ore_index >= len(ore_list):
                print("Invalid selection.")
                return

            selected_ore_id = ore_list[ore_index]
            available_qty = raw_ores_available[selected_ore_id]
            ore_data = RAW_RESOURCES[selected_ore_id]

            # Prompt for quantity
            print(f"\nYou have {available_qty}x {ore_data['name']}")
            qty_input = input(f"How much do you want to refine? (1-{available_qty}, or 'all'): ").strip().lower()

            if qty_input == 'cancel' or qty_input == 'c':
                print("Refining cancelled.")
                return

            if qty_input == 'all' or qty_input == 'a':
                refine_qty = available_qty
            else:
                refine_qty = int(qty_input)

            if refine_qty <= 0 or refine_qty > available_qty:
                print(f"Invalid quantity. You can refine 1 to {available_qty}.")
                return

            # Perform refining
            success, message = self.engine.refine_ore(selected_ore_id, refine_qty)
            print(f"\n{message}")

        except ValueError:
            print("Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\nRefining cancelled.")

    def handle_combat_turn(self, command: str):
        """Handle combat commands"""
        if not self.engine.current_combat or not self.engine.current_combat.is_active:
            print("Not in combat")
            return

        combat = self.engine.current_combat

        # Show combat status
        status = combat.get_combat_status()
        print(f"\n--- Turn {status['turn']} ---")
        print(f"Your Vessel:  Hull {status['player']['hull']} | Shields {status['player']['shields']}")
        print(f"Enemy {status['enemy']['name']}:  Hull {status['enemy']['hull']} | Shields {status['enemy']['shields']}")
        print()

        if command == "attack":
            # Player attacks
            skill_bonus = self.engine.player.get_skill_bonus("weapons_mastery", "damage")
            result = combat.player_attack(0, skill_bonus)
            print(result["message"])

            # Enemy counterattacks if alive
            if combat.is_active:
                enemy_result = combat.enemy_attack()
                print(enemy_result["message"])

                # Check if player destroyed
                if enemy_result.get("player_destroyed"):
                    print("\n>>> YOU HAVE BEEN DESTROYED <<<")
                    print("Game Over")
                    self.running = False
                    return

            # If enemy destroyed
            if result.get("enemy_destroyed"):
                print(f"\n>>> VICTORY! <<<")

                # Rewards
                reward = combat.enemy_vessel.max_hull_hp * 10
                self.engine.player.add_credits(reward)
                self.engine.player.stats["enemies_destroyed"] += 1

                print(f"Reward: {self.format_credits(reward)}")

                # Update contracts
                for contract in self.engine.contract_board.active_contracts:
                    if contract.objectives.get("type") == "destroy_enemies":
                        if contract.update_progress({"enemies_destroyed": 1}):
                            print(f"Contract '{contract.name}' completed!")

                self.engine.current_combat = None

            combat.next_turn()

        elif command == "retreat":
            result = combat.attempt_retreat()
            print(result["message"])

            if result.get("retreated"):
                self.engine.current_combat = None
            elif "enemy_attack" in result:
                print(result["enemy_attack"]["message"])

        else:
            print("Invalid combat command. Use 'attack' or 'retreat'")

    def parse_command(self, command: str):
        """Parse and execute user command"""
        parts = command.lower().strip().split()

        if not parts:
            return

        cmd = parts[0]

        # Check if in combat
        if self.engine.current_combat and self.engine.current_combat.is_active:
            if cmd in ["attack", "retreat"]:
                self.handle_combat_turn(cmd)
            else:
                print("You are in combat! Use 'attack' or 'retreat'")
            return

        # General commands
        if cmd == "help":
            self.show_help()

        elif cmd == "status":
            self.show_status()

        elif cmd == "stats":
            stats = self.engine.get_game_stats()
            self.print_header("STATISTICS")
            for key, value in stats.items():
                print(f"{key.replace('_', ' ').title()}: {value}")

        elif cmd == "inventory":
            self.show_inventory()

        elif cmd == "skills":
            self.show_skills()

        elif cmd == "market":
            self.show_market()

        elif cmd == "ships":
            self.show_ships_for_sale()

        elif cmd == "contracts":
            self.show_contracts()

        elif cmd == "active":
            self.show_active_contracts()

        elif cmd == "factions":
            self.show_factions()

        elif cmd == "vessel":
            self.show_vessel_info()

        elif cmd == "map":
            self.show_map()

        elif cmd == "scan":
            success, message = self.engine.scan_area()
            print(message)

        elif cmd == "mine":
            success, message = self.engine.mine_resources()
            print(message)

        elif cmd == "refine":
            self.handle_refine_interactive(parts)

        elif cmd == "repair":
            success, message = self.engine.repair_vessel()
            if success:
                print(f"\n{message}\n")
            else:
                print(f"Error: {message}")

        elif cmd == "anomaly" or cmd == "scan_anomaly":
            success, message = self.engine.scan_anomaly()
            if success:
                print(f"\n{message}\n")
            else:
                print(f"Error: {message}")

        elif cmd == "deliver" or cmd == "deliver_cargo":
            success, message = self.engine.deliver_cargo()
            if success:
                print(f"\n{message}\n")
            else:
                print(f"Error: {message}")

        elif cmd == "travel" and len(parts) >= 2:
            # Find location by name
            location_name = " ".join(parts[1:])
            location_id = None

            for loc_id, loc_data in LOCATIONS.items():
                if location_name.lower() in loc_data["name"].lower():
                    location_id = loc_id
                    break

            if location_id:
                success, message = self.engine.travel_to_location(location_id)
                print(message)
            else:
                print("Location not found")

        elif cmd == "buy" and len(parts) >= 3:
            resource_name = " ".join(parts[1:-1])
            quantity = int(parts[-1])

            # Find resource
            resource_id = None
            for res_id, res_data in RESOURCES.items():
                if resource_name.lower() in res_data["name"].lower():
                    resource_id = res_id
                    break

            if resource_id:
                market = self.engine.economy.get_market(self.engine.player.location)
                if market:
                    trade_bonus = self.engine.player.get_skill_bonus("trade_proficiency", "buy_discount")
                    success, message, cost = market.buy_from_market(
                        resource_id, quantity, self.engine.player.credits, trade_bonus
                    )

                    if success:
                        self.engine.player.spend_credits(cost)
                        self.engine.player.add_item(resource_id, quantity)

                    print(f"{message} - Cost: {self.format_credits(cost)}")
                else:
                    print("No market at this location")
            else:
                print("Resource not found")

        elif cmd == "sell" and len(parts) >= 3:
            resource_name = " ".join(parts[1:-1])
            quantity = int(parts[-1])

            resource_id = None
            for res_id, res_data in RESOURCES.items():
                if resource_name.lower() in res_data["name"].lower():
                    resource_id = res_id
                    break

            if resource_id and self.engine.player.has_item(resource_id, quantity):
                market = self.engine.economy.get_market(self.engine.player.location)
                if market:
                    trade_bonus = self.engine.player.get_skill_bonus("trade_proficiency", "sell_bonus")
                    tax_reduction = self.engine.player.get_skill_bonus("trade_proficiency", "tax_reduction")

                    success, message, payment = market.sell_to_market(
                        resource_id, quantity, trade_bonus, tax_reduction
                    )

                    if success:
                        self.engine.player.remove_item(resource_id, quantity)
                        self.engine.player.add_credits(payment)

                    print(f"{message} - Payment: {self.format_credits(payment)}")
                else:
                    print("No market at this location")
            else:
                print("You don't have that resource")

        elif cmd == "train" and len(parts) >= 2:
            skill_name = " ".join(parts[1:])

            skill_id = None
            for sk_id, sk_data in SKILLS.items():
                if skill_name.lower() in sk_data["name"].lower():
                    skill_id = sk_id
                    break

            if skill_id:
                success, message = self.engine.player.start_skill_training(skill_id)
                print(message)
            else:
                print("Skill not found")

        elif cmd == "accept" and len(parts) >= 2:
            try:
                index = int(parts[1]) - 1
                contracts = self.engine.contract_board.available_contracts

                if 0 <= index < len(contracts):
                    contract = contracts[index]
                    self.engine.contract_board.accept_contract(contract.contract_id)
                    print(f"Accepted contract: {contract.name}")
                else:
                    print("Invalid contract number")
            except ValueError:
                print("Invalid number")

        elif cmd == "save":
            if self.engine.save_current_game():
                print("Game saved successfully")
            else:
                print("Failed to save game")

        elif cmd == "quit":
            self.engine.save_current_game()
            print("Game saved. Goodbye!")
            self.running = False

        else:
            print(f"Unknown command: {command}")
            print("Type 'help' for a list of commands")
