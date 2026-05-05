from fastapi import FastAPI
from fastapi.responses import FileResponse
import requests
import csv
import os

app = FastAPI()

API_URL = "https://anapioficeandfire.com/api/books"
CSV_FILE = "books.csv"


def fetch_books():
    response = requests.get(API_URL)
    response.raise_for_status()
    return response.json()


def create_books_dict(books_data):
    books_dict = {}

    for book in books_data:
        name = book.get("name")
        pages = book.get("numberOfPages")
        release_date = book.get("released")[:10]
        isbn = book.get("isbn")
        publisher = book.get("publisher")

        books_dict[name] = [pages, release_date, isbn, publisher]

    return books_dict


def write_to_csv(books_dict):
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Book Name", "Pages", "Release Date", "ISBN", "Publisher"])

        for book_name, details in books_dict.items():
            writer.writerow([book_name] + details)


@app.get("/")
def root():
    return {"message": "Books API is running"}


@app.get("/books")
def get_books():
    books_data = fetch_books()
    books_dict = create_books_dict(books_data)
    return books_dict


@app.get("/download-csv")
def download_csv():
    books_data = fetch_books()
    books_dict = create_books_dict(books_data)
    write_to_csv(books_dict)

    return FileResponse(path=CSV_FILE, filename="books.csv", media_type="text/csv")