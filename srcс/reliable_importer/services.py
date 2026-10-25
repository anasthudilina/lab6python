import logging
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from .exceptions import RecordValidationError
from .models import BankTransaction
from .readers import read_csv_rows
from .validators import parse_transaction

logger = logging.getLogger(__name__)

@dataclass
class ImportStatistics:
    total: int = 0
    valid: int = 0
    invalid: int = 0

def import_transactions(
    path: Path, skip_invalid: bool, statistics: ImportStatistics
) -> Iterator[BankTransaction]:
    for line_number, row in read_csv_rows(path):
        statistics.total += 1
        try:
            transaction = parse_transaction(row, line_number=line_number)
        except RecordValidationError as error:
            statistics.invalid += 1
            logger.warning("Invalid record at line %s: %s", error.line_number, error)
            if skip_invalid:
                continue
            raise
        statistics.valid += 1
        yield transaction