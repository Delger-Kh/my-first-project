"""Ургамлын өвчний оношлогоо — Лаб 10-ын тестлэх функцүүд."""

from app import DISEASES

UNKNOWN = "Тодорхойгүй"
MIN_CONFIDENCE = 0.6


def severity_level(infected_leaves, total_leaves):
    """Өвчилсөн навчны хувиар өвчний түвшинг тодорхойлно."""
    if total_leaves <= 0:
        raise ValueError("Нийт навчны тоо 0-ээс их байх ёстой")
    if infected_leaves < 0 or infected_leaves > total_leaves:
        raise ValueError("Өвчилсөн навчны тоо 0 ба нийт тооны хооронд байх ёстой")

    percent = infected_leaves / total_leaves * 100
    if percent == 0:
        return "Эрүүл"
    if percent < 25:
        return "Хөнгөн"
    if percent < 50:
        return "Дунд"
    return "Хүнд"


def diagnose(image, model_client):
    """Зургийг гадаад AI загвар руу илгээж, өвчний нэрийг монголоор буцаана.

    model_client.predict(image) нь {"label": "rust", "confidence": 0.92}
    хэлбэрийн хариу өгдөг гадаад API гэж үзнэ.
    """
    result = model_client.predict(image)
    if result["confidence"] < MIN_CONFIDENCE:
        return UNKNOWN
    return DISEASES.get(result["label"], UNKNOWN)