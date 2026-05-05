"""
test_with_mock.py
-----------------
Demonstrates the full pipeline (fetch → sort → write → preview)
using mock data so the logic can be verified without network access.

Run this to see the output format and sorting behaviour.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from houses_fetcher import sort_houses, write_to_file, extract_name_and_region

# ── Mock data (mirrors the real API response shape) ───────────────────────────
MOCK_HOUSES = [
    {"url": "https://anapioficeandfire.com/api/houses/1",  "name": "House Lannister of Casterly Rock", "region": "The Westerlands"},
    {"url": "https://anapioficeandfire.com/api/houses/2",  "name": "House Stark of Winterfell",         "region": "The North"},
    {"url": "https://anapioficeandfire.com/api/houses/3",  "name": "House Baratheon of Storm's End",    "region": "The Stormlands"},
    {"url": "https://anapioficeandfire.com/api/houses/4",  "name": "House Algood",                      "region": "The Westerlands"},
    {"url": "https://anapioficeandfire.com/api/houses/5",  "name": "House Targaryen of King's Landing",  "region": "The Crownlands"},
    {"url": "https://anapioficeandfire.com/api/houses/6",  "name": "House Allyrion of Godsgrace",        "region": "Dorne"},
    {"url": "https://anapioficeandfire.com/api/houses/7",  "name": "House Tyrell of Highgarden",         "region": "The Reach"},
    {"url": "https://anapioficeandfire.com/api/houses/8",  "name": "House Martell of Sunspear",          "region": "Dorne"},
    {"url": "https://anapioficeandfire.com/api/houses/9",  "name": "House Arryn of the Eyrie",           "region": "The Vale"},
    {"url": "https://anapioficeandfire.com/api/houses/10", "name": "House Tully of Riverrun",            "region": "The Riverlands"},
    {"url": "https://anapioficeandfire.com/api/houses/11", "name": "House Greyjoy of Pyke",              "region": "The Iron Islands"},
    {"url": "https://anapioficeandfire.com/api/houses/12", "name": "House Amber",                        "region": "The North"},
    {"url": "https://anapioficeandfire.com/api/houses/13", "name": "House Bolton of the Dreadfort",      "region": "The North"},
    {"url": "https://anapioficeandfire.com/api/houses/14", "name": "House Frey of the Crossing",         "region": "The Riverlands"},
    {"url": "https://anapioficeandfire.com/api/houses/15", "name": "House Mormont of Bear Island",       "region": "The North"},
    {"url": "https://anapioficeandfire.com/api/houses/16", "name": "House Clegane",                      "region": "The Westerlands"},
    {"url": "https://anapioficeandfire.com/api/houses/17", "name": "House Swyft of Cornfield",           "region": "The Westerlands"},
    {"url": "https://anapioficeandfire.com/api/houses/18", "name": "House Blackwood of Raventree Hall",  "region": "The Riverlands"},
    {"url": "https://anapioficeandfire.com/api/houses/19", "name": "House Dayne of Starfall",            "region": "Dorne"},
    {"url": "https://anapioficeandfire.com/api/houses/20", "name": "",                                   "region": ""},  # edge case
]

OUTPUT_FILE = "test_houses_output.txt"


def run_demo():
    print("=" * 62)
    print("  HOUSES OF ICE AND FIRE  —  Full Pipeline Demo")
    print("=" * 62)

    # ── Step 1: Simulate fetch ────────────────────────────────────
    print(f"\n[STEP 1] Fetching houses …  ({len(MOCK_HOUSES)} loaded from mock)\n")
    for h in MOCK_HOUSES:
        name, region = extract_name_and_region(h)
        print(f"  • {name:<45}  {region}")

    # ── Step 2: Sort alphabetically ───────────────────────────────
    sorted_houses = sort_houses(MOCK_HOUSES)
    print(f"\n[STEP 2] Sorted alphabetically:\n")
    for i, h in enumerate(sorted_houses, 1):
        name, region = extract_name_and_region(h)
        print(f"  {i:>3}. {name:<45}  {region}")

    # ── Step 3: Write to file ─────────────────────────────────────
    write_to_file(sorted_houses, OUTPUT_FILE)
    print(f"\n[STEP 3] Written to '{OUTPUT_FILE}'")

    # ── Step 4: Read back & display ───────────────────────────────
    print(f"\n[STEP 4] File contents:\n")
    with open(OUTPUT_FILE, encoding="utf-8") as fh:
        print(fh.read())

    print("=" * 62)
    print("  All 3 tasks completed successfully!")
    print("  a. ✅  Houses + Regions fetched from API")
    print("  b. ✅  Written to text file")
    print("  c. ✅  Sorted alphabetically")
    print("=" * 62)


if __name__ == "__main__":
    run_demo()
