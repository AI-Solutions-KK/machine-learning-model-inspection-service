import streamlit as st
import requests
from pathlib import Path
import shutil

API_URL = "http://127.0.0.1:8000/api/v1/inspect"
ARTIFACTS_DIR = Path("artifacts")
REPORTS_DIR = Path("reports")

ARTIFACTS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

st.set_page_config(page_title="Model Inspector", layout="centered")

st.title("🔍 Model Inspector")
st.caption("Local UI for inspecting ML model artifacts")

st.divider()

# ---- Upload Section ----
st.subheader("Upload Model Files")

model_file = st.file_uploader(
    "Upload model file (.joblib / .pkl)",
    type=["joblib", "pkl"]
)

scaler_file = st.file_uploader(
    "Upload scaler file (optional)",
    type=["joblib", "pkl"]
)

# ---- Save uploaded files ----
def save_uploaded_file(uploaded_file, target_dir):
    file_path = target_dir / uploaded_file.name
    with open(file_path, "wb") as f:
        shutil.copyfileobj(uploaded_file, f)
    return str(file_path)


# ---- Analyze Button ----
if st.button("Analyze Model", type="primary"):
    if not model_file:
        st.error("Please upload a model file.")
        st.stop()

    with st.spinner("Saving files..."):
        model_path = save_uploaded_file(model_file, ARTIFACTS_DIR)
        scaler_path = None
        if scaler_file:
            scaler_path = save_uploaded_file(scaler_file, ARTIFACTS_DIR)

    payload = {
        "model_path": model_path
    }
    if scaler_path:
        payload["scaler_path"] = scaler_path

    with st.spinner("Inspecting model..."):
        try:
            response = requests.post(API_URL, json=payload)
        except Exception as e:
            st.error(f"Failed to connect to API: {e}")
            st.stop()

    if response.status_code != 200:
        st.error("Inspection failed")
        st.code(response.text)
        st.stop()

    data = response.json()

    st.success("Inspection completed successfully!")

    # ---- Results ----
    st.subheader("Model Summary")
    st.json(data["model_summary"])

    report_path = data["report_path"]

    if Path(report_path).exists():
        st.subheader("Inspection Report")

        with open(report_path, "r", encoding="utf-8") as f:
            report_content = f.read()

        st.markdown(report_content)

        st.download_button(
            label="Download Report (.md)",
            data=report_content,
            file_name=Path(report_path).name,
            mime="text/markdown"
        )
    else:
        st.warning("Report file not found.")
