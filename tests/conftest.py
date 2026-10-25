import pytest
from unittest.mock import Mock, AsyncMock
from bank_app.models import Account
from bank_app.repositories import InMemoryAccountRepository
from bank_app.services import BankService, AsyncBankService

@pytest.fixture
def valid_account() -> Account:
    return Account(account_number="UA001", client="Alice", balance=1000.0)

@pytest.fixture
def second_account() -> Account:
    return Account(account_number="UA002", client="Bob", balance=500.0)

@pytest.fixture
def repository(valid_account, second_account) -> InMemoryAccountRepository:
    repo = InMemoryAccountRepository()
    repo.add(valid_account)
    repo.add(second_account)
    return repo

@pytest.fixture
def mock_notifier() -> Mock:
    return Mock()

@pytest.fixture
def bank_service(repository, mock_notifier) -> BankService:
    return BankService(repo=repository, notifier=mock_notifier)