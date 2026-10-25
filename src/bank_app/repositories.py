from typing import Protocol
from .models import Account

class AccountRepository(Protocol):
    def add(self, account: Account) -> None: ...
    def get(self, account_number: str) -> Account | None: ...

class InMemoryAccountRepository:
    def __init__(self) -> None:
        self._accounts: dict[str, Account] = {}

    def add(self, account: Account) -> None:
        self._accounts[account.account_number] = account

    def get(self, account_number: str) -> Account | None:
        return self._accounts.get(account_number)