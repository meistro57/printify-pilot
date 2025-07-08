

"""Central configuration loaded from environment variables."""

from __future__ import annotations

import os

PRINTIFY_API_KEY = os.getenv("PRINTIFY_API_KEY", "")
BASE_URL = os.getenv("BASE_URL", "https://api.printify.com/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "openai api key")

# Optional Google Drive uploader configuration
GOOGLE_SERVICE_ACCOUNT = os.getenv("GOOGLE_SERVICE_ACCOUNT", "path/to/service_account.json")
GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "drive-folder-id")


def require(keys: list[str] | None = None) -> None:
    """Validate that required keys are present.

    Parameters
    ----------
    keys:
        List of configuration variable names to check. Defaults to
        ``["PRINTIFY_API_KEY", "OPENAI_API_KEY"]``.

    Raises
    ------
    ValueError
        If any of the required keys are empty.
    """

    to_check = keys or ["PRINTIFY_API_KEY", "OPENAI_API_KEY"]
    missing = [k for k in to_check if not globals().get(k)]
    if missing:
        joined = ", ".join(missing)
        raise ValueError(f"Missing required config values: {joined}")

