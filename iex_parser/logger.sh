#!/vagrant/.env BASH_PATH
# Get the absolute path to the utils directory
UTILS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Add the utils directory to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:${UTILS_DIR}"
# Run the Python script using the logger module and pass the message as an argument
python3 -m logger "$1"
