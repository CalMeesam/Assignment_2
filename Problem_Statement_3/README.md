---

# 📗 Problem_Statement_3/README.md

# Problem Statement 3 — Characters of Ice and Fire API

## 📌 Objective
Build a FastAPI service that:
- Fetches all characters from API (with pagination)
- Calculates number of seasons each character appears in
- Sorts characters by number of appearances
- Exports data into Excel file

API Used:  
https://anapioficeandfire.com/api/characters

---

## ⚙️ Features
- Fetch all characters using pagination
- Extract and process character data
- Calculate number of seasons using `tvSeries`
- Sort characters by appearances (descending)
- Export data to Excel
- Provide API endpoints via FastAPI

---

## 🧠 Approach
1. Fetch characters page by page using `requests`
2. Combine all results into a single dataset
3. Extract relevant fields:
   - Name
   - Gender
   - Culture
   - TV Series appearances
4. Count number of seasons per character
5. Sort characters by season count
6. Export to Excel using `pandas`
7. Expose API endpoints

---
## 📂 Project Structure

Problem_Statement_3/
│── main.py
├── requirements.txt
└── README.md
---

---

## 🚀 How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
---
2. Start server
uvicorn src.main:app --reload
3. Open API docs
http://127.0.0.1:8000/docs
🌐 API Endpoints
🔹 GET /
---

Health check

{ "message": "Characters API running" }
🔹 GET /characters

Returns top characters sorted by number of seasons

🔹 GET /download-excel

Downloads Excel file with sorted data
---

📊 Output Format (Excel)
Name	Gender	Culture	Seasons Appeared

Sorted by:
👉 Seasons Appeared (descending)
---

🛠 Tech Stack
Python
FastAPI
Requests
Pandas
OpenPyXL
