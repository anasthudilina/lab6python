from typing import Protocol
from .models import Account
from .repositories import AccountRepository
from .exceptions import ValidationError

class Notifier(Protocol):
    def send(self, message: str) -> None: ...

class AsyncNotifier(Protocol):
    async def notify(self, message: str) -> None: ...

class BankService:
    def __init__(self, repo: AccountRepository, notifier: Notifier) -> None:
        self._repo = repo
        self._notifier = notifier

    def create_account(self, account: Account) -> None:
        self._repo.add(account)
        self._notifier.send(f"Account {account.account_number} created")

    def transfer(self, from_acc: str, to_acc: str, amount: float) -> None:
        source = self._repo.get(from_acc)
        target = self._repo.get(to_acc)
        
        if source is None or target is None:
            raise ValidationError("One or both accounts not found")

        source.withdraw(amount)
        target.deposit(amount)
        self._notifier.send(f"Transferred {amount} {source.currency} to {to_acc}")

class AsyncBankService:
    def __init__(self, notifier: AsyncNotifier) -> None:
        self._notifier = notifier

    async def notify_client(self, message: str) -> None:
        await self._notifier.notify(message)