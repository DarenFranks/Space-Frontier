#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Diagnose Harvest Fields Belt travel connectivity issue"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from data import LOCATIONS

print("=" * 80)
print("HARVEST FIELDS BELT DIAGNOSTIC")
print("=" * 80)

# Check the location definition
loc_id = "harvest_fields"
if loc_id not in LOCATIONS:
    print(f"\nFATAL: '{loc_id}' not found in LOCATIONS dictionary!")
    sys.exit(1)

harvest_data = LOCATIONS[loc_id]

print(f"\nLocation ID in code: '{loc_id}'")
print(f"Location name: '{harvest_data['name']}'")
print(f"Location type: '{harvest_data['type']}'")
print(f"\nConnections defined:")
connections = harvest_data.get('connections', [])
print(f"Total connections: {len(connections)}")

for conn_id in connections:
    if conn_id in LOCATIONS:
        conn_name = LOCATIONS[conn_id]['name']
        conn_type = LOCATIONS[conn_id]['type']
        print(f"  - {conn_id:25} | {conn_name:30} | Type: {conn_type}")
    else:
        print(f"  - {conn_id:25} | ERROR - NOT FOUND IN LOCATIONS!")

print("\nBidirectional verification:")
bidirectional_issues = []
for conn_id in connections:
    if conn_id in LOCATIONS:
        reverse_conns = LOCATIONS[conn_id].get('connections', [])
        if loc_id in reverse_conns:
            print(f"  OK: {conn_id} connects back to {loc_id}")
        else:
            print(f"  ISSUE: {conn_id} does NOT connect back to {loc_id}!")
            bidirectional_issues.append(conn_id)

print("\n" + "=" * 80)
print("WHAT THE GAME WILL DISPLAY")
print("=" * 80)

if not connections:
    print("\nERROR: No destinations will be shown when at this location!")
    print("The 'Connected Locations' panel will be empty.")
else:
    print(f"\nWhen player arrives at {harvest_data['name']}, they will see {len(connections)} destinations:")
    for i, conn_id in enumerate(connections, 1):
        if conn_id in LOCATIONS:
            conn_name = LOCATIONS[conn_id]['name']
            print(f"  {i}. {conn_name} (ID: {conn_id})")

print("\n" + "=" * 80)
print("HOW TO FIX IF STILL BROKEN")
print("=" * 80)

print("""
If the game still shows no destinations when you arrive at Harvest Fields Belt:

1. CLEAR THE PYTHON CACHE:
   Delete the __pycache__ folder in the game directory
   
2. RESTART THE GAME:
   Close and reopen the game completely
   
3. DELETE SAVE FILES:
   If the issue persists, you may need to delete save_game.yaml
   and start a new game (since old saves might have stale location data)
   
4. VERIFY LOCATION ID:
   Check what location ID your game is actually using.
   It should be exactly: 'harvest_fields' (lowercase, with underscore)
""")

if bidirectional_issues:
    print("\nWARNING: Some connections are not bidirectional:")
    for conn_id in bidirectional_issues:
        print(f"  - {LOCATIONS[conn_id]['name']} ({conn_id})")
    print("\nThese should be fixed in the data file.")
else:
    print("\nGOOD: All connections are bidirectional.")
