from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from core.loader import load_model_and_scaler, ArtifactLoadError, ArtifactNotFoundError
from core.analyzer import analyze_model, analyze_scaler
from inspection.formatter import generate_markdown_report, print_console_tables

router = APIRouter()


class InspectRequest(BaseModel):
    model_path: str
    scaler_path: str | None = None


@router.post("/inspect")
def inspect_model(request: InspectRequest):
    try:
        artifacts = load_model_and_scaler(
            request.model_path,
            request.scaler_path
        )

        model_info = analyze_model(artifacts["model"])
        scaler_info = analyze_scaler(artifacts["scaler"])

        # Console output (never crashes API)
        try:
            print_console_tables(model_info, scaler_info)
        except Exception as e:
            print("Console table warning:", str(e))

        report_path = generate_markdown_report(model_info, scaler_info)

        return {
            "model_summary": {
                "class": model_info.get("class_name"),
                "module": model_info.get("module"),
                "task": model_info.get("task")
            },
            "report_path": report_path
        }

    except (ArtifactLoadError, ArtifactNotFoundError) as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        # 🔥 THIS IS THE KEY FIX
        raise HTTPException(
            status_code=500,
            detail=f"Inspector internal error: {str(e)}"
        )
