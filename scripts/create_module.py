from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent))

from helper.config import MODULES_DIR, TEMPLATES_DIR

def create_module(module_name: str, clked: bool, force: bool = False):
    base_path = MODULES_DIR / module_name

    # Check if module already exists
    if base_path.exists() and not force:
        print(f"Error : Module '{module_name}' already exists. Use -f to overwrite.")
        return

    # Recreate directory structure if forcing
    subdirs = ["src", "sim"]
    for subdir in subdirs:
        full_path = base_path / subdir
        if force and full_path.exists():
            for file in full_path.iterdir():
                file.unlink()
        full_path.mkdir(parents=True, exist_ok=True)


    entity_template = TEMPLATES_DIR / ("entity_clk.vhd.tpl" if clked else "entity.vhd.tpl")
    entity_dest     = base_path / "src" / f"{module_name}.vhd"

    with open(entity_template, "r") as src, open(entity_dest, "w") as dst:
        content = src.read().replace("{{MODULE_NAME}}", module_name)
        dst.write(content)
        print(f"Created {entity_dest}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/create_module.py <module_name> [--clk] [-f]")
        sys.exit(1)

    module_name = sys.argv[1]
    clked = "--clk" in sys.argv[2:]
    force = "-f" in sys.argv[2:]
    create_module(module_name, clked, force)