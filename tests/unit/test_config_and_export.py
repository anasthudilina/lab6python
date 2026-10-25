import pytest
import json
from bank_app.config import get_allowed_currency
from bank_app.exporters import export_to_json

def test_currency_from_env(monkeypatch):
    monkeypatch.setenv("ALLOWED_CURRENCY", "USD")
    assert get_allowed_currency() == "USD"

def test_currency_default(monkeypatch):
    monkeypatch.delenv("ALLOWED_CURRENCY", raising=False)
    assert get_allowed_currency() == "UAH"

def test_export_to_json(tmp_path, valid_account):
    output_file = tmp_path / "accounts.json"
    export_to_json([valid_account], output_file)
    
    assert output_file.exists()
    data = json.loads(output_file.read_text(encoding="utf-8"))
    assert len(data) == 1
    assert data[0]["account_number"] == "UA001"