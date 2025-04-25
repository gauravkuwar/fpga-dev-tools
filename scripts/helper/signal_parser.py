import re
from pathlib import Path

if __name__ == "__main__":
    import sys
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from helper.config import MODULES_DIR


def parse_ports(vhdl_file):
    ports = []
    final_ports = {}
    entity_started = False
    port_block = False

    with open(vhdl_file) as f:
        for line in f:
            line = line.strip().lower()

            if line.startswith("--"):
                continue # ignore commented lines
            line = line.split("--")[0].strip()  # Remove inline comments

            if not line:
                continue
            if not entity_started and line.startswith("entity"):
                entity_started = True
            if entity_started and "port" in line.lower():
                port_block = True
                line = line[line.lower().find("port") + 4:]  # Only once
            if port_block:
                if "end entity;" in line:
                    break
                ports.append(line)

    ports_str = " ".join(ports)
    ports_str = re.sub(r"^\(\s*|\s*\);?$", "", ports_str.strip())
    ports_clean = re.findall(r"([\w,\s]+):\s*(in|out)\s+([^;]+)", ports_str, re.IGNORECASE)

    for names, direction, port_type in ports_clean:
        for name in [n.strip() for n in names.split(",")]:
            final_ports[name] = {
                "type": port_type.strip(),
                "direction": direction.lower()
            }

    return final_ports

if __name__ == "__main__":
    module_name = "array_mul_8x8_pl"
    src_file = MODULES_DIR / module_name / "src" / f"{module_name}.vhd"

    # Example usage:
    final_ports = parse_ports(src_file)
    print("Ports:", final_ports)
