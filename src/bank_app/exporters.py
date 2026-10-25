import json
from pathlib import Path
from .models import Account

def export_to_json(accounts: list[Account], file_path: Path) -> None:
    data = [
        {"account_number": a.account_number, "balance": a.balance, "currency": a.currency}
        for a in accounts
    ]
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(json.dumps(data, indent=2), encoding="utf-8")