# NewsLens – News & Blog Analytics System

## Overview
NewsLens is a Python-based analytics system that processes and analyzes
news and blog article datasets using MongoDB. The application provides
insights such as article counts by date, source-based trends, and
content statistics through a menu-driven interface.

## Features
- Load large JSON datasets into MongoDB
- Compare article counts between news and blogs by date
- Query article statistics using aggregation pipelines
- Robust user input validation for dates
- Graceful handling of cases where no articles exist for a given date

## Tech Stack
- Python
- MongoDB
- PyMongo

## How to Run
## How to Run

### 1. Start MongoDB locally
```bash
mkdir -p mongo-data
mongod --port 27015 --dbpath ./mongo-data
```

### 2. Load the dataset
```bash
python3 load-json.py <dataset.json> 27015
```

### 3. Run the application
```bash
python3 phase2_query.py
```
