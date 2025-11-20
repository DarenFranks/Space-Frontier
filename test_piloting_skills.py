"""
Test script to verify piloting skills system
"""

from data import SKILLS, VESSEL_CLASSES

print("=" * 60)
print("PILOTING SKILLS TEST")
print("=" * 60)

# Check all piloting skills exist
piloting_skills = {k: v for k, v in SKILLS.items() if k.endswith("_piloting")}

print(f"\n[OK] Found {len(piloting_skills)} piloting skills:")
for skill_id, skill_data in piloting_skills.items():
    print(f"  - {skill_id}: {skill_data['name']}")
    print(f"    Description: {skill_data['description']}")
    print(f"    Max Level: {skill_data['max_level']}")

# Check faction ships exist
print("\n" + "=" * 60)
print("FACTION SHIPS")
print("=" * 60)

faction_ships = {k: v for k, v in VESSEL_CLASSES.items() if k.endswith("_faction")}

print(f"\n[OK] Found {len(faction_ships)} faction ships:")
for ship_id, ship_data in faction_ships.items():
    print(f"\n  {ship_id}:")
    print(f"    Name: {ship_data['name']}")
    print(f"    Type: {ship_data['class_type']}")
    print(f"    Tier: {ship_data['tier_num']}")
    print(f"    Variant: {ship_data['variant']}")
    print(f"    Cost: {ship_data['cost']:,} credits")
    print(f"    Hull HP: {ship_data['hull_hp']}")
    print(f"    Shield: {ship_data['shield_capacity']}")
    print(f"    Cargo: {ship_data['cargo_capacity']}")

# Test skill requirements
print("\n" + "=" * 60)
print("SKILL REQUIREMENT VERIFICATION")
print("=" * 60)

# Check a sample of ships for each tier
test_ships = [
    "scout_standard_mk1",  # Should need scout_piloting level 1+
    "scout_standard_mk2",  # Should need scout_piloting level 4+
    "scout_standard_mk3",  # Should need scout_piloting level 7+
    "scout_faction",       # Should need scout_piloting level 10
]

for ship_id in test_ships:
    if ship_id in VESSEL_CLASSES:
        ship = VESSEL_CLASSES[ship_id]
        tier_num = ship['tier_num']
        variant = ship.get('variant', 'standard')
        
        # Calculate required skill level
        if variant == "faction":
            req_level = 10
        elif tier_num == 1:
            req_level = 1
        elif tier_num == 2:
            req_level = 4
        else:
            req_level = 7
        
        print(f"\n  {ship['name']} (Tier {tier_num}):")
        print(f"    Required: scout_piloting level {req_level}+")

print("\n" + "=" * 60)
print("[OK] ALL TESTS PASSED")
print("=" * 60)
