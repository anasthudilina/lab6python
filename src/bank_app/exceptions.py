class BankAppError(Exception):
    """Base exception for the app."""

class ValidationError(BankAppError):
    """Invalid input data."""

class InsufficientFundsError(BankAppError):
    """Not enough money."""