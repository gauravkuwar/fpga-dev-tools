from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from helper.signal_parser import parse_ports, solve_generic_decl
from helper.config import MODULES_DIR
from helper.util import is_clock_port, get_vector_idx


def generate_sdc(module_name: str, sdc_path: str, freq: float = 50.0):
    ports, generics = parse_ports(MODULES_DIR / module_name / "src" / f"{module_name}.vhd")
    clk_name = next((p for p in ports if is_clock_port(p)), "clk")

    input_ports = [p for p, props in ports.items() if props["direction"] == "in" and p != clk_name]
    output_ports = [p for p, props in ports.items() if props["direction"] == "out"]

    lines = [
        f"create_clock -name {clk_name} -period \"{freq:.3f} MHz\" [get_ports {clk_name}]",
        "derive_clock_uncertainty"
    ]

    for port in input_ports:
        if ports[port]["type"].lower() == "std_logic":
            lines.append(f"set_input_delay 0 -clock {clk_name} [get_ports {port}]")
        else:
            for i in range(get_vector_idx(solve_generic_decl(ports[port]["type"], generics))[1]+1):
                lines.append(f"set_input_delay 0 -clock {clk_name} [get_ports {port}[{i}]]")

    for port in output_ports:
        if ports[port]["type"].lower() == "std_logic":
            lines.append(f"set_output_delay 0 -clock {clk_name} [get_ports {port}]")
        else:
            for i in range(get_vector_idx(solve_generic_decl(ports[port]["type"], generics))[1]+1):
                lines.append(f"set_output_delay 0 -clock {clk_name} [get_ports {port}[{i}]]")

    with open(sdc_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Generated SDC file for {module_name} at {sdc_path}")
    return sdc_path

if __name__ == "__main__":
    import sys
    if not (2 <= len(sys.argv) <= 3):
        print("Usage: python scripts/helper/generate_sdc_constraints.py <module_name> [freq]")
        sys.exit(1)

    module_name = sys.argv[1]
    freq = float(sys.argv[2]) if len(sys.argv) == 3 else 50.0
    generate_sdc(module_name, freq)