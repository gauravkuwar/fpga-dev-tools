import re
from pathlib import Path

if __name__ == "__main__":
    import sys
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from helper.config import MODULES_DIR


def parse_ports(vhdl_file):
    ports = []
    generics = []
    final_ports = {}
    final_generics = {}
    entity_started = False
    port_block = False
    generic_block = False
    entity_name = None

    with open(vhdl_file) as f:
        for line in f:
            line = line.strip()

            if line.startswith("--"):
                continue # ignore commented lines
            line = line.split("--")[0].strip()  # Remove inline comments

            if not line:
                continue
            if not entity_started and line.lower().startswith("entity"):
                match = re.search(r'ENTITY\s+(\w+)\s+IS', line, re.IGNORECASE)
                if match:
                    entity_name = match.group(1)

                entity_started = True
            if entity_started and "generic" in line.lower():
                generic_block = True
                line = line[line.lower().find("generic") + 7:]
            if entity_started and "port" in line.lower():
                generic_block = False
                port_block = True
                line = line[line.lower().find("port") + 4:]  # Only once

            if generic_block:
                generics.append(line)
            if port_block:
                if "end entity;" in line.lower() or f"end {entity_name};" in line.lower():
                    break
                ports.append(line)

    generics_str = " ".join(generics)
    generics_str = re.sub(r"^\(\s*|\s*\);?$", "", generics_str.strip())
    generics_clean = re.findall(r"(\w+)\s*:\s*(\w+)\s*:=\s*([^;]+)", generics_str, re.IGNORECASE)

    for name, var_type, default_value in generics_clean:
        final_generics[name] = {
            "type": var_type,
            "default": default_value.strip() if default_value else None
        }

    ports_str = " ".join(ports)
    ports_str = re.sub(r"^\(\s*|\s*\);?$", "", ports_str.strip())
    ports_clean = re.findall(r"([\w,\s]+):\s*(in|out|inout)\s+([^;]+)", ports_str, re.IGNORECASE)

    for name, direction, port_type in ports_clean:
        # TODO: remove is it doesn matter 
        # for name in [n.strip() for n in names.split(",")]:
        final_ports[name.strip()] = {
            "type": port_type.split(":=")[0].strip(),
            "direction": direction.lower()
        }

    return final_ports, final_generics

def eval_expr(expr):
    if not re.match(r'^[0-9+\-*/() ]+$', expr):
        raise ValueError(f"Unsafe expression detected: {expr}")
    return eval(expr)

def parse_std_logic_vector_bounds(type_string):
    # Match patterns like (expr downto 0) or (expr to 0)
    pattern = re.compile(r'(\w+)\s*\(\s*([0-9+\-*/() ]+)\s*(downto|to)\s*([0-9+\-*/() ]+)\s*\)', re.IGNORECASE)
    match = pattern.search(type_string)

    if match:
        port_type = match.group(1).strip()
        left_expr = match.group(2).strip()
        direction = match.group(3).lower()
        right_expr = match.group(4).strip()
        return port_type, left_expr, direction, right_expr
    else:
        return None, None, None, None
    
def solve_generic_decl(port_type, generics):
    for generic in generics:
        port_type = re.sub(rf'\b{generic}\b', str(generics[generic]["default"]), port_type)
    
    port_type, left_expr, direction, right_expr = parse_std_logic_vector_bounds(port_type)
    return f"{port_type}({eval_expr(left_expr)} {direction} {eval_expr(right_expr)})"

if __name__ == "__main__":
    from pprint import pprint
    if len(sys.argv) < 2:
        print("Usage: python parse_ports.py <module_name>")
        sys.exit(1)

    module_name = sys.argv[1]
    src_file = MODULES_DIR / module_name / "src" / f"{module_name}.vhd"    

    # Example usage
    ports, generics = parse_ports(src_file)

    print("generics")
    pprint(generics)
    print()

    print("ports")
    pprint(ports)
    # print("Solve generic:", solve_generic_decl(ports["a"]["type"], generics))

