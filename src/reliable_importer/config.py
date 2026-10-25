from pathlib import Path
import yaml
from dataclasses import dataclass
from .exceptions import ConfigurationError

@dataclass(frozen=True, slots=True)
class ProcessingConfig:
    skip_invalid: bool

@dataclass(frozen=True, slots=True)
class LoggingConfig:
    level: str
    path: Path

@dataclass(frozen=True, slots=True)
class AppConfig:
    input_path: Path
    output_path: Path
    processing: ProcessingConfig
    logging: LoggingConfig

def load_config(path: Path) -> AppConfig:
    try:
        with path.open("r", encoding="utf-8") as file:
            raw = yaml.safe_load(file)
    except FileNotFoundError as error:
        raise ConfigurationError(f"Configuration file not found: {path}") from error
    except yaml.YAMLError as error:
        raise ConfigurationError("Invalid YAML configuration") from error

    try:
        config = AppConfig(
            input_path=Path(raw["input"]["path"]),
            output_path=Path(raw["output"]["path"]),
            processing=ProcessingConfig(skip_invalid=bool(raw["processing"]["skip_invalid"])),
            logging=LoggingConfig(
                level=str(raw["logging"]["level"]),
                path=Path(raw["logging"]["path"])
            )
        )
    except (KeyError, TypeError, ValueError) as error:
        raise ConfigurationError("Missing or invalid configuration keys") from error

    # Fail-fast validation
    if not config.input_path.exists():
        raise ConfigurationError(f"Input file not found: {config.input_path}")

    return config