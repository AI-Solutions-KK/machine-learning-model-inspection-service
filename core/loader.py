from pathlib import Path
import joblib


class ArtifactNotFoundError(Exception):
    pass


class ArtifactLoadError(Exception):
    pass


def _validate_path(path: str) -> Path:
    """
    Validate that the artifact path exists and is a file.
    """
    p = Path(path)

    if not p.exists():
        raise ArtifactNotFoundError(f"Artifact not found: {path}")

    if not p.is_file():
        raise ArtifactLoadError(f"Path is not a file: {path}")

    return p


def load_artifact(path: str):
    """
    Generic loader for any joblib / pickle artifact.
    """
    artifact_path = _validate_path(path)

    try:
        return joblib.load(artifact_path)
    except Exception as e:
        raise ArtifactLoadError(
            f"Failed to load artifact '{artifact_path.name}': {str(e)}"
        )


def load_model_and_scaler(model_path: str, scaler_path: str | None = None):
    """
    Load model and optional scaler safely.
    """
    model = load_artifact(model_path)

    scaler = None
    if scaler_path:
        scaler = load_artifact(scaler_path)

    return {
        "model": model,
        "scaler": scaler
    }
