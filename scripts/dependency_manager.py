import subprocess
import sys
from pathlib import Path

# Hardcoded Configuration
SCRIPT_DIR = Path(__file__).resolve().parent  # Directory of this script
PROJECT_ROOT = SCRIPT_DIR.parent  # Root directory of the project
REQUIREMENTS_FILE = PROJECT_ROOT / "requirements.txt"  # Path to requirements.txt
DEFAULT_PYTHON_VERSION = "python3.12"  # Python interpreter version
VENV_PATH = PROJECT_ROOT / ".venv"  # Path to the virtual environment
LOG_FILE = SCRIPT_DIR / "setup_log.txt"  # Log file for tracking actions

def log_message(message: str):
    """Write logs to the setup_log.txt file."""
    with open(LOG_FILE, "a") as f:
        f.write(f"{message}\n")

def create_virtualenv():
    """Create a virtual environment using the specified Python version."""
    if VENV_PATH.exists():
        print("Virtual environment already exists.", flush=True)
        return

    print(f"Creating virtual environment with {DEFAULT_PYTHON_VERSION}...", flush=True)
    try:
        result = subprocess.run([DEFAULT_PYTHON_VERSION, "-m", "venv", str(VENV_PATH)])
        result.check_returncode()
    except FileNotFoundError:
        print(f"Error: {DEFAULT_PYTHON_VERSION} not found. Please install it.", flush=True)
        sys.exit(1)
    except subprocess.CalledProcessError:
        log_message("Failed to create virtual environment.")
        print("Error: Failed to create virtual environment.", flush=True)
        sys.exit(1)

    print(f"Virtual environment created at {VENV_PATH}", flush=True)
    log_message("Virtual environment created.")

def install_dependencies():
    """Install all dependencies from requirements.txt."""
    if not VENV_PATH.exists():
        print("Virtual environment not found. Please create one first.", flush=True)
        sys.exit(1)

    print("Installing dependencies from requirements.txt...", flush=True)
    result = subprocess.run([f"{VENV_PATH}/bin/pip", "install", "-r", str(REQUIREMENTS_FILE)])
    if result.returncode == 0:
        print("Dependencies installed successfully.", flush=True)
    else:
        print("Failed to install dependencies.", flush=True)

def add_dependency(dependency: str):
    """Add a new dependency, install it, and update requirements.txt."""
    # Check if the dependency is already listed
    with open(REQUIREMENTS_FILE, "r") as f:
        if dependency in f.read():
            print(f"'{dependency}' is already listed in requirements.txt.", flush=True)
            return

    # Add the dependency to requirements.txt
    with open(REQUIREMENTS_FILE, "a") as f:
        f.write(f"{dependency}\n")
    print(f"Added '{dependency}' to requirements.txt.", flush=True)

    # Install the dependency
    print(f"Installing '{dependency}'...", flush=True)
    result = subprocess.run([f"{VENV_PATH}/bin/pip", "install", dependency])
    if result.returncode == 0:
        print(f"'{dependency}' installed successfully.", flush=True)
        log_message(f"Added and installed '{dependency}'.")
    else:
        print(f"Failed to install '{dependency}'.", flush=True)

def list_dependencies():
    """List installed dependencies in the virtual environment."""
    print("Currently installed dependencies:", flush=True)
    subprocess.run([f"{VENV_PATH}/bin/pip", "list"])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python dependency_manager.py <command> [dependency]", flush=True)
        sys.exit(1)

    command = sys.argv[1]

    if command == "create-venv":
        create_virtualenv()
    elif command == "install":
        install_dependencies()
    elif command == "list":
        list_dependencies()
    elif command == "add" and len(sys.argv) == 3:
        add_dependency(sys.argv[2])
    else:
        print("Invalid command or missing dependency.", flush=True)
