import subprocess
import sys
import os
import re
import shutil
from pathlib import Path
from helper.dependency import find_dependents
from helper.signal_parser import parse_ports

def run_ghdl_sim(module_name: str):
    module_path = Path("modules") / module_name
    src_dir = module_path / "src"
    sim_dir = module_path / "sim"
    tb_file = sim_dir / "testbench.vhd"
    vcd_file = sim_dir / "wave.vcd"
    gtkw_file = sim_dir / "wave.gtkw"
    workdir = (sim_dir / "ghdl_work").resolve()
    workdir.mkdir(exist_ok=True)

    if not tb_file.exists():
        print(f"Error: testbench not found at {tb_file}")
        return

    # Clean previous outputs
    if workdir.exists():
        shutil.rmtree(workdir)
    workdir.mkdir()
    if vcd_file.exists():
        vcd_file.unlink()

    # Set environment and workdir override
    env = os.environ.copy()
    env["GHDL_OBJ_DIR"] = str(workdir)

    # Compile dependencies in correct order
    for dep in find_dependents(module_name) + [module_name]:
        dep_src = Path("modules").resolve() / dep / "src" / f"{dep}.vhd"
        if dep_src.exists():
            print(f"Analyzing: {dep_src}")
            subprocess.run(["ghdl", "-a", "--workdir=" + str(workdir), str(dep_src.resolve())],
                           check=True, cwd=sim_dir, env=env)
        else:
            print(f"Warning: dependency not found: {dep_src}")

    # Compile testbench
    subprocess.run(["ghdl", "-a", "--workdir=" + str(workdir), str(tb_file.resolve())],
                   check=True, cwd=sim_dir, env=env)

    # Elaborate and simulate
    subprocess.run(["ghdl", "-e", "--workdir=" + str(workdir), "testbench"],
                   check=True, cwd=sim_dir, env=env)

    subprocess.run(["ghdl", "-r", "--workdir=" + str(workdir), "testbench", f"--vcd={vcd_file.resolve()}"],
                   check=True, cwd=sim_dir, env=env)

    print(f"Waveform written to: {vcd_file}")

    # Auto-generate .gtkw layout
    entity_file = src_dir / f"{module_name}.vhd"
    ports = parse_ports(entity_file)

    with open(gtkw_file, "w") as f:
        f.write(f"""[*] GTKWave Save File
[dumpfile] {vcd_file.name}
[dumpfile_mtime] 0
[sst_expanded] 1
[signals_width] 200
[sst_width] 200
""")
        f.write("[signals]\n@29\n")
        for sig in ports:
            if ports[sig]['type'] == 'std_logic':
                f.write(f"testbench.{sig}\n")  # unquoted = wave view
            else:
                match = re.search(r"std_logic_vector\s*\(\s*(\d+)\s+downto\s+(\d+)\s*\)", ports[sig]['type'], re.IGNORECASE)
                high, low = int(match.group(1)), int(match.group(2))
                f.write(f"testbench.{sig}[{high}:{low}]\n")  # unquoted = wave view
        f.write("[*end]\n")


    print(f"Layout saved to: {gtkw_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/gen_waveform.py <module_name>")
        sys.exit(1)

    run_ghdl_sim(sys.argv[1])
