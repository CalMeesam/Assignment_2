"""
houses_fetcher.py
-----------------
Fetches ALL houses and their regions from the Ice and Fire API,
sorts them alphabetically by house name, and writes the result to a text file.

API: https://anapioficeandfire.com/api/houses
"""

import requests
import logging
from typing import Optional

# ── Configuration ────────────────────────────────────────────────────────────
BASE_URL   = "https://anapioficeandfire.com/api/houses"
PAGE_SIZE  = 50          # Maximum allowed by the API
OUTPUT_FILE = "houses_of_ice_and_fire.txt"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ── Core helpers ─────────────────────────────────────────────────────────────

def fetch_page(session: requests.Session, page: int) -> list[dict]:
    """Fetch a single page of houses from the API.

    Args:
        session: A reusable requests.Session for connection pooling.
        page:    1-based page number.

    Returns:
        A list of house dicts (empty list if the page is beyond the last page).

    Raises:
        requests.HTTPError: On any non-2xx response.
    """
    params = {"page": page, "pageSize": PAGE_SIZE}
    response = session.get(BASE_URL, params=params, timeout=15)
    response.raise_for_status()
    return response.json()


def fetch_all_houses(session: Optional[requests.Session] = None) -> list[dict]:
    """Paginate through the entire API and return every house record.

    Args:
        session: Optional external session; a new one is created if omitted.

    Returns:
        A list of all house dicts returned by the API.
    """
    own_session = session is None
    session = session or requests.Session()

    all_houses: list[dict] = []
    page = 1

    try:
        while True:
            logger.info("Fetching page %d …", page)
            houses = fetch_page(session, page)

            if not houses:          # API returns [] on out-of-range pages
                logger.info("No more data — stopping at page %d.", page)
                break

            all_houses.extend(houses)
            logger.info("  → %d houses collected so far.", len(all_houses))
            page += 1

    finally:
        if own_session:
            session.close()

    return all_houses


def extract_name_and_region(house: dict) -> tuple[str, str]:
    """Pull the display name and region from a raw house dict.

    Args:
        house: Raw dict from the API.

    Returns:
        (name, region) — both default to 'Unknown' when the field is absent/empty.
    """
    name   = house.get("name",   "").strip() or "Unknown"
    region = house.get("region", "").strip() or "Unknown"
    return name, region


def sort_houses(houses: list[dict]) -> list[dict]:
    """Return a new list of houses sorted alphabetically by name (case-insensitive).

    Args:
        houses: Unsorted list of house dicts.

    Returns:
        Alphabetically sorted copy.
    """
    return sorted(houses, key=lambda h: h.get("name", "").lower())


# ── File output ───────────────────────────────────────────────────────────────

def write_to_file(houses: list[dict], filepath: str = OUTPUT_FILE) -> None:
    """Write the sorted house list to a human-readable text file.

    Format
    ------
    A header block is followed by one numbered entry per house:

        1.  House Algood
            Region : The Westerlands

    Args:
        houses:   Sorted list of house dicts.
        filepath: Destination file path.
    """
    total = len(houses)
    separator = "─" * 60

    with open(filepath, "w", encoding="utf-8") as fh:
        # ── Header ───────────────────────────────────────────────
        fh.write("HOUSES OF ICE AND FIRE\n")
        fh.write(f"Source  : {BASE_URL}\n")
        fh.write(f"Total   : {total} houses\n")
        fh.write(separator + "\n\n")

        # ── Entries ──────────────────────────────────────────────
        for idx, house in enumerate(houses, start=1):
            name, region = extract_name_and_region(house)
            fh.write(f"{idx:>4}.  {name}\n")
            fh.write(f"        Region : {region}\n")
            fh.write("\n")

        # ── Footer ───────────────────────────────────────────────
        fh.write(separator + "\n")
        fh.write(f"END OF LIST  —  {total} records written.\n")

    logger.info("Output written to '%s'.", filepath)


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    """Orchestrate fetch → sort → write."""
    logger.info("Starting Houses of Ice and Fire data fetch …")

    # Step 1 — Fetch
    houses = fetch_all_houses()
    logger.info("Total houses fetched: %d", len(houses))

    # Step 2 — Sort alphabetically
    sorted_houses = sort_houses(houses)
    logger.info("Houses sorted alphabetically.")

    # Step 3 — Write to file
    write_to_file(sorted_houses, OUTPUT_FILE)

    # Step 4 — Console preview (first 10)
    print("\n" + "═" * 60)
    print(f"  HOUSES OF ICE AND FIRE  —  {len(sorted_houses)} total")
    print("═" * 60)
    print(f"  {'#':<5} {'House Name':<40} {'Region'}")
    print("  " + "─" * 58)
    for i, house in enumerate(sorted_houses[:10], 1):
        name, region = extract_name_and_region(house)
        print(f"  {i:<5} {name:<40} {region}")
    if len(sorted_houses) > 10:
        print(f"  … and {len(sorted_houses) - 10} more (see {OUTPUT_FILE})")
    print("═" * 60 + "\n")


if __name__ == "__main__":
    main()
