"""Өгөгдлийн сангийн тохиргоо ба хүснэгтүүд (Лаб 5-ын Data давхарга).

DATABASE_URL орчны хувьсагчаар PostgreSQL руу холбогдоно (docker compose).
Тохируулаагүй бол локал SQLite файл ашиглана (тест, хөгжүүлэлт).
"""

import os
from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from app import DISEASES

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./plant.db")

_connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=_connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class Disease(Base):
    __tablename__ = "diseases"

    code: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    treatment: Mapped[str] = mapped_column(Text)


class Diagnosis(Base):
    __tablename__ = "diagnoses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    plant_name: Mapped[str] = mapped_column(String(100))
    image_filename: Mapped[str] = mapped_column(String(255))
    disease_code: Mapped[str] = mapped_column(ForeignKey("diseases.code"))
    confidence: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(20))  # AI_DONE | NEEDS_REVIEW
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )


TREATMENTS = {
    "powdery_mildew": "Өвчилсөн навчийг тайрч устгах, хүхэр агуулсан фунгицид шүрших, агааржуулалтыг сайжруулах.",
    "leaf_spot": "Навчийг нойтон байлгахгүйн тулд ёроолоор нь услах, зэс агуулсан бэлдмэл хэрэглэх.",
    "rust": "Халдвартай навчийг түүж устгах, триазол бүлгийн фунгицид хэрэглэх.",
}


def init_db():
    """Хүснэгт үүсгэж, app.py дахь өвчний жагсаалтаар мэдлэгийн санг дүүргэнэ."""
    Base.metadata.create_all(engine)
    with SessionLocal() as session:
        for code, name in DISEASES.items():
            if session.get(Disease, code) is None:
                session.add(Disease(code=code, name=name, treatment=TREATMENTS.get(code, "")))
        session.commit()


def db_kind():
    return engine.dialect.name  # "postgresql" эсвэл "sqlite"
