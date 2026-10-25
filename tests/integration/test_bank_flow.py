import json
import pytest
from bank_app.models import Account
from bank_app.repositories import InMemoryAccountRepository
from bank_app.services import BankService
from bank_app.exporters import export_to_json
from unittest.mock import Mock

def test_full_operation_pipeline(tmp_path):
    # Arrange
    notifier = Mock()
    repo = InMemoryAccountRepository()
    service = BankService(repo, notifier)
    
    acc1 = Account("UA1", "Alice", 1000.0)
    acc2 = Account("UA2", "Bob", 500.0)
    
    # Act
    service.create_account(acc1)
    service.create_account(acc2)
    service.transfer("UA1", "UA2", 250.0)
    
    accounts = [acc1, acc2]
    output_file = tmp_path / "report.json"
    export_to_json(accounts, output_file)
    
    # Assert
    data = json.loads(output_file.read_text())
    assert data[0]["balance"] == 750.0
    assert data[1]["balance"] == 750.0
    assert notifier.send.call_count == 3

def test_export_pipeline_failure(tmp_path):
    # Arrange
    invalid_path = tmp_path / "dir" / "file.json"
    invalid_path.mkdir(parents=True, exist_ok=True) # Створюємо папку замість файлу
    
    # Act & Assert
    # Додаємо PermissionError для сумісності з Windows
    with pytest.raises((IsADirectoryError, PermissionError)):
        export_to_json([], invalid_path)