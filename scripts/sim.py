from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent))

from helper.dependency import find_dependents
from helper.config import MODULES_DIR, PROJECT_ROOT, TEMPLATES_DIR
from helper.signal_parser import parse_ports
from helper.util import is_clock_port
from offloader import sync_files, run

def simulate(module_name):
    sim_dir = MODULES_DIR / module_name / "sim"
    template_file = TEMPLATES_DIR / "simulate.do.tpl"
    simulate_do_file = sim_dir / "simulate.do"
    template = template_file.read_text()
    simulate_do_file.write_text(template)
    sync_files([simulate_do_file.relative_to(PROJECT_ROOT)])
    run("vsim -c -do simulate.do", sim_dir.relative_to(PROJECT_ROOT))

    template_file = TEMPLATES_DIR / "waveview.do.tpl"
    template = template_file.read_text()
    waveview_do_file = sim_dir / "waveview.do"

    input_signals_lines = []
    output_signals_lines = []
    all_ports = parse_ports(MODULES_DIR / module_name / "src" / f"{module_name}.vhd")

    for port in all_ports:
        if not is_clock_port(port):
            if all_ports[port]["direction"] == "in":
                input_signals_lines.append(f"add wave /testbench/{port}")
            else:
                output_signals_lines.append(f"add wave /testbench/{port}")

    filled = template.replace("{{INPUTS}}", "\n".join(input_signals_lines)) \
                     .replace("{{OUTPUTS}}", "\n".join(output_signals_lines))
    
    template = template_file.read_text()
    waveview_do_file.write_text(filled)
    sync_files([waveview_do_file.relative_to(PROJECT_ROOT)])

def compile(module_name):
    # generates compile.do file and then runs compile on remote
    sim_dir = MODULES_DIR / module_name / "sim"
    template_file = TEMPLATES_DIR / "compile.do.tpl"
    template = template_file.read_text()

    compile_do_file = sim_dir / "compile.do"
    compile_do_lines = []

    dep_files = [
        compile_do_file.relative_to(PROJECT_ROOT),
        Path(sim_dir / "testbench.vhd").relative_to(PROJECT_ROOT)
        ]

    for dep in find_dependents(module_name) + [module_name]:
        # relative to sim dir
        dep_src = Path("../../..") / "modules" / dep / "src" / f"{dep}.vhd"
        compile_do_lines.append(f"vcom -2008 {dep_src}")
        dep_files.append((MODULES_DIR.relative_to(PROJECT_ROOT) / dep / "src" / f"{dep}.vhd"))

    filled = template.replace("{{DEPS}}", "\n".join(compile_do_lines))
    compile_do_file.write_text(filled)
    sync_files(dep_files)
    run("vsim -c -do compile.do", sim_dir.relative_to(PROJECT_ROOT))


def main():
    if len(sys.argv) < 3:
        print("Usage: python scripts/sim.py <module_name> [--compile] [--simulate]")
        sys.exit(1)

    module_name = sys.argv[1]
    actions = sys.argv[2:]

    valid_action = False

    if "--compile" in actions:
        compile(module_name)
        valid_action = True

    if "--simulate" in actions:
        simulate(module_name)
        valid_action = True

    if not valid_action:
        print("No valid action specified. Use --compile and/or --simulate.")
        sys.exit(1)

if __name__ == "__main__":
    main()