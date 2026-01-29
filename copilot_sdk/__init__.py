"""GitHub Copilot SDK v2 - A Python SDK for interacting with GitHub Copilot Chat API."""

__version__ = "2.0.0"

from .client import CopilotClient
from .auth import get_copilot_token

__all__ = ["CopilotClient", "get_copilot_token"]
