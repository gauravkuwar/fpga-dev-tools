from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent))

from helper.signal_parser import parse_ports
from helper.config import MODULES_DIR, TEMPLATES_DIR

def is_clock_port(port):
    return port.lower() in ['clk', 'clock']

def is_clocked(ports):
    return any(is_clock_port(p) for p in ports)

def gen_signal_declarations(ports):
    decls = []
    for p in ports:
        decls.append(f"signal {p} : {ports[p]['type']};")
    return "\n\t".join(decls)

def gen_port_map(ports):
    return ",\n\t\t".join([f"{p} => {p}" for p in ports])

def create_tb(module_name: str, force: bool = False):
    entity_path = MODULES_DIR / module_name / "src" / f"{module_name}.vhd"
    if not entity_path.exists():
        print(f"Error: Entity file '{entity_path}' not found.")
        return

    output_file = MODULES_DIR / module_name / "sim" / "testbench.vhd"
    if output_file.exists() and not force:
        print(f"Error: Testbench already exists at '{output_file}'. Use -f to overwrite.")
        return

    ports, generics = parse_ports(entity_path)
    clked = is_clocked(ports)

    generic_list = []
    generic_map = []
    for generic, prop in generics.items():
        generic_list.append(f"constant {generic} : {prop["type"]} := {prop["default"]};")
        generic_map.append(f"{generic} => {generic}")

    if generic_map:
        generic_map_str = (
            "\n\tgeneric map (\n\t\t" +
            ",\n\t\t".join(generic_map) +
            "\n\t)"
        )
    else:
        generic_map_str = ""


    template_file = TEMPLATES_DIR / ("testbench_clk.vhd.tpl" if clked else "testbench.vhd.tpl")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(template_file, "r") as template:
        content = template.read()
        content = content.replace("{{MODULE_NAME}}", module_name)
        content = content.replace("{{SIGNAL_DECLS}}", gen_signal_declarations(ports))
        content = content.replace("{{PORT_MAP}}", gen_port_map(ports))
        content = content.replace("{{GENERIC_LIST}}", "\n\t".join(generic_list))
        content = content.replace("{{GENERIC_MAP}}", generic_map_str)

    with open(output_file, "w") as tb:
        tb.write(content)

    print(f"Testbench created at: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/create_tb.py <module_name> [-f]")
        sys.exit(1)

    module_name = sys.argv[1]
    force = "-f" in sys.argv[2:]
    create_tb(module_name, force=force)