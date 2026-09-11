# 🚀 Supply Chain Production Analytics

An end-to-end, production-grade data engineering and analytics platform for supply chain management. This system transforms raw ERP data into actionable intelligence, featuring automated ETL pipelines, machine learning demand forecasting, inventory optimization algorithms, and a real-time automated warehouse simulation dashboard.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-FF4B4B.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791.svg)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**🔗 Live Demo:** [supply-chain-appuction-analytics-huanper2uchf36nkfvcuug.streamlit.app](https://supply-chain-appuction-analytics-huanper2uchf36nkfvcuug.streamlit.app/)

---

## 📋 Table of Contents
1. [Overview](#overview)
2. [Key Features](#key-features)
3. [System Architecture](#system-architecture)
4. [Tech Stack](#tech-stack)
5. [Project Structure](#project-structure)
6. [Getting Started](#getting-started)
7. [Usage & Interacting with the System](#usage--interacting-with-the-system)
8. [API Endpoints](#api-endpoints)
9. [Testing](#testing)
10. [Contributing](#contributing)
11. [License](#license)

---

## 📖 Overview
Modern supply chains require real-time visibility and predictive capabilities to reduce costs and prevent stockouts. This project provides a complete data pipeline that ingests raw procurement, sales, and production data, processes it, and serves it through a RESTful API and an interactive dashboard.

It includes mathematical models for Economic Order Quantity (EOQ), Reorder Points (ROP), and dynamic Safety Stock calculations, alongside a machine learning model for time-series demand forecasting.

---

## ✨ Key Features
- **Automated ETL Pipeline:** Ingests raw CSV data, cleans/validates it using Pandas, and loads it into a PostgreSQL data warehouse.
- **Big Data Warehouse Simulation:** Generates and manages a dynamic dataset of 10,000 SKUs.
- **Live Automated Simulation:** A real-time toggle that simulates live inbound (supplier deliveries) and outbound (customer orders) warehouse movements.
- **Inventory Optimization:** Built-in algorithms for EOQ, ROP, and Safety Stock based on service levels (Z-scores).
- **Demand Forecasting:** Scikit-Learn machine learning pipeline utilizing time-series feature engineering (lags, rolling averages) to predict future product demand.
- **Production Analytics:** Overall Equipment Effectiveness (OEE) calculations and Material Requirements Planning (MRP).
- **RESTful API:** A FastAPI backend exposing all analytical models as endpoints.
- **Interactive Dashboard:** A Streamlit frontend for visualizing KPIs, managing stock, and running optimization calculators.

---

## 🏗 System Architecture
```text
[ Raw CSVs ] --> ( ETL Pipeline / Pandas ) --> [ PostgreSQL DB ]
                                                   |
                                     +-------------+-------------+
                                     |                           |
                              [ FastAPI Backend ]        [ Streamlit Dashboard ]
                              ( Math & ML Models )        ( Live Simulation )
                                     |                           |
                                     +-------------+-------------+
                                                   |
                                           [ PowerBI / External BI ]
```

---

## 🛠 Tech Stack
- **Backend / API:** FastAPI, Uvicorn
- **Frontend / Dashboard:** Streamlit
- **Database:** PostgreSQL 15 (Dockerized)
- **Data Processing:** Pandas, NumPy
- **Machine Learning:** Scikit-Learn, Statsmodels
- **Testing:** Pytest
- **Containerization:** Docker, Docker Compose

---

## 📁 Project Structure
```text
supply-chain-production-analytics/
├── api/                    # FastAPI backend and Pydantic schemas
├── dashboard/              # Streamlit frontend application
├── data/                   # Raw, processed, and sample datasets
├── database/               # SQL schemas, tables, views, and seeds
├── docs/                   # Architecture and methodology docs
├── etl/                    # Extract, Transform, Load pipeline scripts
├── forecasting/            # ML models for demand prediction
├── inventory/              # EOQ, ROP, Safety Stock algorithms
├── notebooks/              # Jupyter notebooks for ad-hoc analysis
├── powerbi/                # PowerBI DAX formulas and data models
├── production/             # OEE, MRP, and capacity analysis
├── procurement/            # Supplier scorecards and risk assessment
├── tests/                  # Pytest automated test suite
├── docker-compose.yml      # Container orchestration
└── requirements.txt        # Python dependencies
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Docker & Docker Compose
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/supply-chain-production-analytics.git
cd supply-chain-production-analytics
```

### 2. Set up the Environment
Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Start the Database (Optional but recommended)
Start the PostgreSQL database via Docker:
```bash
docker-compose up -d db
```
*Note: The Streamlit app runs on local CSVs by default, but the FastAPI backend and ETL pipeline are configured to connect to PostgreSQL.*

### 4. Run the ETL Pipeline
Ensure you have raw CSV files in `data/raw/`, then run:
```bash
python etl/pipeline.py
```

---

## 💻 Usage & Interacting with the System

You need to run two separate terminals to power the full application.

**Terminal 1: Start the FastAPI Backend**
```bash
uvicorn api.main:app --reload --port 8000
```
- API Documentation (Swagger UI): `http://localhost:8000/docs`

**Terminal 2: Start the Streamlit Dashboard**
```bash
streamlit run dashboard/streamlit_app.py
```
- Dashboard URL: `http://localhost:8501`

### Using the Live Warehouse Simulation:
1. Open the Streamlit app in your browser.
2. Select **"Live Warehouse Simulation"** from the sidebar menu.
3. Toggle **"Start Automated Simulation"** to watch the 10,000 SKUs automatically process inbound/outbound movements, recalculate KPIs, and update charts in real-time.

---

## 🌐 API Endpoints
The FastAPI backend exposes the following endpoints:

| Method | Endpoint                        | Description                                  |
|--------|---------------------------------|----------------------------------------------|
| `GET`  | `/health`                       | API health check                             |
| `POST`| `/api/inventory/eoq`            | Calculate Economic Order Quantity            |
| `POST`| `/api/inventory/reorder-point`  | Calculate Reorder Point (ROP)                |
| `POST`| `/api/production/oee`           | Calculate Overall Equipment Effectiveness    |
| `POST`| `/api/procurement/supplier-scorecard` | Evaluate supplier performance & tiering |

---

## 🧪 Testing
The core supply chain math (EOQ, ROP, OEE, Supplier Scoring) is fully unit-tested. To run the test suite:

```bash
pytest tests/ -v
```

---

## 🤝 Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/AmazingFeature`.
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`.
4. Push to the branch: `git push origin feature/AmazingFeature`.
5. Open a Pull Request.

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
