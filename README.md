# Assignment 2 — Ice and Fire API Solutions

## 📌 Overview
This repository contains solutions to three API-based problem statements using Python.  
Each problem demonstrates data fetching, processing, and exporting using real-world APIs.

API Used:  
https://anapioficeandfire.com/

---

## 🧩 Problem Statements

### 🔹 Q1: Houses of Ice and Fire
Tasks:
- Fetch all houses and their regions from API
- Store data in a list
- Write data to a text file
- Sort houses alphabetically

📂 Folder: `Problem_Statement_1`

---

### 🔹 Q2: Books of Ice and Fire
Tasks:
- Fetch list of books from API
- Create dictionary:
  `{book_name: [pages, release_date, ISBN, publisher]}`
- Export data into CSV file

📂 Folder: `Problem_Statement_2`

---

### 🔹 Q3: Characters of Ice and Fire
Tasks:
- Fetch all characters using pagination
- Calculate number of seasons per character (`tvSeries`)
- Sort based on appearances
- Export data into Excel file

📂 Folder: `Problem_Statement_3`

---

## 📂 Repository Structure

Assignment_2/
├── Problem_Statement_1/
├── Problem_Statement_2/
├── Problem_Statement_3/
├── .gitignore
└── README.md

---



## ⚙️ Tech Stack

- Python
- FastAPI (for PS2 & PS3)
- Requests (API handling)
- Pandas (Excel processing)
- CSV module
- OpenPyXL

---

## 🚀 How to Run

### 1. Clone repository

git clone https://github.com/CalMeesam/Assignment_2.git
cd Assignment_2

---

2. (Optional) Create virtual environment
python -m venv venv
.\venv\Scripts\activate

---

## 📊 Outputs

 PS1 → Text file (houses + regions)
 PS2 → CSV file (books data)
 PS3 → Excel file (characters sorted by appearances)
---

### 🧠 Key Concepts Demonstrated
REST API integration
Data transformation & structuring
Pagination handling
File generation (TXT, CSV, Excel)
Backend API development using FastAPI
Clean project structuring

---

👤 Author

Meesam Raza
