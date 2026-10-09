"""Ургамлын өвчин илрүүлэх болон арчилгааны зөвлөх систем — жишээ модуль (Лаб 6)."""

APP_NAME = "Ургамлын өвчин илрүүлэх систем"

DISEASES = {
    "powdery_mildew": "Цагаан хөгц",
    "leaf_spot": "Навчны толбо",
    "rust": "Зэв өвчин",
}


def greeting():
    return "Сайн байна уу!"


def main():
    print(greeting())
    print(f"{APP_NAME} — таних боломжтой өвчнүүд:")
    for name in DISEASES.values():
        print(f"- {name}")


if __name__ == "__main__":
    main()