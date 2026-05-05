import requests
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

BASE_URL = "https://anapioficeandfire.com/api/characters"
EXCEL_FILE = "characters.xlsx"


def fetch_all_characters():
    all_characters = []
    page = 1

    while True:
        response = requests.get(f"{BASE_URL}?page={page}&pageSize=50")
        response.raise_for_status()
        data = response.json()

        if not data:
            break

        all_characters.extend(data)
        page += 1

    return all_characters


def process_characters(characters):
    processed_data = []

    for char in characters:
        name = char.get("name") or "Unknown"
        gender = char.get("gender")
        culture = char.get("culture")

        # Count seasons (tvSeries list)
        seasons = [s for s in char.get("tvSeries", []) if s]
        season_count = len(seasons)

        processed_data.append({
            "Name": name,
            "Gender": gender,
            "Culture": culture,
            "Seasons Appeared": season_count
        })

    return processed_data


def create_excel(data):
    df = pd.DataFrame(data)

    # Sort descending by seasons
    df = df.sort_values(by="Seasons Appeared", ascending=False)

    df.to_excel(EXCEL_FILE, index=False)


@app.get("/")
def root():
    return {"message": "Characters API running"}


@app.get("/characters")
def get_characters():
    characters = fetch_all_characters()
    processed = process_characters(characters)

    # Sort before returning
    processed_sorted = sorted(
        processed,
        key=lambda x: x["Seasons Appeared"],
        reverse=True
    )

    return processed_sorted[:20]  # top 20 (avoid huge response)


@app.get("/download-excel")
def download_excel():
    characters = fetch_all_characters()
    processed = process_characters(characters)

    create_excel(processed)

    return FileResponse(
        path=EXCEL_FILE,
        filename="characters.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )