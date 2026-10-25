import os

def get_allowed_currency() -> str:
    return os.getenv("ALLOWED_CURRENCY", "UAH")