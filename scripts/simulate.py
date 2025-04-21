import subprocess
import sys
from pathlib import Path

def simulate(module_name):
    sim_dir = Path("modules") / module_name / "sim"
    compile_do = sim_dir / "compile.do"
    run_do = sim_dir / "run.do"

    if not compile_do.exists() or not run_do.exists():
        print("Error: compile.do or run.do not found. Generate them first.")
        return

    subprocess.run(["vsim", "-c", "-do", str(compile_do)], cwd=sim_dir)
    subprocess.run(["vsim", "-c", "-do", str(run_do)], cwd=sim_dir)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/simulate.py <module_name>")
        sys.exit(1)

    simulate(sys.argv[1])
