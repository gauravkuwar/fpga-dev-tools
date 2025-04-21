import re
import sys
from pathlib import Path

MODULES_DIR = Path("modules")
TEMPLATE_DIR = Path("templates")

component_pattern = re.compile(r"\bcomponent\s+(\w+)", re.IGNORECASE)
entity_pattern = re.compile(r"\bentity\s+work\.(\w+)", re.IGNORECASE)

def find_dependencies(module_name, visited=None, ordered=None):
    if visited is None:
        visited = set()
    if ordered is None:
        ordered = []

    if module_name in visited:
        return

    visited.add(module_name)
    src_file = MODULES_DIR / module_name / "src" / f"{module_name}.vhd"
    if not src_file.exists():
        print(f"Warning: {src_file} does not exist.")
        return

    with open(src_file) as f:
        for line in f:
            if line.strip().startswith("--"):
                continue
            match_entity = entity_pattern.search(line)
            match_component = component_pattern.search(line)
            dep = match_entity.group(1) if match_entity else (
                  match_component.group(1) if match_component else None)
            if dep:
                find_dependencies(dep, visited, ordered)

    ordered.append(module_name)
    return ordered

def generate_modelsim_files(target_module):
    compile_template_path = TEMPLATE_DIR / "compile.do.tpl"
    run_template_path = TEMPLATE_DIR / "run.do.tpl"
    compile_tpl = compile_template_path.read_text()
    run_tpl = run_template_path.read_text()

    deps = find_dependencies(target_module) or []
    # Always add the target module itself last (if not already added)
    if target_module not in deps:
        deps.append(target_module)

    # Build vcom command list
    compile_lines = [
        f"vcom modules/{mod}/src/{mod}.vhd" for mod in deps
    ]
    compile_lines.append(f"vcom modules/{target_module}/sim/testbench.vhd")

    compile_content = compile_tpl.format(commands="\n".join(compile_lines))
    run_content = run_tpl.format(entity="testbench")

    sim_dir = MODULES_DIR / target_module / "sim"
    sim_dir.mkdir(parents=True, exist_ok=True)

    (sim_dir / "compile.do").write_text(compile_content)
    (sim_dir / "run.do").write_text(run_content)

    print(f"Generated {sim_dir / 'compile.do'}")
    print(f"Generated {sim_dir / 'run.do'}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/generate_modelsim_do.py <module_name>")
        sys.exit(1)
    generate_modelsim_files(sys.argv[1])
