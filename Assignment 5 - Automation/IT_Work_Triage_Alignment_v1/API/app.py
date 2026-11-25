from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from pathlib import Path
import hashlib
import sqlite3
import joblib
import os
from datetime import datetime, timezone

APP_DIR = Path(__file__).resolve().parent
MODEL_FILE = APP_DIR / "assignment3_selected_model_naive_bayes.joblib"
DB_FILE = APP_DIR / "triage_api.sqlite3"

EXPECTED_MODEL_SHA256 = "e7e440cacfc5926e4eab482bc9baad188eebedf2dbab22b21b3d49fcffac4239"
MODEL_VERSION = "NB-v1"

app = FastAPI(
    title="INAI 6986 IT Work Triage Model API",
    version="1.0.0",
    description="Local scoring API for the frozen Assignment 3 TF-IDF + Multinomial Naive Bayes model."
)

model = None
model_hash = None


class ScoreRequest(BaseModel):
    request_id: str = Field(..., min_length=1, max_length=100)
    scenario_text: str = Field(..., min_length=5, max_length=10000)
    domain: Optional[str] = Field(default=None, max_length=100)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scored_requests (
                request_id TEXT PRIMARY KEY,
                received_at_utc TEXT NOT NULL,
                domain TEXT,
                scenario_text TEXT NOT NULL,
                prediction_code INTEGER NOT NULL,
                prediction TEXT NOT NULL,
                confidence REAL,
                model_version TEXT NOT NULL,
                model_sha256 TEXT NOT NULL
            )
        """)
        conn.commit()


def load_frozen_model():
    global model, model_hash

    if not MODEL_FILE.exists():
        raise RuntimeError(
            f"Frozen model not found: {MODEL_FILE.name}. "
            "Copy the exact Assignment 3 .joblib file into this folder."
        )

    model_hash = sha256_file(MODEL_FILE)

    if model_hash != EXPECTED_MODEL_SHA256:
        raise RuntimeError(
            "Model SHA-256 does not match the frozen Assignment 3 artifact. "
            f"Expected {EXPECTED_MODEL_SHA256}, got {model_hash}."
        )

    model = joblib.load(MODEL_FILE)


@app.on_event("startup")
def startup():
    init_db()
    load_frozen_model()


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "model_version": MODEL_VERSION,
        "model_sha256": model_hash,
    }


@app.post("/score")
def score(req: ScoreRequest):
    request_id = req.request_id.strip()
    scenario_text = req.scenario_text.strip()
    domain = req.domain.strip() if req.domain else None

    if not request_id:
        raise HTTPException(status_code=400, detail="request_id cannot be blank.")

    if len(scenario_text) < 5:
        raise HTTPException(status_code=400, detail="scenario_text is too short.")

    # Duplicate / idempotency protection
    with sqlite3.connect(DB_FILE) as conn:
        row = conn.execute(
            """
            SELECT request_id, prediction_code, prediction, confidence,
                   model_version, model_sha256, received_at_utc
            FROM scored_requests
            WHERE request_id = ?
            """,
            (request_id,)
        ).fetchone()

    if row:
        return {
            "status": "duplicate",
            "request_id": row[0],
            "prediction_code": row[1],
            "prediction": row[2],
            "confidence": row[3],
            "model_version": row[4],
            "model_sha256": row[5],
            "original_received_at_utc": row[6],
            "message": "Duplicate request_id detected. Existing result returned; no second action should be taken."
        }

    try:
        pred_code = int(model.predict([scenario_text])[0])

        confidence = None
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba([scenario_text])[0]
            confidence = float(max(probs))

        pred_label = (
            "Escalation Recommended"
            if pred_code == 1
            else "Generalist Handling Appropriate"
        )

        now = datetime.now(timezone.utc).isoformat()

        with sqlite3.connect(DB_FILE) as conn:
            conn.execute(
                """
                INSERT INTO scored_requests (
                    request_id, received_at_utc, domain, scenario_text,
                    prediction_code, prediction, confidence,
                    model_version, model_sha256
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    request_id, now, domain, scenario_text,
                    pred_code, pred_label, confidence,
                    MODEL_VERSION, model_hash
                )
            )
            conn.commit()

        return {
            "status": "scored",
            "request_id": request_id,
            "prediction_code": pred_code,
            "prediction": pred_label,
            "confidence": confidence,
            "review_required": bool(pred_code == 1),
            "model_version": MODEL_VERSION,
            "model_sha256": model_hash,
            "received_at_utc": now,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Model scoring failed: {type(exc).__name__}: {exc}"
        )


@app.get("/result/{request_id}")
def get_result(request_id: str):
    with sqlite3.connect(DB_FILE) as conn:
        row = conn.execute(
            """
            SELECT request_id, received_at_utc, domain, scenario_text,
                   prediction_code, prediction, confidence,
                   model_version, model_sha256
            FROM scored_requests
            WHERE request_id = ?
            """,
            (request_id,)
        ).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="request_id not found.")

    return {
        "request_id": row[0],
        "received_at_utc": row[1],
        "domain": row[2],
        "scenario_text": row[3],
        "prediction_code": row[4],
        "prediction": row[5],
        "confidence": row[6],
        "model_version": row[7],
        "model_sha256": row[8],
    }
