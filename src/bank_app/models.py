from dataclasses import dataclass
from .exceptions import ValidationError, InsufficientFundsError

@dataclass
class Account:
    account_number: str
    client: str
    balance: float
    currency: str = "UAH"

    def __post_init__(self) -> None:
        if not self.account_number:
            raise ValidationError("Account number cannot be empty")
        if self.balance < 0:
            raise ValidationError("Initial balance cannot be negative")

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValidationError("Deposit amount must be positive")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValidationError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise InsufficientFundsError("Insufficient funds")
        self.balance -= amount

    def test_withdraw_exact_balance(valid_account):
        valid_account.withdraw(1000.0)
        assert valid_account.balance == 0.0