import sys
from pathlib import Path

MODULES_DIR = Path("modules")

def generate_qsf_snippet(module_name):
    src_file = MODULES_DIR / module_name / "src" / f"{module_name}.vhd"
    if not src_file.exists():
        print(f"Source file not found: {src_file}")
        return

    qsf_path = MODULES_DIR / module_name / "qsf" / "qsf_snippet.tcl"
    qsf_line = f"set_global_assignment -name VHDL_FILE modules/{module_name}/src/{module_name}.vhd\n"
    qsf_path.write_text(f"# Auto-generated QSF snippet for {module_name}\n{qsf_line}")
    print(f"Generated {qsf_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/helper/generate_qsf_snippet.py <module_name>")
        sys.exit(1)

    generate_qsf_snippet(sys.argv[1])
