from datetime import datetime
from pathlib import Path
from tabulate import tabulate


def _safe_table(data: dict):
    rows = []
    for k, v in data.items():
        rows.append((k, str(v)))
    return tabulate(rows, headers=["Property", "Value"], tablefmt="github")


def generate_markdown_report(model_info, scaler_info, output_dir="reports"):
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    ts = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    report_path = output_dir / f"model_inspection_{ts}.md"

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Model Inspection Report\n\n")
        f.write(f"Generated on: {datetime.now()}\n\n")

        f.write("## Model Overview\n\n")
        f.write(_safe_table({
            "Class": model_info.get("class_name"),
            "Module": model_info.get("module"),
            "Task": model_info.get("task"),
            "Has Coefficients": model_info.get("has_coefficients", False),
            "Feature Importance Available": model_info["feature_importance"]["available"],
            "Feature Importance Type": model_info["feature_importance"]["type"]
        }))
        f.write("\n\n")

        f.write("## Feature Importance Details\n\n")
        f.write(_safe_table({
            "Details": model_info["feature_importance"]["details"]
        }))
        f.write("\n\n")

        f.write("## Hyperparameters\n\n")
        f.write(_safe_table(model_info.get("hyperparameters", {})))
        f.write("\n\n")

        if scaler_info:
            f.write("## Preprocessing\n\n")
            f.write(_safe_table({
                "Scaler": scaler_info["class_name"],
                "Module": scaler_info["module"]
            }))
            f.write("\n\n")

        f.write("## Engineering Notes\n")
        f.write("- Artifact-only inspection\n")
        f.write("- XGBoost / sklearn safe\n")
        f.write("- Raw internals intentionally hidden\n")

    return str(report_path)


def print_console_tables(model_info, scaler_info):
    print("\nMODEL SUMMARY")
    print(_safe_table({
        "Class": model_info.get("class_name"),
        "Module": model_info.get("module"),
        "Task": model_info.get("task")
    }))
