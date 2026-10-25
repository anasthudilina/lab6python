from dataclasses import dataclass, asdict

@dataclass(frozen=True, slots=True)
class BankTransaction:
    account_number: str
    client: str
    balance: float
    operation: str
    amount: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)