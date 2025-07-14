"""Utility functions for XSS Blaster."""

import os
from importlib.resources import files
from pathlib import Path


def get_payload_file_path(custom_file: str | None = None) -> str | None:
    """
    Get the path to the payload file in the following order of preference:
    1. Custom file specified by user
    2. User config file at ~/.config/xssblaster/my-xss.txt
    3. Package bundled file
    4. None (will use built-in payloads)

    Args:
        custom_file: Path to custom payload file specified by user

    Returns:
        Path to payload file or None if no file found
    """
    # 1. Custom file specified by user
    if custom_file and os.path.isfile(custom_file):
        return custom_file

    # 2. User config file
    config_dir = Path.home() / ".config" / "xssblaster"
    user_payload_file = config_dir / "my-xss.txt"
    if user_payload_file.exists():
        return str(user_payload_file)

    # 3. Package bundled file
    try:
        # Try to get the bundled file from the package
        package_files = files("xssblaster")
        payload_file = package_files / "my-xss.txt"
        if payload_file.is_file():
            return str(payload_file)
    except (ImportError, FileNotFoundError, AttributeError):
        pass

    # 4. Fallback - no file found, will use built-in payloads
    return None


def load_payloads_from_file(file_path: str) -> list[str]:
    """
    Load payloads from a file.

    Args:
        file_path: Path to the payload file

    Returns:
        List of payload strings
    """
    try:
        with open(file_path, encoding="utf-8") as f:
            payloads = [
                line.strip()
                for line in f
                if line.strip() and not line.strip().startswith("#")
            ]
        return payloads
    except (OSError, FileNotFoundError):
        return []


def ensure_config_dir() -> Path:
    """
    Ensure the user config directory exists and return its path.

    Returns:
        Path to the config directory
    """
    config_dir = Path.home() / ".config" / "xssblaster"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def copy_default_payload_file() -> bool:
    """
    Copy the default payload file to user config directory if it doesn't exist.

    Returns:
        True if file was copied or already exists, False if failed
    """
    config_dir = ensure_config_dir()
    user_payload_file = config_dir / "my-xss.txt"

    # If user file already exists, don't overwrite
    if user_payload_file.exists():
        return True

    try:
        # Try to copy from package
        package_files = files("xssblaster")
        payload_file = package_files / "my-xss.txt"
        if payload_file.is_file():
            # Read from package and write to user config
            content = payload_file.read_text(encoding="utf-8")
            user_payload_file.write_text(content, encoding="utf-8")
            return True
    except (OSError, ImportError, FileNotFoundError, AttributeError):
        pass

    return False
