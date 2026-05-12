# src/api/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
from src.access.rbac import get_current_user, require_permission
from src.pii.anonymizer import MedVietAnonymizer

app = FastAPI(title="MedViet Data API", version="1.0.0")
anonymizer = MedVietAnonymizer()

# --- ENDPOINT 1 ---
@app.get("/api/patients/raw")
@require_permission(resource="patient_data", action="read")
async def get_raw_patients(
    current_user: dict = Depends(get_current_user)
):
    try:
        df = pd.read_csv("data/raw/patients_raw.csv")
        return df.head(10).to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- ENDPOINT 2 ---
@app.get("/api/patients/anonymized")
@require_permission(resource="training_data", action="read")
async def get_anonymized_patients(
    current_user: dict = Depends(get_current_user)
):
    try:
        df = pd.read_csv("data/raw/patients_raw.csv")
        df_anon = anonymizer.anonymize_dataframe(df)
        return df_anon.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- ENDPOINT 3 ---
@app.get("/api/metrics/aggregated")
@require_permission(resource="aggregated_metrics", action="read")
async def get_aggregated_metrics(
    current_user: dict = Depends(get_current_user)
):
    try:
        df = pd.read_csv("data/raw/patients_raw.csv")
        metrics = df.groupby("benh").size().to_dict()
        return {"patient_count_by_disease": metrics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- ENDPOINT 4 ---
@app.delete("/api/patients/{patient_id}")
@require_permission(resource="patient_data", action="delete")
async def delete_patient(
    patient_id: str,
    current_user: dict = Depends(get_current_user)
):
    # Trong lab này, chúng ta chỉ giả lập việc xóa (vì không dùng DB thật)
    return JSONResponse(
        status_code=200,
        content={"message": f"Patient {patient_id} deleted successfully by {current_user['username']}"}
    )

@app.get("/health")
async def health():
    return {"status": "ok", "service": "MedViet Data API"}
