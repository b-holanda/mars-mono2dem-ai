"""Configuration loader utilities abiding by SOLID principles."""

from __future__ import annotations

import importlib
import pkgutil
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any, Dict, Mapping, MutableMapping, Optional, Tuple, Type

import yaml


@dataclass(frozen=True)
class SettingsFileResolver:
    """Finds the first settings file available under the configuration directory."""

    config_dir: Path
    candidates: Tuple[str, ...] = (
        "settings.yaml",
        "settings.yml",
        "settings.default.yaml",
        "settings.default.yml",
    )

    def resolve(self) -> Path:
        """Returns the first existing configuration file."""
        for candidate in self.candidates:
            path = self.config_dir / candidate
            if path.exists():
                return path
        raise FileNotFoundError(
            f"No settings file found in {self.config_dir}. Looked for: {', '.join(self.candidates)}"
        )

class SettingsLoader:
    """Loads YAML configuration data from disk."""

    def __init__(self, resolver: SettingsFileResolver) -> None:
        self._resolver = resolver

    def load(self) -> MutableMapping[str, Any]:
        """Reads YAML content and returns a mutable mapping."""
        path = self._resolver.resolve()
        with path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
        if not isinstance(data, MutableMapping):  # pragma: no cover - defensive guard
            raise TypeError(f"Settings file {path} must contain a mapping at the root level")
        return data

_initialized = False
_settings: MutableMapping[str, Any] = {}

def _initialize() -> MutableMapping[str, Any]:
    global _initialized
    global _settings

    resolver = SettingsFileResolver(config_dir=Path(__file__).resolve().parent.parent)

    _settings = SettingsLoader(resolver).load()
    _initialized = True

    return _settings

def config() -> MutableMapping[str, Any]:
    return _settings if _initialized else _initialize()
