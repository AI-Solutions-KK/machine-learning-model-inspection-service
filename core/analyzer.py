def analyze_model(model):
    info = {}

    info["class_name"] = model.__class__.__name__
    info["module"] = model.__class__.__module__

    # Hyperparameters (safe)
    info["hyperparameters"] = {}
    if hasattr(model, "get_params"):
        try:
            info["hyperparameters"] = model.get_params()
        except Exception:
            info["hyperparameters"] = {}

    # Task detection
    name = info["class_name"].lower()
    if "classifier" in name:
        info["task"] = "classification"
    elif "regressor" in name:
        info["task"] = "regression"
    else:
        info["task"] = "unknown"

    # Coefficients (safe)
    info["has_coefficients"] = False
    try:
        if hasattr(model, "coef_"):
            info["has_coefficients"] = True
    except Exception:
        info["has_coefficients"] = False

    # Feature importance (XGBoost + sklearn safe)
    info["feature_importance"] = {
        "available": False,
        "type": None,
        "details": None
    }

    # sklearn-style
    if hasattr(model, "feature_importances_"):
        try:
            fi = model.feature_importances_
            info["feature_importance"] = {
                "available": True,
                "type": "sklearn_style",
                "details": {
                    "length": len(fi)
                }
            }
        except Exception:
            pass

    # XGBoost native
    elif hasattr(model, "get_booster"):
        try:
            booster = model.get_booster()
            score = booster.get_score(importance_type="weight")
            info["feature_importance"] = {
                "available": True,
                "type": "xgboost_booster",
                "details": {
                    "num_features": len(score)
                }
            }
        except Exception:
            pass

    return info


def analyze_scaler(scaler):
    if scaler is None:
        return None

    return {
        "class_name": scaler.__class__.__name__,
        "module": scaler.__class__.__module__,
        "parameters": scaler.get_params() if hasattr(scaler, "get_params") else {}
    }
