# 🌍 African Climate Trend Analysis Week 0 Challenge
**10 Academy KAIM9 | April 2026**

EthioClimate Analytics — supporting Ethiopia's data-driven position for COP32 (Addis Ababa, 2027).

---

## 📌 Project Overview
This project analyzes NASA POWER satellite-derived daily climate data (2015–2026) 
for five African countries: Ethiopia, Kenya, Sudan, Tanzania, and Nigeria.

The goal is to surface key climate trends, seasonal patterns, and anomalies that 
will inform Ethiopia's negotiating position at COP32 — the UN Climate Change 
Conference scheduled for Addis Ababa in 2027.

---

## 📁 Repository StructureS

climate-challenge-week0/
├── .github/
│   └── workflows/
│       └── ci.yml            # GitHub Actions CI pipeline
├── notebooks/
│   ├── ethiopia_eda.ipynb    # Ethiopia EDA
│   ├── kenya_eda.ipynb       # Kenya EDA
│   ├── sudan_eda.ipynb       # Sudan EDA
│   ├── tanzania_eda.ipynb    # Tanzania EDA
│   ├── nigeria_eda.ipynb     # Nigeria EDA
│   └── compare_countries.ipynb # Cross-country comparison
├── app/
│   ├── main.py               # Streamlit dashboard
│   └── utils.py              # Data processing utilities
├── tests/
│   └── test_utils.py         # Unit tests
├── data/                     # ⚠️ Gitignored — add CSVs here
├── .gitignore
├── requirements.txt
└── README.md

---

## ⚙️ Environment Setup

### 1. Clone the repository
git clone https://github.com/Maki4444444/climate-challenge-week0.git
cd climate-challenge-week0

### 2. Create and activate virtual environment

# Create
python -m venv .venv

# Activate — Mac/Linux
source .venv/bin/activate

# Activate — Windows
.venv\Scripts\activate

### 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

### 4. Add data files
Download the NASA POWER CSVs and place them in the data/ folder:

data/
├── ethiopia.csv
├── kenya.csv
├── sudan.csv
├── tanzania.csv
└── nigeria.csv

⚠️ The data/ folder is gitignored. Never commit CSV files.

---

## 📊 How to Run EDA Notebooks

### Option 1 — Jupyter in browser
jupyter notebook notebooks/

Then open any <country>_eda.ipynb file.

### Option 2 — VS Code or Cursor
Open any .ipynb file directly in Cursor or VS Code with the Jupyter extension installed.

### Running all cells
In Jupyter: Kernel → Restart & Run All
In Cursor: Click the ▶▶ Run All button at the top

---

## 🔄 How to Run CI Locally

The CI pipeline installs all dependencies from requirements.txt. To replicate locally:

pip install --upgrade pip
pip install -r requirements.txt
python -m pytest tests/ -v

The GitHub Actions workflow (.github/workflows/ci.yml) runs automatically on every push.

---

## 🚀 How to Run the Streamlit Dashboard

streamlit run app/main.py

Make sure all cleaned CSVs (ethiopia_clean.csv etc.) are in the data/ folder first.

---

## 📦 Dependencies

All dependencies are listed in requirements.txt:

Package     | Version | Purpose
------------|---------|--------
pandas      | 2.2.2   | Data manipulation
numpy       | 1.26.4  | Numerical operations
matplotlib  | 3.8.4   | Static visualizations
seaborn     | 0.13.2  | Statistical charts
scipy       | 1.13.0  | Statistical testing
streamlit   | 1.35.0  | Interactive dashboard
plotly      | 5.22.0  | Interactive charts
openpyxl    | 3.1.2   | Excel support
jupyter     | 1.0.0   | Notebook environment
ipykernel   | 6.29.4  | Jupyter kernel

---

## 🌿 Branch Strategy

Branch              | Purpose
--------------------|--------
main                | Production — all merged work
setup-task          | Task 1 — Git & environment setup
eda-ethiopia        | Task 2 — Ethiopia EDA
eda-kenya           | Task 2 — Kenya EDA
eda-sudan           | Task 2 — Sudan EDA
eda-tanzania        | Task 2 — Tanzania EDA
eda-nigeria         | Task 2 — Nigeria EDA
compare-countries   | Task 3 — Cross-country comparison
dashboard-dev       | Bonus — Streamlit dashboard

---

## 👩‍💻 Author
Meklit Tensae | 10 Academy KAIM9
GitHub: https://github.com/Maki4444444/climate-challenge-week0
