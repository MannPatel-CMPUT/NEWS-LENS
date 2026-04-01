# 📰 NewsLens — News & Blog Analytics System

> A Python-based data analytics system that ingests and analyzes large-scale news and blog datasets using **MongoDB** aggregation pipelines — providing article trend insights, source-level statistics, and date-based comparisons through a menu-driven CLI.

---

## 🧭 Table of Contents

- [Overview](#-overview)
- [Tech Stack](#-tech-stack)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Usage](#-usage)
- [Sample Queries](#-sample-queries)
- [Author](#-author)

---

## 📋 Overview

NewsLens processes large JSON datasets containing thousands of news and blog articles, loads them into MongoDB, and provides analytical queries through a command-line interface. It demonstrates real-world data engineering skills including NoSQL data modeling, aggregation pipeline design, and robust input validation.

**What this project demonstrates:**
- Working with **large-scale unstructured JSON data** in MongoDB
- Building **complex aggregation pipelines** ($match, $group, $sort, $project)
- **Data validation** and graceful edge-case handling
- Clean Python CLI application design

---

## 🛠 Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.x |
| Database | MongoDB |
| Driver | PyMongo |
| Data Format | JSON (large-scale datasets) |

---

## ✨ Features

- **JSON Dataset Ingestion** — Load large news/blog JSON files directly into MongoDB
- **Article Count by Date** — Query how many articles were published on a given date
- **News vs. Blog Comparison** — Compare publishing volumes between news and blog sources by date
- **Source-Level Statistics** — Extract per-source article counts and trends
- **Date Validation** — Robust input parsing with graceful error messages for invalid or missing dates
- **Edge-Case Handling** — Graceful behavior when no articles exist for a queried date

---

## 📁 Project Structure

```
NEWS-LENS/
├── load-json.py          # Ingests a JSON dataset file into MongoDB
├── phase2_query.py       # Menu-driven CLI for running analytics queries
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- MongoDB installed and running locally
- PyMongo: `pip install pymongo`

### Setup & Run

```bash
# 1. Clone the repo
git clone https://github.com/MannPatel-CMPUT/NEWS-LENS.git
cd NEWS-LENS

# 2. Install dependencies
pip install pymongo

# 3. Start MongoDB on a custom port
mkdir -p mongo-data
mongod --port 27015 --dbpath ./mongo-data

# 4. Load your dataset (in a new terminal)
python3 load-json.py <path-to-dataset.json> 27015

# 5. Run the analytics CLI
python3 phase2_query.py
```

---

## 💻 Usage

After running `phase2_query.py`, you'll be presented with a menu to select analytics queries. Enter the corresponding number and follow the prompts (e.g., enter a date in `YYYY-MM-DD` format).

Example interaction:
```
=== NewsLens Analytics ===
1. Article count by date
2. Compare news vs blog articles by date
3. Source statistics
4. Exit

Select option: 1
Enter date (YYYY-MM-DD): 2023-06-15

Results:
  News articles: 142
  Blog articles: 38
  Total: 180
```

---

## 🔍 Sample Aggregation Pipeline

```python
# Count articles by source, sorted by volume
pipeline = [
    { "$match": { "type": "news" } },
    { "$group": { "_id": "$source", "count": { "$sum": 1 } } },
    { "$sort": { "count": -1 } }
]
results = collection.aggregate(pipeline)
```


---

## 👤 Author

**Mann Patel**
BSc Computing Science — University of Alberta
[LinkedIn](https://www.linkedin.com/in/mann-patel-08359a3a3/) · [GitHub](https://github.com/MannPatel-CMPUT) · mannjpatel234@gmail.com
