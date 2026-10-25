from .exceptions import RecordValidationError
from .models import BankTransaction

def parse_transaction(row: dict[str, str], *, line_number: int) -> BankTransaction:
    try:
        account_number = row.get("account_number", "").strip()
        if not account_number:
            raise RecordValidationError("Account number is empty", line_number=line_number, field="account_number")

        client = row.get("client", "").strip()
        if not client:
            raise RecordValidationError("Client name is empty", line_number=line_number, field="client")

        operation = row.get("operation", "").strip()
        if operation not in ("deposit", "withdraw"):
            raise RecordValidationError("Invalid operation type", line_number=line_number, field="operation")

        try:
            balance = float(row["balance"])
            amount = float(row["amount"])
        except (KeyError, TypeError, ValueError) as error:
            raise RecordValidationError("Invalid numeric format", line_number=line_number) from error

        if balance < 0:
            raise RecordValidationError("Balance cannot be negative", line_number=line_number, field="balance")
        
        if amount <= 0:
            raise RecordValidationError("Amount must be positive", line_number=line_number, field="amount")

        new_balance = balance + amount if operation == "deposit" else balance - amount
        if new_balance < 0:
            raise RecordValidationError("Operation causes negative balance", line_number=line_number, field="amount")

        return BankTransaction(
            account_number=account_number,
            client=client,
            balance=new_balance,
            operation=operation,
            amount=amount
        )
    except KeyError as error:
        raise RecordValidationError(f"Missing field: {error}", line_number=line_number) from error