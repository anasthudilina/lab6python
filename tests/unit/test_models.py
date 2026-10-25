import pytest
from bank_app.models import Account
from bank_app.exceptions import ValidationError, InsufficientFundsError

# Normal & Boundary cases for creation
@pytest.mark.parametrize("amount, expected", [
    (0.0, 0.0),
    (0.01, 0.01),
    (1000.0, 1000.0),
])
def test_account_creation(amount, expected):
    acc = Account("UA1", "Test", amount)
    assert acc.balance == pytest.approx(expected)

def test_account_negative_balance_rejected():
    with pytest.raises(ValidationError, match="negative"):
        Account("UA1", "Test", -1.0)

def test_empty_account_number_rejected():
    with pytest.raises(ValidationError, match="empty"):
        Account("", "Test", 10.0)

# Deposit tests
def test_deposit_valid(valid_account):
    valid_account.deposit(500.0)
    assert valid_account.balance == pytest.approx(1500.0)

@pytest.mark.parametrize("invalid_amount", [0, -1, -100])
def test_deposit_invalid_amount(valid_account, invalid_amount):
    with pytest.raises(ValidationError, match="positive"):
        valid_account.deposit(invalid_amount)

# Withdraw tests
def test_withdraw_valid(valid_account):
    valid_account.withdraw(200.0)
    assert valid_account.balance == pytest.approx(800.0)

def test_withdraw_insufficient_funds(valid_account):
    with pytest.raises(InsufficientFundsError, match="Insufficient"):
        valid_account.withdraw(2000.0)