import os
import subprocess
import sys
from pathlib import Path

# Configuration
SCRIPT_DIR = Path(__file__).resolve().parent  # Directory of the init.py script
PROJECT_ROOT = SCRIPT_DIR.parent  # Parent directory (project root)
REQUIREMENTS_FILE = PROJECT_ROOT / "requirements.txt"  # Path to requirements.txt
DEFAULT_PYTHON_VERSION = "python3.12"  # Python interpreter to use
LOG_FILE = PROJECT_ROOT / "setup_log.txt"  # Log file in project root

# Track dependency status
dependency_status = {}

def log_message(message):
    """Log messages to both console and log file."""
    print(message)
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")

def run_command(command):
    """Run a shell command and log output."""
    try:
        result = subprocess.run(
            command, shell=True, text=True, capture_output=True
        )
        if result.returncode != 0:
            log_message(f"Error: {command} failed with:\n{result.stderr}")
            return False
        log_message(f"Success: {command} completed successfully.")
        return True
    except Exception as e:
        log_message(f"Exception while running '{command}': {str(e)}")
        return False

def prompt_for_env_name():
    """Prompt the user for a new virtual environment name if it already exists."""
    while True:
        env_name = input("Enter the name for the virtual environment: ").strip()
        venv_path = PROJECT_ROOT / env_name
        if not venv_path.exists():
            return env_name
        print(f"Environment '{env_name}' already exists. Please choose a different name.")

def create_virtualenv(env_name):
    """Create the virtual environment."""
    venv_path = PROJECT_ROOT / env_name
    log_message(f"Creating virtual environment '{env_name}' using {DEFAULT_PYTHON_VERSION}...")
    if run_command(f"{DEFAULT_PYTHON_VERSION} -m venv {venv_path}"):
        log_message(f"Virtual environment '{env_name}' created successfully.")
        return venv_path
    else:
        sys.exit(f"Failed to create virtual environment '{env_name}'.")

def ensure_path(venv_bin):
    """Ensure the virtual environment's bin folder is in PATH."""
    venv_bin_path = str(venv_bin.resolve())
    if venv_bin_path not in os.environ["PATH"]:
        log_message(f"Adding '{venv_bin_path}' to PATH...")
        os.environ["PATH"] = f"{venv_bin_path}:{os.environ['PATH']}"

def get_pip_command(venv_bin):
    """Get the correct pip command."""
    pip_cmd = venv_bin / "pip3" if (venv_bin / "pip3").exists() else venv_bin / "pip"
    return str(pip_cmd)

def install_dependencies(pip_cmd):
    """Install dependencies from requirements.txt."""
    log_message(f"Reading dependencies from {REQUIREMENTS_FILE}...")
    try:
        with open(REQUIREMENTS_FILE) as f:
            dependencies = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            log_message(f"Found dependencies: {dependencies}")
    except FileNotFoundError:
        sys.exit(f"Error: {REQUIREMENTS_FILE} not found.")

    if not dependencies:
        log_message("No dependencies found in the requirements.txt file.")
        return

    for dependency in dependencies:
        log_message(f"Installing {dependency}...")
        if run_command(f"{pip_cmd} install {dependency}"):
            dependency_status[dependency] = "Installed"
        else:
            log_message(f"Retrying installation for {dependency}...")
            if run_command(f"{pip_cmd} install {dependency} --no-cache-dir"):
                dependency_status[dependency] = "Installed"
            else:
                dependency_status[dependency] = "Failed"

def verify_dependencies(pip_cmd):
    """Verify that all dependencies are installed."""
    log_message("Verifying installed dependencies...")
    for dependency in dependency_status.keys():
        dep_name = dependency.split("[")[0]
        result = subprocess.run(
            f"{pip_cmd} show {dep_name}", shell=True, text=True, capture_output=True
        )
        if result.returncode == 0:
            dependency_status[dependency] = "Installed"
        else:
            dependency_status[dependency] = "Failed"

def print_summary(env_name):
    """Print a summary of the setup."""
    log_message("\n==== Environment Setup Summary ====")
    log_message(f"Environment Name: {env_name}")
    log_message("Dependency Status:")
    if not dependency_status:
        log_message("  No dependencies found or installed.")
    for dependency, status in dependency_status.items():
        log_message(f"  - {dependency}: {status}")
    log_message("==================================\n")

def print_instructions(env_name):
    """Print instructions for activating the environment and running the app."""
    venv_path = PROJECT_ROOT / env_name
    log_message("\nSetup complete! To start using the virtual environment:")
    if os.name == "nt":
        log_message(f"   {env_name}\\Scripts\\activate")
    else:
        log_message(f"   source {venv_path}/bin/activate")
    log_message("After activation, you can run your application with:")
    log_message("   uvicorn src.main.controllers:app --host 0.0.0.0 --port 8000 --reload\n")

def main():
    """Main function to initialize the environment."""
    try:
        log_message("Initializing development environment...")
        env_name = prompt_for_env_name()
        venv_path = create_virtualenv(env_name)
        ensure_path(venv_path / VENV_BIN)
        pip_cmd = get_pip_command(venv_path / VENV_BIN)
        install_dependencies(pip_cmd)
        verify_dependencies(pip_cmd)
        print_summary(env_name)
        print_instructions(env_name)
    except Exception as e:
        log_message(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
