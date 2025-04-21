import re
from pathlib import Path

# Base paths relative to project root
MODULES_DIR = Path("modules")

component_pattern = re.compile(r"\bcomponent\s+(\w+)", re.IGNORECASE)
entity_pattern = re.compile(r"\bentity\s+work\.(\w+)", re.IGNORECASE)

def find_dependents(module_name, visited=None):
    if visited is None:
        visited = set()

    if module_name in visited:
        return set()  # prevent re-visiting

    dependents = set()
    src_file = MODULES_DIR / module_name / "src" / f"{module_name}.vhd"

    if not src_file.exists():
        print(f"Warning: {src_file} does not exist.")
        return set()

    with open(src_file) as f:
        for line in f:
            # ignore commented lines
            if line.strip().startswith("--"):
                continue

            match_entity = entity_pattern.search(line)
            match_component = component_pattern.search(line)

            if match_entity:
                dependents.add(match_entity.group(1))
            if match_component:
                dependents.add(match_component.group(1))
                
    for dep in list(dependents):
        dependents |= find_dependents(dep, visited)
        
    return dependents

if __name__ == "__main__":
    print(find_dependents("adder_32bit"))