from app import APP_NAME, DISEASES, greeting, main


def test_greeting_default_name():
    assert greeting() == f"Тавтай морил, Хэрэглэгч! Энэ бол {APP_NAME}."


def test_greeting_custom_name():
    assert "Дэлгэр" in greeting("Дэлгэр")


def test_diseases_count():
    assert len(DISEASES) == 3


def test_diseases_contains_rust():
    assert DISEASES["rust"] == "Зэв өвчин"


def test_main_prints_all_diseases(capsys):
    main()
    output = capsys.readouterr().out
    for name in DISEASES.values():
        assert f"- {name}" in output
