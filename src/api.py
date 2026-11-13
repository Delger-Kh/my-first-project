"""Ургамлын өвчин илрүүлэх систем — мобайл апп-ын backend REST API (Лаб 8: Docker).

Flutter мобайл апп энэ API руу HTTP/JSON хүсэлт илгээнэ:
  GET  /api/diseases          — өвчний жагсаалт (мэдлэгийн сан)
  POST /api/diagnoses         — навчны зураг илгээж онош авах
  GET  /api/diagnoses         — оношийн түүх
  GET  /health                — сервер ба өгөгдлийн сангийн төлөв
"""

import hashlib
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from sqlalchemy import select, text

from app import APP_NAME
from db import Diagnosis, Disease, SessionLocal, db_kind, init_db

VERSION = "1.1"
CONFIDENCE_THRESHOLD = 0.70  # Лаб 5: үүнээс бага бол агрономич хянана
MIN_IMAGE_BYTES = 1024  # хэт жижиг файл = тодорхойгүй зураг


@asynccontextmanager
async def lifespan(_app):
    init_db()
    print(f"{APP_NAME} API ажиллаж байна · өгөгдлийн сан: {db_kind()}", flush=True)
    yield


app = FastAPI(
    title="Ургамлын өвчин илрүүлэх систем — API",
    description="Flutter мобайл апп-д зориулсан backend (FastAPI + PostgreSQL, Docker-т ажиллана).",
    version=VERSION,
    lifespan=lifespan,
)


def predict(image_bytes: bytes):
    """AI загварын түр орлуулагч (stub).

    Жинхэнэ CNN загвар (жишээ нь MobileNetV2) холбогдох хүртэл зургийн hash-аас
    тогтвортой үр дүн гаргана: нэг зураг үргэлж нэг онош өгнө.
    """
    digest = hashlib.sha256(image_bytes).digest()
    codes = sorted(["powdery_mildew", "leaf_spot", "rust"])
    disease_code = codes[digest[0] % len(codes)]
    confidence = round(0.55 + (digest[1] / 255) * 0.44, 2)  # 0.55 – 0.99
    return disease_code, confidence


@app.get("/health")
def health():
    with SessionLocal() as session:
        session.execute(text("SELECT 1"))
    return {"status": "ok", "version": VERSION, "database": db_kind()}


@app.get("/api/diseases")
def list_diseases():
    with SessionLocal() as session:
        rows = session.scalars(select(Disease).order_by(Disease.code)).all()
        return [{"code": d.code, "name": d.name, "treatment": d.treatment} for d in rows]


@app.post("/api/diagnoses", status_code=201)
async def create_diagnosis(plant_name: str = Form(...), image: UploadFile = File(...)):
    data = await image.read()
    # Flutter-ийн http сан content-type-г ихэвчлэн octet-stream гэж илгээдэг тул өргөтгөлийг ч шалгана
    is_image = (image.content_type or "").startswith("image/") or (image.filename or "").lower().endswith(
        (".jpg", ".jpeg", ".png", ".webp")
    )
    if not is_image or len(data) < MIN_IMAGE_BYTES:
        raise HTTPException(status_code=422, detail="Зураг тодорхойгүй байна. Дахин зураг авна уу.")

    disease_code, confidence = predict(data)
    status = "AI_DONE" if confidence >= CONFIDENCE_THRESHOLD else "NEEDS_REVIEW"

    with SessionLocal() as session:
        disease = session.get(Disease, disease_code)
        diagnosis = Diagnosis(
            plant_name=plant_name,
            image_filename=image.filename or "leaf.jpg",
            disease_code=disease_code,
            confidence=confidence,
            status=status,
        )
        session.add(diagnosis)
        session.commit()
        return {
            "id": diagnosis.id,
            "plant_name": plant_name,
            "disease": disease.name,
            "confidence": confidence,
            "status": status,
            "treatment": disease.treatment,
            "message": "Агрономич хянах болно" if status == "NEEDS_REVIEW" else "AI онош бэлэн",
        }


@app.get("/api/diagnoses")
def list_diagnoses():
    with SessionLocal() as session:
        rows = session.scalars(select(Diagnosis).order_by(Diagnosis.id.desc())).all()
        return [
            {
                "id": d.id,
                "plant_name": d.plant_name,
                "disease_code": d.disease_code,
                "confidence": d.confidence,
                "status": d.status,
                "created_at": d.created_at.isoformat(),
            }
            for d in rows
        ]
