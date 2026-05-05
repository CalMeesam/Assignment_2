# Problem Statement 2 — Books of Ice and Fire API

## 📌 Objective
Build a FastAPI service that:
- Fetches book data from the Ice and Fire API
- Transforms it into a structured dictionary
- Exports the data into a CSV file

API Used:  
https://anapioficeandfire.com/api/books

---

## ⚙️ Features
- Fetch books data from external API
- Transform into dictionary:
  `{book_name: [pages, release_date, ISBN, publisher]}`
- Export data to CSV
- REST API endpoints using FastAPI

---

## 🧠 Approach
1. Fetch data using `requests`
2. Extract required fields:
   - Name
   - Number of pages
   - Release date
   - ISBN
   - Publisher
3. Store in dictionary format
4. Write data into CSV using `csv` module
5. Expose endpoints via FastAPI

---

## 🚀 How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
http://127.0.0.1:8000/docs

---

🌐 API Endpoints
🔹 GET /

Health check

{ "message": "Books API is running" }
🔹 GET /books

Returns books data as JSON

🔹 GET /download-csv

Downloads the CSV file

📄 Output Format (CSV)
Book Name	Pages	Release Date	ISBN	Publisher
🛠 Tech Stack
Python
FastAPI
Requests
CSV
