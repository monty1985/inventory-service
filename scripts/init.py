from pathlib import Path

# Configuration settings
SCRIPT_DIR = Path(__file__).resolve().parent  # Directory of this script
PROJECT_ROOT = SCRIPT_DIR.parent  # Root directory of the project
REQUIREMENTS_FILE = PROJECT_ROOT / "requirements.txt"  # Path to requirements.txt
DEFAULT_PYTHON_VERSION = "python3.12"  # Python interpreter version
VENV_PATH = PROJECT_ROOT / ".venv"  # Path to the virtual environment
LOG_FILE = SCRIPT_DIR / "setup_log.txt"  # Log file for tracking

def log_message(message: str):
    """Write logs to the setup_log.txt file."""
    with open(LOG_FILE, "a") as f:
        f.write(f"{message}\n")
