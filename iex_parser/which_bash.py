import shutil
import subprocess
from pathlib import Path

def find_bash_path():
    try:
        # Use the 'which' command to find the path to the Bash interpreter
        bash_path = subprocess.check_output(["which", "bash"]).decode().strip()
        return bash_path
    except subprocess.CalledProcessError:
        return "Bash interpreter not found"


def write_bash_path_to_env_file(env_file_path, bash_path):
    """
    Writes the path to the Bash interpreter to the specified env file if not already present.
    """
    try:
        # Check if the environment file exists
        env_file = Path(env_file_path)
        if env_file.exists():
            # Read existing content
            with open(env_file, 'r') as f:
                existing_content = f.read()
                if f"BASH_PATH={bash_path}" in existing_content:
                    print(f"Bash path already exists in {env_file_path}.")
                    return

        # Append the Bash path to the environment file
        with open(env_file, 'a') as f:
            f.write(f"BASH_PATH={bash_path}\n")
        print(f"Bash path written to {env_file_path}")
    except Exception as e:
        print(f"Error writing to {env_file_path}: {e}")

if __name__ == "__main__":
    write_bash_path_to_env_file("/vagrant/.env", find_bash_path())
    print(f"The path to the Bash interpreter is: {find_bash_path()}")
    