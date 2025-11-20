#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test script to diagnose location connection issues"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from data import LOCATIONS

problem_locations = {
    "outer_belts": "Outer Belt Clusters",
    "garrison_outpost": "Garrison Outpost", 
    "harvest_fields": "Harvest Fields Belt",
    "aurora_reach": "Aurora Reach Station"
}

print("=" * 80)
print("CHECKING PROBLEM LOCATIONS")
print("=" * 80)

for loc_id, display_name in problem_locations.items():
    print(f"\n[{loc_id}] {display_name}")
    print("-" * 80)
    
    if loc_id not in LOCATIONS:
        print(f"  ERROR: LOCATION NOT FOUND IN LOCATIONS DICT!")
        continue
    
    loc_data = LOCATIONS[loc_id]
    connections = loc_data.get('connections', [])
    
    print(f"  Connections count: {len(connections)}")
    
    if not connections:
        print(f"  ERROR: NO CONNECTIONS DEFINED!")
    else:
        print(f"  Outgoing connections:")
        for conn_id in connections:
            if conn_id in LOCATIONS:
                conn_name = LOCATIONS[conn_id]['name']
                print(f"    OK - {conn_id}: {conn_name}")
            else:
                print(f"    ERROR - {conn_id}: LOCATION NOT FOUND!")
        
        print(f"\n  Bidirectional check (do these connect back?):")
        for conn_id in connections:
            if conn_id in LOCATIONS:
                reverse_conns = LOCATIONS[conn_id].get('connections', [])
                has_reverse = loc_id in reverse_conns
                status = "OK" if has_reverse else "MISSING"
                print(f"    [{status}] {conn_id} connects back: {has_reverse}")

print("\n" + "=" * 80)
print("SUMMARY OF CONNECTION ISSUES")
print("=" * 80)

for loc_id, display_name in problem_locations.items():
    if loc_id not in LOCATIONS:
        print(f"\n[ERROR] {display_name}: LOCATION DEFINITION MISSING")
        continue
    
    connections = LOCATIONS[loc_id].get('connections', [])
    
    if not connections:
        print(f"\n[ERROR] {display_name}: NO OUTGOING CONNECTIONS")
    else:
        missing_reverse = []
        for conn_id in connections:
            if conn_id in LOCATIONS:
                reverse_conns = LOCATIONS[conn_id].get('connections', [])
                if loc_id not in reverse_conns:
                    missing_reverse.append(conn_id)
        
        if missing_reverse:
            print(f"\n[INCOMPLETE] {display_name}: Missing reverse connections from:")
            for conn_id in missing_reverse:
                print(f"    - {LOCATIONS[conn_id]['name']} ({conn_id})")
        else:
            print(f"\n[OK] {display_name}: All connections are bidirectional")
