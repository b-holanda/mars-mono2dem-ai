"""Central logging utilities shared across the project."""

from __future__ import annotations

import json
import logging
import logging.config
import os
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, MutableMapping, Optional

import yaml

_DEFAULT_LOGGING_DICT: Mapping[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "std": {
            "format": "%(asctime)s | %(levelname)-7s | %(name)s:%(lineno)d | %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "std",
            "level": "INFO",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "app.log",
            "maxBytes": 5_000_000,
            "backupCount": 3,
            "formatter": "std",
            "level": "INFO",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": "INFO",
        }
    },
}


@dataclass
class LoggingConfigurator:
    """Builds and applies logging configurations."""

    default_config: Mapping[str, Any] = field(default_factory=lambda: deepcopy(_DEFAULT_LOGGING_DICT))

    def configure(self, config_path: Optional[str] = None, level: str = "INFO") -> None:
        """Applies logging configuration from file or defaults."""
        path = self._resolve_config_path(config_path)
        if path:
            config_dict = self._load_external_config(path)
        else:
            config_dict = self._with_level(level)
        logging.config.dictConfig(config_dict)

    def _resolve_config_path(self, config_path: Optional[str]) -> Optional[Path]:
        """Chooses the path from explicit argument or LOG_CFG env var."""
        candidate = config_path or os.getenv("LOG_CFG")
        resolved = Path(candidate) if candidate else None
        if resolved and resolved.exists():
            return resolved
        return None

    def _with_level(self, level: str) -> MutableMapping[str, Any]:
        """Returns a copy of the default config with uniform log level."""
        config = deepcopy(self.default_config)
        # Comentário: garante consistência de nível para handlers e logger raiz.
        config["handlers"]["console"]["level"] = level
        config["handlers"]["file"]["level"] = level
        config["loggers"][""]["level"] = level
        return config  # type: ignore[return-value]

    def _load_external_config(self, path: Path) -> Mapping[str, Any]:
        """Parses JSON/YAML logging configuration files."""
        suffix = path.suffix.lower()
        with path.open("r", encoding="utf-8") as handle:
            if suffix in {".yaml", ".yml"}:
                return yaml.safe_load(handle) or {}
            return json.load(handle)


_CONFIGURED = False
_CONFIGURATOR = LoggingConfigurator()


def setup_logging(config_path: Optional[str] = None, level: str = "INFO") -> None:
    """Configures logging only once to avoid repeated dictConfig calls."""
    global _CONFIGURED
    if _CONFIGURED:
        return
    _CONFIGURATOR.configure(config_path=config_path, level=level)
    _CONFIGURED = True


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Returns a configured logger instance."""
    return logging.getLogger(name)
