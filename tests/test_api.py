import pytest
from fastapi.testclient import TestClient

from api import app
from app import DISEASES


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:  # lifespan → init_db() ажиллана
        yield c


def fake_image(seed=b"leaf"):
    return seed * 400  # 1KB-аас их


def test_health(client):
    body = client.get("/health").json()
    assert body["status"] == "ok"


def test_diseases_seeded_from_app(client):
    names = {d["name"] for d in client.get("/api/diseases").json()}
    assert names == set(DISEASES.values())


def test_create_diagnosis(client):
    r = client.post(
        "/api/diagnoses",
        data={"plant_name": "Улаан лооль"},
        files={"image": ("leaf.jpg", fake_image(), "image/jpeg")},
    )
    assert r.status_code == 201
    body = r.json()
    assert body["disease"] in DISEASES.values()
    assert body["status"] == ("AI_DONE" if body["confidence"] >= 0.70 else "NEEDS_REVIEW")


def test_blurry_image_rejected(client):
    r = client.post(
        "/api/diagnoses",
        data={"plant_name": "Өргөст хэмх"},
        files={"image": ("tiny.jpg", b"x" * 10, "image/jpeg")},
    )
    assert r.status_code == 422


def test_history_lists_diagnoses(client):
    assert len(client.get("/api/diagnoses").json()) >= 1
