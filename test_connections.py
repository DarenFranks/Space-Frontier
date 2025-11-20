#!/usr/bin/env python3
"""
Test connections for problematic locations
"""

from data import LOCATIONS

problem_locations = [
    "outer_belts",
    "garrison_outpost", 
    "harvest_fields",
    "aurora_reach"
]

print("="*60)
print("TESTING PROBLEMATIC LOCATIONS")
print("="*60 + "\n")

for loc_id in problem_locations:
    if loc_id in LOCATIONS:
        loc_data = LOCATIONS[loc_id]
        connections = loc_data.get("connections", [])
        
        print(f"{loc_id}: {loc_data['name']}")
        print(f"  Type: {loc_data['type']}")
        print(f"  Connections ({len(connections)}): {connections}")
        
        # Verify connections exist and are bidirectional
        for conn_id in connections:
            if conn_id in LOCATIONS:
                reverse_conns = LOCATIONS[conn_id].get("connections", [])
                bidirectional = "YES" if loc_id in reverse_conns else "NO"
                print(f"    -> {conn_id}: {LOCATIONS[conn_id]['name']} [{bidirectional}]")
            else:
                print(f"    -> {conn_id}: MISSING LOCATION!")
        print()
    else:
        print(f"{loc_id}: NOT FOUND IN LOCATIONS!\n")
