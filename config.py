

"""Central configuration loaded from environment variables or an ``.env`` file."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Load variables from a .env file if present
load_dotenv(Path(__file__).resolve().with_name(".env"))

PRINTIFY_API_KEY = os.getenv("PRINTIFY_API_KEY", "")
BASE_URL = os.getenv("BASE_URL", "https://api.printify.com/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Optional Google Drive uploader configuration
GOOGLE_SERVICE_ACCOUNT = os.getenv("GOOGLE_SERVICE_ACCOUNT", "")
GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "")


class ConfigError(ValueError):
    """Raised when required configuration values are missing."""
    pass


def require(keys: list[str] | None = None) -> None:
    """Validate that required keys are present.

    Parameters
    ----------
    keys:
        List of configuration variable names to check. Defaults to
        ``["PRINTIFY_API_KEY", "OPENAI_API_KEY"]``.

    Raises
    ------
    ConfigError
        If any of the required keys are empty.
    """

    to_check = keys or ["PRINTIFY_API_KEY", "OPENAI_API_KEY"]
    missing = [k for k in to_check if not globals().get(k)]
    if missing:
        joined = ", ".join(missing)
        raise ConfigError(f"Missing required config values: {joined}")

