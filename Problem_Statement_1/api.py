"""
api.py
------
FastAPI application exposing the Houses of Ice and Fire data via REST endpoints.

Endpoints
---------
GET  /houses            — All houses (sorted alphabetically)
GET  /houses/{index}    — Single house by 1-based sorted index
GET  /houses/search     — Search houses by name or region query param
GET  /regions           — Distinct list of all regions (sorted)
POST /export            — Re-run the fetch+sort+write pipeline on demand
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import Optional
import logging
import os

from houses_fetcher import (
    fetch_all_houses,
    sort_houses,
    write_to_file,
    extract_name_and_region,
    OUTPUT_FILE,
)

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ── App-level state ───────────────────────────────────────────────────────────
# We cache the sorted house list in memory after the first fetch so subsequent
# API calls are instant (no repeated HTTP round-trips to the external API).

class AppState:
    houses: list[dict] = []


state = AppState()


def load_houses() -> None:
    """Fetch, sort, and cache all houses; also persist to the text file."""
    logger.info("Loading houses from Ice and Fire API …")
    raw = fetch_all_houses()
    state.houses = sort_houses(raw)
    write_to_file(state.houses, OUTPUT_FILE)
    logger.info("Loaded and cached %d houses.", len(state.houses))


# ── Lifespan (startup / shutdown) ─────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    load_houses()          # runs once when the server starts
    yield
    logger.info("Shutting down.")


# ── FastAPI app ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="Houses of Ice and Fire API",
    description="Proxy + aggregator for https://anapioficeandfire.com/api/houses",
    version="1.0.0",
    lifespan=lifespan,
)


# ── Pydantic response models ──────────────────────────────────────────────────
class HouseItem(BaseModel):
    index:  int
    name:   str
    region: str
    url:    Optional[str] = None


class HouseListResponse(BaseModel):
    total:  int
    houses: list[HouseItem]


class RegionListResponse(BaseModel):
    total:   int
    regions: list[str]


class ExportResponse(BaseModel):
    message:      str
    total_houses: int
    output_file:  str


# ── Helper ────────────────────────────────────────────────────────────────────
def _to_item(idx: int, house: dict) -> HouseItem:
    name, region = extract_name_and_region(house)
    return HouseItem(
        index=idx,
        name=name,
        region=region,
        url=house.get("url"),
    )


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get(
    "/houses",
    response_model=HouseListResponse,
    summary="List all houses (alphabetically sorted)",
)
def list_houses(
    page:     int = Query(1,  ge=1,  description="Page number (1-based)"),
    per_page: int = Query(50, ge=1, le=200, description="Items per page"),
) -> HouseListResponse:
    """Return all houses sorted alphabetically, with optional pagination."""
    start = (page - 1) * per_page
    end   = start + per_page
    page_data = state.houses[start:end]

    if not page_data and page > 1:
        raise HTTPException(status_code=404, detail="Page out of range.")

    return HouseListResponse(
        total=len(state.houses),
        houses=[_to_item(start + i + 1, h) for i, h in enumerate(page_data)],
    )


@app.get(
    "/houses/search",
    response_model=HouseListResponse,
    summary="Search houses by name or region",
)
def search_houses(
    q: str = Query(..., min_length=1, description="Search term"),
) -> HouseListResponse:
    """Case-insensitive substring search across house name and region."""
    term = q.lower()
    matches = [
        h for h in state.houses
        if term in h.get("name", "").lower()
        or term in h.get("region", "").lower()
    ]
    return HouseListResponse(
        total=len(matches),
        houses=[_to_item(i + 1, h) for i, h in enumerate(matches)],
    )


@app.get(
    "/houses/{index}",
    response_model=HouseItem,
    summary="Get a single house by its sorted index",
)
def get_house(index: int) -> HouseItem:
    """Retrieve one house by its 1-based position in the sorted list."""
    if index < 1 or index > len(state.houses):
        raise HTTPException(
            status_code=404,
            detail=f"Index {index} out of range (1–{len(state.houses)}).",
        )
    return _to_item(index, state.houses[index - 1])


@app.get(
    "/regions",
    response_model=RegionListResponse,
    summary="List all distinct regions",
)
def list_regions() -> RegionListResponse:
    """Return a deduplicated, alphabetically sorted list of all regions."""
    regions = sorted(
        {h.get("region", "").strip() or "Unknown" for h in state.houses}
    )
    return RegionListResponse(total=len(regions), regions=regions)


@app.post(
    "/export",
    response_model=ExportResponse,
    summary="Re-fetch data from source and overwrite the text file",
)
def export_houses() -> ExportResponse:
    """Trigger a fresh fetch from the Ice and Fire API and rewrite the output file."""
    load_houses()
    abs_path = os.path.abspath(OUTPUT_FILE)
    return ExportResponse(
        message=f"Successfully exported {len(state.houses)} houses.",
        total_houses=len(state.houses),
        output_file=abs_path,
    )


@app.get(
    "/export/file",
    response_class=PlainTextResponse,
    summary="Download the text file content directly",
)
def download_file() -> str:
    """Return the raw text file content as plain text."""
    if not os.path.exists(OUTPUT_FILE):
        raise HTTPException(status_code=404, detail="Output file not found. Call POST /export first.")
    with open(OUTPUT_FILE, encoding="utf-8") as fh:
        return fh.read()
