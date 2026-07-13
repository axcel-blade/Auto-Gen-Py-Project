"""Shared exceptions."""

from __future__ import annotations


class AutoGenError(Exception):
    """Base error for auto-gen-py-project."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class ConfigurationError(AutoGenError):
    """Invalid or missing configuration."""


class TemplateError(AutoGenError):
    """Template discovery, rendering, or validation failure."""


class GenerationError(AutoGenError):
    """Project generation failure."""


class PluginError(AutoGenError):
    """Plugin load or execution failure."""
