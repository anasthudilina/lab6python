import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.insert(0, src_dir)

import logging
from pathlib import Path
from reliable_importer.config import load_config
from reliable_importer.exceptions import ApplicationError
from reliable_importer.exporters import export_transactions_json
from reliable_importer.logging_config import configure_logging
from reliable_importer.services import ImportStatistics, import_transactions
from reliable_importer.utils import logged_operation

logger = logging.getLogger(__name__)

def main() -> None:
    try:
        config = load_config(Path("config.yaml"))
        configure_logging(config.logging.level, config.logging.path)
        statistics = ImportStatistics()

        with logged_operation("Bank data import/export"):
            # Використовуємо генератор для потокового читання
            transactions_gen = import_transactions(
                config.input_path, 
                config.processing.skip_invalid, 
                statistics
            )
            
            # Експорт (генератор споживається під час запису)
            exported_count = export_transactions_json(transactions_gen, config.output_path)
            
            logger.info(
                "Total=%d, valid=%d, invalid=%d, exported=%d",
                statistics.total, statistics.valid, statistics.invalid, exported_count
            )

    except ApplicationError:
        logger.exception("Application stopped due to critical error")
        sys.exit(1)

if __name__ == "__main__":
    main()