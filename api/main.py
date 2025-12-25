from fastapi import FastAPI
from api.v1.endpoints import router

app = FastAPI(
    title="Model Inspector API",
    description="Internal ML model inspection utility",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok"}
