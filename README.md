⸻

🚀 AI-Driven FMCG Decision Intelligence Platform

Enterprise Analytics • Executive AI • Boardroom-Ready

⸻

📌 Overview

This project is a production-grade, AI-assisted FMCG analytics platform developed during an internship at D’s Group.
It transforms raw FMCG operational data into executive-level insights, risks, and decision-ready intelligence using a secure, explainable, and API-free architecture.

The platform is deployed on Streamlit Cloud and designed to support:
	•	Leadership reviews
	•	Sales & operations monitoring
	•	Data-driven strategic decisions

⸻

🎯 Key Objectives
	•	Provide single source of truth for FMCG analytics
	•	Enable executive-friendly insights without technical complexity
	•	Deliver enterprise-safe AI reasoning (no hallucinations, no external APIs)
	•	Support real-time analysis across sales, outlets, SKUs, teams, and operations

⸻

🧠 Core Capabilities

✅ Executive KPI dashboards
✅ Advanced sales & daily trend analysis
✅ Product, SKU & brand intelligence
✅ Outlet & territory performance analysis
✅ Field force productivity tracking
✅ Order operations & rejection analysis
✅ Forecasting (trend-based, explainable)
✅ Data quality & integrity monitoring
✅ Snowflake SQL Studio (read-only, secure)
✅ AI Executive Chat (rule-based, deterministic)

⸻

🏗️ Architecture Overview

User (Browser)
   │
   ▼
Streamlit UI (app.py)
   │
   ├── Pages (16 analytics modules)
   │
   ├── Core Engines
   │     ├─ Intent Engine
   │     ├─ Metric Engine
   │     ├─ Response Formatter
   │
   ├── Utils Layer
   │     ├─ Data Processing
   │     ├─ KPI Calculations
   │     ├─ Risk Scoring
   │     ├─ Business Signals
   │
   └── Data Layer
         ├─ Upload (CSV / Excel)
         └─ Snowflake (Read-only)

✔ Fully deterministic
✔ Auditable logic
✔ Enterprise-safe

⸻

📂 Project Structure

.
├── app.py
├── config.py
├── requirements.txt
├── assets/
│   ├── ds_group_favicon.png
│   └── style.css
├── core/
│   ├── data_registry.py
│   ├── intent_engine.py
│   ├── metric_engine.py
│   └── response_formatter.py
├── pages/
│   ├── 0_Upload_Dataset.py
│   ├── 1_Executive_Overview.py
│   ├── 2_Sales_Performance.py
│   ├── 3_Product_SKU_Brand.py
│   ├── 4_Outlet_Distribution.py
│   ├── 5_Field_Force_Productivity.py
│   ├── 6_Order_Operations.py
│   ├── 7_Sales_Forecasting.py
│   ├── 8_Outlet_Segmentation.py
│   ├── 9_Daily_Sales_Analysis.py
│   ├── 10_Advanced_Daily_Analysis.py
│   ├── 11_Actionable_Insights.py
│   ├── 13_Snowflake_SQL_Studio.py
│   ├── 14_Data_Quality_Monitor.py
│   └── 16_AI_Executive_Chat.py
└── utils/
    ├── data_loader.py
    ├── data_processing.py
    ├── metrics.py
    ├── kpis.py
    ├── risk_scoring.py
    ├── business_signal_engine.py
    ├── churn_analysis.py
    ├── forecasting.py
    ├── segmentation.py
    ├── snowflake_connector.py
    └── helpers.py


⸻

🧾 Supported Dataset (MFD)

The platform supports FMCG datasets with columns such as:
	•	Orders & Transactions
	•	Sales & Discounts
	•	SKUs, Brands, Categories
	•	Outlets & Geography
	•	Sales Force & Warehouses
	•	Time, Productivity & Assets

Designed specifically for large-scale FMCG operational data.

⸻

🤖 AI Executive Assistant (Key Highlight)

What it is:
A ChatGPT-style executive intelligence interface.

What it does:
	•	Answers business questions using only dataset logic
	•	Supports drill-downs & explain-why follow-ups
	•	No predictions, no hallucinations, no APIs

Example Queries:
	•	“Total sales in June”
	•	“Why were orders rejected?”
	•	“Top 10 SKUs by revenue”
	•	“Which outlets are inactive?”

✔ Fully deterministic
✔ Leadership-safe

⸻

🔐 Security & Governance
	•	No external APIs or LLM calls
	•	No data leaves the platform
	•	Snowflake access is read-only
	•	Session-based data isolation
	•	Fully auditable Python & SQL logic

⸻

⚠️ Known Limitations
	•	Forecasting is trend-based (no ML models)
	•	Chat assistant is dataset-bounded
	•	Real-time streaming not enabled
	•	Role-based access control (RBAC) not yet implemented

All limitations are intentional design choices to ensure accuracy, safety, and executive trust.

⸻

🚀 Deployment

The application is deployed on Streamlit Cloud.

Run Locally

pip install -r requirements.txt
streamlit run app.py


⸻

🧑‍💼 Internship Context
	•	Organization: D’s Group
	•	Role: Data / Analytics Intern
	•	Outcome:
	•	Built an end-to-end enterprise analytics system
	•	Delivered 16 production-ready modules
	•	Enabled leadership-level decision intelligence

⸻

🏁 Final Note

This project demonstrates:
	•	Enterprise analytics thinking
	•	Production-grade engineering
	•	Business-first AI implementation
	•	Strong ownership & system design skills

Built for real business decisions — not demos.

⸻

📬 Contact

Developer: Abhay Dubey
Role: Data / Analytics Engineer
Project: AI-Driven FMCG Decision Intelligence Platform

⸻
