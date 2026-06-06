# 📦 Sales Analytics Dashboard — Superstore Data Analysis

[![Live Dashboard](https://img.shields.io/badge/Live-Dashboard-brightgreen)](https://sales-analytic-dashboard.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![MySQL](https://img.shields.io/badge/MySQL-Railway-orange)](https://railway.app)
[![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-red)](https://streamlit.io)

An end-to-end data analytics project that ingests Superstore orders data, processes it with Python, stores it in a cloud MySQL database, performs SQL analysis, and visualizes insights through both a Power BI dashboard and a live public Streamlit dashboard.

🔗 **Live Dashboard:** [sales-analytic-dashboard.streamlit.app](https://sales-analytic-dashboard.streamlit.app)

---

## 📌 Objective

To analyze Superstore sales data and identify:
- Top performing categories, regions and states
- Monthly sales and profit trends
- Loss-making orders and discount impact
- Regional and segment-level performance

---

## ⚙️ Tech Stack

| Category        | Technologies                        |
| --------------- | ----------------------------------- |
| Programming     | Python                              |
| Database        | MySQL (Railway Cloud)               |
| Data Processing | Pandas, SQLAlchemy                  |
| Analysis        | SQL, Jupyter Notebook               |
| Visualization   | Power BI, Streamlit, Plotly         |
| Deployment      | Streamlit Cloud + Railway           |
| Environment     | Virtual Environment (.venv)         |

---

## 📂 Project Structure

```
sales_analytic_dashboard/
│
├── assets/
│   ├── Dashboard.png
│   ├── sales_by_category.png
│   ├── monthly_trend.png
│   ├── top_subcategories.png
│   └── sales_by_region.png
│
├── app.py                  # Streamlit dashboard
├── main.ipynb              # Full pipeline: ingestion, cleaning, EDA
├── data_analysis.sql       # SQL queries for business analysis
├── filtered_orders.csv     # Cleaned orders dataset (9,994 rows)
├── Dashboard.pbix          # Power BI dashboard
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🔄 Pipeline

```
Kaggle / CSV Data
      ↓
Python (cleaning + EDA + feature engineering)
      ↓
MySQL on Railway (cloud database)
      ↓
SQL Analysis
      ↓
Power BI Dashboard (.pbix)
      +
Streamlit Dashboard (sales-analytic-dashboard.streamlit.app)
```

---

## 📊 Power BI Dashboard

Built a multi-page interactive Power BI dashboard covering:

### Page 1 — Dashboard
- Monthly sales trend (sales, profit, orders)
- Sales and profit by state
- Total sales by category (region breakdown)
- Profit by category and state

### Page 2 — Sales Performance Report
- Sales by category bar chart
- Monthly sales trend
- Category × region breakdown table
- Total sales donut chart + KPI

### Page 3 — Profit Performance Report
- Profit by category
- Monthly profit trend
- Category × region profit table
- Total profit donut chart + margin KPI

### Page 4 — Regional Report
- Sales and profit maps by state
- Total sales vs target gauge
- Orders and quantity KPIs

![Dashboard Preview](assets/Dashboard.png)

---

## 🌐 Streamlit Live Dashboard

Since Power BI requires a Pro license for public sharing, the dashboard was rebuilt using **Streamlit + Plotly** and deployed publicly on Streamlit Cloud — connected to the same cloud MySQL database on Railway.

🔗 **[sales-analytic-dashboard.streamlit.app](https://sales-analytic-dashboard.streamlit.app)**

### Features
- 4 pages matching Power BI layout
- Year and category filters
- KPI cards, bar charts, line charts, donut charts, data tables
- Fully public — no login required

---

## 📈 Key Insights

- **Technology leads with $806K in sales** and 9.47% profit margin — all 3 categories profitable
- **California dominates** with $441K in sales and $40K profit
- **Chairs ($29K) and Phones ($28K)** are top profit sub-categories
- **East Consumer segment** is strongest at $338K sales
- **Q4 peaks** observed consistently each year
- **Loss-making orders** concentrated in Technology and Furniture — likely caused by heavy discounting

---

## 📋 Dataset Summary

| Metric | Value |
|---|---|
| Total Orders | 9,994 |
| Total Sales | $1.10M |
| Total Profit | $205.2K |
| Profit Margin | 9.3% |
| Categories | 3 |
| States | 49 |
| Regions | 4 |

---

## ▶️ How to Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/rajanshaky/sales-analytic-dashboard.git
cd sales-analytic-dashboard
```

### 2. Create & Activate Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file:
```env
MYSQL_HOST=your_host
MYSQL_PORT=3306
MYSQL_USER=your_user
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=your_database
```

### 5. Run the Pipeline
```bash
jupyter notebook main.ipynb
```

### 6. Launch the Dashboard
```bash
streamlit run app.py
```

---

## 🧠 Skills Demonstrated

- Python data processing with Pandas
- ETL pipeline development
- SQL business analysis
- Cloud MySQL management (Railway)
- Power BI dashboard development (4 pages)
- Streamlit + Plotly interactive dashboards
- Cloud deployment (Streamlit Cloud)
- End-to-end analytics workflow

---

## 🔒 Security

- Database credentials stored in `.env` file
- `.env` excluded from version control via `.gitignore`

---

## 👨‍💻 Author

**Rajan Shaky**
Aspiring Data Analyst | Python • SQL • Power BI • Streamlit

[![GitHub](https://img.shields.io/badge/GitHub-rajanshaky-black)](https://github.com/rajanshaky)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://linkedin.com/in/rajanshaky)

---

⭐ If you found this project useful, consider starring the repository!

