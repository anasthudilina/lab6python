from bank_app.config import get_allowed_currency

def test_currency_from_env(monkeypatch):
    monkeypatch.setenv("ALLOWED_CURRENCY", "USD")
    assert get_allowed_currency() == "USD"

def test_currency_default(monkeypatch):
    monkeypatch.delenv("ALLOWED_CURRENCY", raising=False)
    assert get_allowed_currency() == "UAH"