from pathlib import Path

PROJECT_NAME = "fpga_dev_tools"

# Resolve project root from this file's location
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Remote config - offloader
REMOTE_HOST     = "Admin@thinkpad.local"
SSH_KEY_PATH    = Path.home() / ".ssh" / "id_ed25519"
REMOTE_DIR      = Path("offload_server") / PROJECT_NAME

# Paths (always anchored to project root)
SCRIPTS_DIR         = PROJECT_ROOT / "scripts"
MODULES_DIR         = PROJECT_ROOT / "modules"
QUARTUS_DIR         = PROJECT_ROOT / "quartus"
TEMPLATES_DIR       = PROJECT_ROOT / "templates"
OFFLOADER_HASH_FILE = PROJECT_ROOT / ".filehashes.json"
REPORTS_DIR         = PROJECT_ROOT / "reports"

# DE0-Nano
FPGA_FAMILY     = "Cyclone IV E"
FPGA_DEVICE     = "EP4CE22F17C6"

# DE10-Nano
# FPGA_FAMILY     = "Cyclone V"
# FPGA_DEVICE     = "5CSEBA6U23I7"