# Model Inspector API

Internal ML engineering utility to inspect trained model artifacts
(joblib / pickle) and generate human-readable reports.

## Features
- API-first design (FastAPI)
- Swagger UI via `/docs`
- Console tables for engineers
- Markdown inspection reports
- Artifact-only (no training data required)

## Run Locally
```bash
pip install -r requirements.txt
uvicorn api.main:app --reload
