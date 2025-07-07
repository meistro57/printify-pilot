#!/usr/bin/env python3
"""Interactive setup for configuring API keys."""
import json
from pathlib import Path

CONFIG_FILE = Path('config.py')

def prompt(key, default=""):
    val = input(f"Enter {key} [{default}]: ").strip()
    return val or default

def main():
    print("=== Printify Pilot setup ===")
    print("This will store your API keys in config.py")

    printify = prompt("Printify API key")
    openai = prompt("OpenAI API key")
    g_service = prompt("Path to Google service account JSON", "path/to/service_account.json")
    g_folder = prompt("Google Drive folder ID", "drive-folder-id")

    lines = [
        "# config.py",
        f"PRINTIFY_API_KEY = \"{printify}\"",
        "BASE_URL = \"https://api.printify.com/v1\"",
        f"OPENAI_API_KEY = \"{openai}\"",
        "",
        "# Optional Google Drive uploader configuration",
        f"GOOGLE_SERVICE_ACCOUNT = \"{g_service}\"",
        f"GOOGLE_DRIVE_FOLDER_ID = \"{g_folder}\"",
        ""
    ]
    CONFIG_FILE.write_text("\n".join(lines), encoding="utf-8")
    print("Configuration written to", CONFIG_FILE)

if __name__ == "__main__":
    main()
