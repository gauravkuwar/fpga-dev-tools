import subprocess
import sys
import os
import re
import shutil
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

from helper.dependency import find_dependents
from helper.signal_parser import parse_ports
from helper.config import MODULES_DIR


def generate_waveform(module_name: str, sim_dir: Path, workdir: Path, tb_file: Path, vcd_file: Path, env: dict):
    # Clean previous build
    if workdir.exists():
        shutil.rmtree(workdir)
    workdir.mkdir()
    if vcd_file.exists():
        vcd_file.unlink()

    # Compile dependencies
    for dep in find_dependents(module_name) + [module_name]:
        dep_src = MODULES_DIR.resolve() / dep / "src" / f"{dep}.vhd"
        if dep_src.exists():
            print(f"Checking Syntax: {dep_src}")
            subprocess.run(["ghdl", "-s", "--workdir=" + str(workdir), str(dep_src.resolve())],
                           check=True, cwd=sim_dir, env=env)
            print(f"Analyzing: {dep_src}")
            subprocess.run(["ghdl", "-a", "--workdir=" + str(workdir), str(dep_src.resolve())],
                           check=True, cwd=sim_dir, env=env)
        else:
            print(f"Warning: dependency not found: {dep_src}")

    print(f"Checking tb Syntax: {tb_file}")
    subprocess.run(["ghdl", "-s", "--workdir=" + str(workdir), str(tb_file.resolve())],
                   check=True, cwd=sim_dir, env=env)
    print(f"Compiling tb: {tb_file}")
    subprocess.run(["ghdl", "-a", "--workdir=" + str(workdir), str(tb_file.resolve())],
                   check=True, cwd=sim_dir, env=env)

    print(f"Elaborating tb: {tb_file}")
    subprocess.run(["ghdl", "-e", "--workdir=" + str(workdir), "testbench"],
                   check=True, cwd=sim_dir, env=env)

    print(f"Simulating tb: {tb_file}")
    subprocess.run(["ghdl", "-r", "--workdir=" + str(workdir), "testbench", f"--vcd={vcd_file.resolve()}"],
                   check=True, cwd=sim_dir, env=env)

    print(f"Waveform written to: {vcd_file}")


def generate_gtkw(module_name: str, src_dir: Path, sim_dir: Path, vcd_file: Path, gtkw_file: Path):
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
                f.write(f"testbench.{sig}\n")
            else:
                match = re.search(r"std_logic_vector\s*\(\s*(\d+)\s+downto\s+(\d+)\s*\)", ports[sig]['type'], re.IGNORECASE)
                high, low = int(match.group(1)), int(match.group(2))
                f.write(f"testbench.{sig}[{high}:{low}]\n")
        f.write("[*end]\n")
    print(f"Layout saved to: {gtkw_file}")


def run_ghdl_sim(module_name: str, open_gtkwave: bool = False):
    module_path = MODULES_DIR / module_name
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

    env = os.environ.copy()
    env["GHDL_OBJ_DIR"] = str(workdir)

    if open_gtkwave and vcd_file.exists() and gtkw_file.exists():
        print("Waveform and layout exist, opening GTKWave...")
    else:
        print("Generating waveform and layout...")
        generate_waveform(module_name, sim_dir, workdir, tb_file, vcd_file, env)
        generate_gtkw(module_name, src_dir, sim_dir, vcd_file, gtkw_file)

    if open_gtkwave:
        subprocess.run(["gtkwave", str(vcd_file), str(gtkw_file)])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/gen_waveform.py <module_name> [-g]")
        sys.exit(1)

    module_name = sys.argv[1]
    open_gtkwave = "-g" in sys.argv[2:]
    run_ghdl_sim(module_name, open_gtkwave=open_gtkwave)
