"""Лаб 10: AAA (Arrange-Act-Assert) зарчмаар бичсэн 5 тест."""

from unittest.mock import Mock

import pytest

from diagnosis import diagnose, severity_level


# ---------- 1-2. Хэвийн тохиолдол (unit test) ----------

def test_severity_light_when_few_leaves_infected():
    # Arrange
    infected, total = 2, 20  # 10%

    # Act
    level = severity_level(infected, total)

    # Assert
    assert level == "Хөнгөн"


def test_severity_severe_when_most_leaves_infected():
    # Arrange
    infected, total = 15, 20  # 75%

    # Act
    level = severity_level(infected, total)

    # Assert
    assert level == "Хүнд"


# ---------- 3-4. Хилийн тохиолдол (edge case) ----------

def test_severity_raises_when_total_is_zero():
    # Arrange
    infected, total = 0, 0  # хоосон утга — 0-д хуваах аюултай

    # Act + Assert
    with pytest.raises(ValueError):
        severity_level(infected, total)


def test_severity_raises_when_infected_is_negative():
    # Arrange
    infected, total = -3, 20  # сөрөг тоо

    # Act + Assert
    with pytest.raises(ValueError):
        severity_level(infected, total)


# ---------- 5. Mock ашигласан тест ----------

def test_diagnose_uses_mocked_ai_model():
    # Arrange — жинхэнэ AI API-г дуудахгүй, Mock-оор орлуулна
    fake_model = Mock()
    fake_model.predict.return_value = {"label": "rust", "confidence": 0.92}
    image = b"fake-leaf-image"

    # Act
    result = diagnose(image, fake_model)

    # Assert
    assert result == "Зэв өвчин"
    fake_model.predict.assert_called_once_with(image)