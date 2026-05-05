# 🏰 Houses of Ice and Fire

A Python project that fetches all houses and regions from the
[An API of Ice and Fire](https://anapioficeandfire.com/api/houses),
sorts them alphabetically, writes the result to a text file, and
exposes the data through a clean **FastAPI** REST service.

---

## 📁 Project Structure

```
houses_of_ice_and_fire/
├── houses_fetcher.py          # Core logic: fetch, sort, write
├── api.py                     # FastAPI REST application
├── requirements.txt           # Python dependencies
├── houses_of_ice_and_fire.txt # Auto-generated output file (after run)
└── README.md
```

---

## ⚙️ Tech Stack

| Layer       | Technology            | Purpose                            |
|-------------|----------------------|------------------------------------|
| Language    | Python 3.12+         | Core runtime                       |
| HTTP Client | `requests`           | Paginated fetching from Ice & Fire API |
| API Server  | `FastAPI`            | REST endpoints over the data       |
| ASGI Server | `uvicorn`            | Runs the FastAPI app               |
| Validation  | `pydantic v2`        | Request/response schema models     |

---

## 🚀 Setup & Running

### 1. Clone / navigate to the project folder

```bash
cd houses_of_ice_and_fire
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

### Option A — Run the standalone script (fetch + sort + write file)

```bash
python houses_fetcher.py
```

**What it does:**
1. Fetches all ~440 houses across all API pages
2. Sorts them alphabetically by name
3. Writes `houses_of_ice_and_fire.txt` in the same directory
4. Prints a preview of the first 10 houses to the console

**Sample console output:**
```
════════════════════════════════════════════════════════════
  HOUSES OF ICE AND FIRE  —  444 total
════════════════════════════════════════════════════════════
  #     House Name                               Region
  ──────────────────────────────────────────────────────────
  1     House Algood                             The Westerlands
  2     House Allyrion of Godsgrace              Dorne
  3     House Amber                              The North
  ...
════════════════════════════════════════════════════════════
```

---

### Option B — Run the FastAPI server

```bash
uvicorn api:app --reload
```

Then open: **http://127.0.0.1:8000/docs** for the interactive Swagger UI.

---

## 📡 API Endpoints

| Method | Endpoint            | Description                                        |
|--------|---------------------|----------------------------------------------------|
| GET    | `/houses`           | All houses, sorted alphabetically (paginated)      |
| GET    | `/houses/{index}`   | Single house by 1-based sorted index               |
| GET    | `/houses/search?q=` | Search houses by name or region                    |
| GET    | `/regions`          | All distinct regions (sorted)                      |
| POST   | `/export`           | Re-fetch from source API & overwrite text file     |
| GET    | `/export/file`      | Download the raw text file content                 |

### Example requests

```bash
# All houses (page 1)
curl http://127.0.0.1:8000/houses

# Search for houses in "The North"
curl "http://127.0.0.1:8000/houses/search?q=north"

# Get house #1 in sorted order
curl http://127.0.0.1:8000/houses/1

# All distinct regions
curl http://127.0.0.1:8000/regions

# Re-export text file
curl -X POST http://127.0.0.1:8000/export
```

---

## 📄 Output File Format

`houses_of_ice_and_fire.txt` example:

```
HOUSES OF ICE AND FIRE
Source  : https://anapioficeandfire.com/api/houses
Total   : 444 houses
────────────────────────────────────────────────────────────

   1.  House Algood
        Region : The Westerlands

   2.  House Allyrion of Godsgrace
        Region : Dorne
...
```

---

## 🧠 How It Works

1. **Pagination** — The Ice and Fire API returns max 50 records per page.
   `fetch_all_houses()` loops through pages until the API returns an empty list.
2. **Sorting** — `sort_houses()` uses Python's built-in `sorted()` with a
   case-insensitive key on the `name` field.
3. **Writing** — `write_to_file()` formats and writes a numbered, human-readable
   text file with each house's name and region.
4. **Caching** — The FastAPI app fetches once on startup and keeps the sorted
   list in memory. Use `POST /export` to refresh.
