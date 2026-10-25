import pytest
from unittest.mock import Mock, AsyncMock
from bank_app.exceptions import ValidationError
from bank_app.services import AsyncBankService, BankService
from bank_app.models import Account


def test_create_account_interaction(bank_service, valid_account, mock_notifier):
    bank_service.create_account(valid_account)
    mock_notifier.send.assert_called_once_with(f"Account {valid_account.account_number} created")

def test_transfer_success(bank_service, valid_account, second_account, mock_notifier):
    bank_service.transfer("UA001", "UA002", 300.0)
    
    assert valid_account.balance == pytest.approx(700.0)
    assert second_account.balance == pytest.approx(800.0)
    mock_notifier.send.assert_called_once()

def test_transfer_missing_account(bank_service):
    with pytest.raises(ValidationError, match="not found"):
        bank_service.transfer("UA001", "UA999", 100.0)

def test_notifier_failure_path(bank_service, valid_account, mock_notifier):
    # side_effect triggers a failure scenario
    mock_notifier.send.side_effect = ConnectionError("Network down")
    
    with pytest.raises(ConnectionError):
        bank_service.create_account(valid_account)
def test_service_uses_repository_return_value(mock_notifier):
    repo = Mock()
    # Налаштовуємо return_value для Mock
    repo.get.return_value = Account("UA1", "Alice", 100.0)
    
    service = BankService(repo, mock_notifier)
    acc = repo.get("UA1")
    
    assert acc.client == "Alice"
    assert acc.balance == 100.0

@pytest.mark.asyncio
async def test_async_notifier():
    mock_async_notifier = AsyncMock()
    service = AsyncBankService(notifier=mock_async_notifier)
    
    await service.notify_client("Test message")
    
    mock_async_notifier.notify.assert_awaited_once_with("Test message")

