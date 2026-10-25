import pytest
from bank_app.models import Account
from bank_app.exceptions import ValidationError, InsufficientFundsError

def test_account_negative_balance_rejected():
    with pytest.raises(ValidationError, match="negative"):
        Account("UA1", "Test", -1.0)

def test_empty_account_number_rejected():
    with pytest.raises(ValidationError, match="empty"):
        Account("", "Test", 10.0)

def test_withdraw_insufficient_funds(valid_account):
    with pytest.raises(InsufficientFundsError, match="Insufficient"):
        valid_account.withdraw(2000.0)