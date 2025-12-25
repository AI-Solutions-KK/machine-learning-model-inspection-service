# Model Inspector API

Internal ML engineering utility to inspect trained model artifacts
(joblib / pickle), analyze model metadata, and generate human-readable
inspection reports via an API.

This project is designed for **model governance, reverse-engineering,
and auditability** when original training code or datasets are unavailable.

---

## 🎯 Use Case

This tool is useful when you:
- Receive trained ML models without training code
- Need to understand model type, task, and structure
- Want to rebuild or fine-tune a similar model safely
- Need internal inspection tooling (not a demo app)

The system focuses on **artifact-only inspection** — no training data
is required.

---

## ✨ Key Features

- API-first design using **FastAPI**
- Supports **scikit-learn** and **XGBoost** models
- Safe model deserialization (joblib / pickle)
- Extracts:
  - Model class & module
  - ML task (regression / classification)
  - Hyperparameters (when available)
  - Feature importance availability
  - Preprocessing metadata (scalers)
- Generates **human-readable Markdown reports**
- Swagger UI available at `/docs`
- Optional local Streamlit UI for easy uploads (non-production)

---

## 🧱 Architecture

Client / UI  
→ HTTP (JSON)  
→ FastAPI Inspector Service  
→ Markdown Report (.md)

The API is the **single source of truth**.  
UI clients are intentionally thin.

## 📂 Project Structure

---
## 📁 Project Structure

````
model_inspector/
├── api/
│   ├── main.py                 # FastAPI app entry point
│   └── v1/
│       ├── __init__.py
│       └── endpoints.py        # /inspect API endpoint
│
├── core/
│   ├── __init__.py
│   ├── loader.py               # Safe artifact loading
│   └── analyzer.py             # Model inspection logic
│
├── inspection/
│   ├── __init__.py
│   └── formatter.py            # Markdown + console reports
│
├── reports/
│   └── model_inspection_*.md   # Generated reports
│
├── artifacts/                  # Local model files (gitignored)
│
├── app.py                      # Local Streamlit UI (optional)
├── Dockerfile                  # Container configuration
├── requirements.txt            # Dependencies
├── README.md                   # Documentation
├── LICENSE
└── .gitignore

---


## 🚀 Run Locally

pip install -r requirements.txt  
uvicorn api.main:app --reload  

Swagger UI:
http://127.0.0.1:8000/docs

---

## 🧪 API Usage

POST /api/v1/inspect

Request body:
{
  "model_path": "artifacts/model.joblib",
  "scaler_path": "artifacts/scaler.joblib"
}

---

## 🐳 Docker

docker build -t model-inspector .  
docker run -p 8000:8000 model-inspector

---

## 📄 License

MIT License
