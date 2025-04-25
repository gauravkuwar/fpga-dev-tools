from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from helper.signal_parser import parse_ports
from helper.config import MODULES_DIR, TEMPLATES_DIR
from helper.util import is_clock_port

def generate_target_wrapper(module_name: str):
    ports = parse_ports(MODULES_DIR / module_name / "src" / f"{module_name}.vhd")
    clk_name = next((p for p in ports if is_clock_port(p)), "clk")
    clk_declared = clk_name in ports

    port_map = []
    flop_decls = []
    flop_logic = []
    sig_decls = []
    port_list = []
    flop_out = []

    if not clk_declared:
        port_list.append(f"{clk_name} : in std_logic")

    for name, prop in ports.items():
        ptype = prop["type"]
        direction = prop["direction"]
        port_list.append(f"{name} : {direction} {ptype}")
        if direction == "out":
            flop_decls.append(f"signal reg_{name} : {ptype};")
            sig_decls.append(f"signal sig_{name} : {ptype};")
            flop_logic.append(f"reg_{name} <= sig_{name};")
            flop_out.append(f"{name} <= reg_{name};")
            port_map.append(f"{name} => sig_{name}")
        elif is_clock_port(name):
            port_map.append(f"{name} => {name}")
        else:
            flop_decls.append(f"signal reg_{name} : {ptype};")
            flop_logic.append(f"reg_{name} <= {name};")
            port_map.append(f"{name} => reg_{name}")


    template_path = TEMPLATES_DIR / "target_wrapper.vhd.tpl"
    with open(template_path, "r") as tpl:
        template = tpl.read()

    wrapper = template.replace("{{MODULE_NAME}}", module_name)
    wrapper = wrapper.replace("{{CLK_NAME}}", clk_name)
    wrapper = wrapper.replace("{{SIG_DECLS}}", "\n\t".join(sig_decls))
    wrapper = wrapper.replace("{{FLOP_DECLS}}", "\n\t".join(flop_decls))
    wrapper = wrapper.replace("{{FLOP_LOGIC}}", "\n\t\t\t".join(flop_logic))
    wrapper = wrapper.replace("{{PORT_MAP}}", ",\n\t\t".join(port_map))
    wrapper = wrapper.replace("{{PORT_LIST}}", ";\n\t\t".join(port_list))
    wrapper = wrapper.replace("{{FLOP_OUT}}", "\n\t".join(flop_out))

    wrapper_path = MODULES_DIR / "target" / "src" / "target.vhd"
    wrapper_path.parent.mkdir(parents=True, exist_ok=True)
    with open(wrapper_path, "w") as f:
        f.write(wrapper)

    print(f"Generated target wrapper for {module_name} at {wrapper_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/helper/generate_target_wrapper.py <module_name>")
        sys.exit(1)

    generate_target_wrapper(sys.argv[1])
