#!/usr/bin/env python3
"""
Verify that all locations in Void Dominion are reachable from the starting location.
"""

from data import LOCATIONS
from collections import deque

def verify_all_locations_reachable(start_location="nexus_prime"):
    """
    Verify that all locations can be reached from the starting location.
    Uses breadth-first search to traverse the location graph.
    """
    # Get all location IDs
    all_locations = set(LOCATIONS.keys())
    total_locations = len(all_locations)
    
    print(f"Total locations in game: {total_locations}")
    print(f"Starting location: {start_location}\n")
    
    # Track visited locations
    visited = set()
    queue = deque([start_location])
    visited.add(start_location)
    
    # BFS traversal
    while queue:
        current = queue.popleft()
        
        # Get connections from current location
        connections = LOCATIONS[current].get("connections", [])
        
        for connected_location in connections:
            if connected_location not in visited:
                visited.add(connected_location)
                queue.append(connected_location)
    
    # Check for unreachable locations
    unreachable = all_locations - visited
    
    print(f"Reachable locations: {len(visited)}")
    print(f"Unreachable locations: {len(unreachable)}\n")
    
    if unreachable:
        print("X PROBLEM: The following locations are UNREACHABLE:")
        for loc_id in sorted(unreachable):
            loc_data = LOCATIONS[loc_id]
            print(f"  - {loc_id}: {loc_data['name']} ({loc_data['type']})")
            print(f"    Connections: {loc_data.get('connections', [])}")
        return False
    else:
        print("SUCCESS: All locations are reachable from the starting location!")
        return True

def analyze_connections():
    """
    Analyze the connection structure to identify potential issues.
    """
    print("\n" + "="*60)
    print("CONNECTION ANALYSIS")
    print("="*60 + "\n")
    
    # Find locations with no connections
    no_connections = []
    # Find locations with only one-way connections (not bidirectional)
    one_way_only = []
    
    for loc_id, loc_data in LOCATIONS.items():
        connections = loc_data.get("connections", [])
        
        if not connections:
            no_connections.append(loc_id)
        
        # Check if connections are bidirectional
        for connected_id in connections:
            if connected_id in LOCATIONS:
                reverse_connections = LOCATIONS[connected_id].get("connections", [])
                if loc_id not in reverse_connections:
                    one_way_only.append((loc_id, connected_id))
    
    if no_connections:
        print("WARNING: Locations with NO connections:")
        for loc_id in no_connections:
            print(f"  - {loc_id}: {LOCATIONS[loc_id]['name']}")
        print()
    
    if one_way_only:
        print("INFO: One-way connections (A->B but not B->A):")
        for from_loc, to_loc in one_way_only:
            print(f"  - {from_loc} -> {to_loc}")
            print(f"    ({LOCATIONS[from_loc]['name']} -> {LOCATIONS[to_loc]['name']})")
        print()
    
    # Show faction territories
    print("\n" + "="*60)
    print("LOCATIONS BY FACTION")
    print("="*60 + "\n")
    
    factions = {}
    for loc_id, loc_data in LOCATIONS.items():
        faction = loc_data.get("faction", "None")
        if faction not in factions:
            factions[faction] = []
        factions[faction].append(loc_id)
    
    for faction, locations in sorted(factions.items()):
        print(f"{faction}: {len(locations)} locations")
        for loc_id in sorted(locations):
            print(f"  - {loc_id}: {LOCATIONS[loc_id]['name']}")
        print()

if __name__ == "__main__":
    print("="*60)
    print("SPACE FRONTIER - LOCATION REACHABILITY VERIFICATION")
    print("="*60 + "\n")
    
    success = verify_all_locations_reachable()
    analyze_connections()
    
    print("\n" + "="*60)
    if success:
        print("SUCCESS: VERIFICATION PASSED: All locations are accessible!")
    else:
        print("FAILED: VERIFICATION FAILED: Some locations are unreachable!")
    print("="*60)
