from pathlib import Path
import sys
from helper.generate_qsf_snippet import generate_qsf_snippet

# Base paths relative to project root
TEMPLATE_DIR = Path("templates")
MODULES_DIR = Path("modules")

def create_module(module_name: str, clked: bool, force: bool = False):
    base_path = MODULES_DIR / module_name

    # Check if module already exists
    if base_path.exists() and not force:
        print(f"Error : Module '{module_name}' already exists. Use -f to overwrite.")
        return

    # Recreate directory structure if forcing
    subdirs = ["src", "sim", "qsf"]
    for subdir in subdirs:
        full_path = base_path / subdir
        if force and full_path.exists():
            for file in full_path.iterdir():
                file.unlink()
        full_path.mkdir(parents=True, exist_ok=True)

    # Template files
    templates = {
        "src": TEMPLATE_DIR / ("entity_clk.vhd.tpl" if clked else "entity.vhd.tpl"),
        "qsf": TEMPLATE_DIR / "qsf_snippet.tcl.tpl"
    }

    # Destination files
    destinations = {
        "src": base_path / "src" / f"{module_name}.vhd",
        "qsf": base_path / "qsf" / "qsf_snippet.tcl"
    }

    # Generate files from templates
    for key in templates:
        with open(templates[key], "r") as src, open(destinations[key], "w") as dst:
            content = src.read().replace("{{MODULE_NAME}}", module_name)
            dst.write(content)
            print(f"Created {destinations[key]}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/create_module.py <module_name> [--clk] [-f]")
        sys.exit(1)

    module_name = sys.argv[1]
    clked = "--clk" in sys.argv[2:]
    force = "-f" in sys.argv[2:]
    create_module(module_name, clked, force)
    generate_qsf_snippet(module_name)
