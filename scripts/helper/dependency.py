import re
from pathlib import Path

# Base paths relative to project root
MODULES_DIR = Path("modules")

component_pattern = re.compile(r"\bcomponent\s+(\w+)", re.IGNORECASE)
entity_pattern = re.compile(r"\bentity\s+work\.(\w+)", re.IGNORECASE)

def find_dependents(module_name):
    visited = set()
    dependents = []

    def find_dependents_helper(module_name):   
        if module_name in visited: return
        src_file = MODULES_DIR / module_name / "src" / f"{module_name}.vhd"

        if not src_file.exists():
            print(f"Warning: {src_file} does not exist.")
            return []

        with open(src_file) as f:
            for line in f:
                # ignore commented lines
                if line.strip().startswith("--"):
                    continue

                match_entity = entity_pattern.search(line)
                match_component = component_pattern.search(line)

                if match_entity:
                    find_dependents_helper(match_entity.group(1))
                if match_component:
                    find_dependents_helper(match_component.group(1))

        if module_name not in visited:
            visited.add(module_name)
            dependents.append(module_name)

    find_dependents_helper(module_name)
    return dependents[:-1]

if __name__ == "__main__":
    print(find_dependents("adder_32bit"))