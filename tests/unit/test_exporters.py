import json
from bank_app.exporters import export_to_json

def test_export_to_json(tmp_path, valid_account):
    output_file = tmp_path / "accounts.json"
    export_to_json([valid_account], output_file)
    
    assert output_file.exists()
    data = json.loads(output_file.read_text(encoding="utf-8"))
    assert len(data) == 1
    assert data[0]["account_number"] == "UA001"