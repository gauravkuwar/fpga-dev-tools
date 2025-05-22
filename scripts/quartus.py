import subprocess
from pathlib import Path
import argparse
import sys
sys.path.append(str(Path(__file__).resolve().parent))

from helper.generate_target_wrapper import generate_target_wrapper
from helper.generate_sdc_constraints import generate_sdc
from helper.dependency import find_dependents
from helper.signal_parser import parse_ports, solve_generic_decl
from helper.config import MODULES_DIR, QUARTUS_DIR, TEMPLATES_DIR, PROJECT_ROOT, FPGA_DEVICE, FPGA_FAMILY, REPORTS_DIR
from helper.generate_report import generate_report, get_table
from helper.util import is_clock_port, get_vector_idx
from offloader import sync_files, run, get_output_files

def update_qsf_file(project_path: Path, top_level: str, mode: str, seed: int = 1):
    template_file = TEMPLATES_DIR / ("component_test.qsf.tpl" if mode == "component" else "normal_project.qsf.tpl")
    template = template_file.read_text()
    qsf_file = project_path / f"{project_path.name}.qsf"
    vhdl_files = []
    dep_files = []
    pin_mappings = []

    if mode == "component":
        ports, generics = parse_ports(MODULES_DIR / top_level / "src" / f"{top_level}.vhd")
        for port in ports:
                if is_clock_port(port):
                    pin_mappings.append(f"set_location_assignment PIN_R8 -to {port}")
                    # pin_mappings.append(f"set_instance_assignment -name VIRTUAL_PIN ON -to {port}")
                    pin_mappings.append(f"set_instance_assignment -name GLOBAL_SIGNAL \"GLOBAL CLOCK\" -to {port}")
                elif ports[port]["type"].lower() == "std_logic":
                    pin_mappings.append(f"set_instance_assignment -name VIRTUAL_PIN ON -to {port}")
                else:
                    for i in range(get_vector_idx(solve_generic_decl(ports[port]["type"], generics))[1]+1):
                        pin_mappings.append(f"set_instance_assignment -name VIRTUAL_PIN ON -to {port}[{i}]")

    for mod in find_dependents(top_level) + [top_level]:
        vhdl_path = Path("..") / ".." / "modules" / mod / "src" / f"{mod}.vhd"
        vhdl_files.append(f'set_global_assignment -name VHDL_FILE "{vhdl_path.as_posix()}"')
        dep_files.append(Path("modules") / mod / "src" / f"{mod}.vhd")

    filled = template.replace("{{FAMILY}}", FPGA_FAMILY)\
                    .replace("{{DEVICE}}", FPGA_DEVICE)\
                    .replace("{{TOP_LEVEL_ENTITY}}", top_level)\
                    .replace("{{PIN_MAPPINGS}}", "\n".join(pin_mappings))\
                    .replace("{{VHDL_FILES}}", "\n".join(vhdl_files))\
                    .replace("{{SEED}}", str(seed))


    qsf_file.write_text(filled)
    print(f"Updated QSF file at {qsf_file}")
    dep_files.append(qsf_file)
    return dep_files

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", help="Name of the Quartus project (folder inside quartus/)")
    parser.add_argument("--target", help="Component/module name to test individually")
    parser.add_argument("--freq", type=float, default=50.0, help="Clock freq in MHz for generated SDC")
    parser.add_argument("--clean", action="store_true", help="Clean Quartus build artifacts")
    parser.add_argument("--syntax", action="store_true", help="Run syntax check only")
    parser.add_argument("--compile", action="store_true", help="Run Quartus compile flow")
    parser.add_argument("--program", action="store_true", help="Program device with .sof")
    parser.add_argument("--update-mif", action="store_true", help="Reassemble after MIF update")
    parser.add_argument("--seed", type=int, default=1, help="Quartus compilation seed")
    args = parser.parse_args()

    if args.target:
        project_path = QUARTUS_DIR.relative_to(PROJECT_ROOT) / "component_test"
    elif args.project:
        project_path = QUARTUS_DIR.relative_to(PROJECT_ROOT) / args.project
    else:
        print("Error: Must provide either --project or --target")
        return
    
    project_name = args.project if args.project else project_path.name
    module_name = args.target if args.target else args.project
    project_path.mkdir(parents=True, exist_ok=True)
    dep_files = []
    
    if args.target:
        print(f"\n[Component Test Mode] Target: {args.target}\n")
        generate_target_wrapper(args.target)
        dep_files += update_qsf_file(project_path, "target", mode="component", seed=args.seed)
    else:
        print(f"\n[Normal Mode] Project: {args.project}\n")
        dep_files += update_qsf_file(project_path, module_name, mode="normal", seed=args.seed)
    
    sdc_fp = generate_sdc(module_name, project_path / f"{project_name}.sdc", args.freq)
    if args.compile or args.syntax:
        dep_files.append(sdc_fp)
        sync_files(dep_files)

    if args.clean:
        run(f"quartus_sh --clean {project_name}", project_path)

    if args.syntax:
        run(f"quartus_map --read_settings_files=on --write_settings_files=off {project_name}", project_path)

    if args.compile:
        run(f"quartus_sh --flow compile {project_name}", project_path)

    if args.program:
        run(f'quartus_pgm --mode JTAG -o "p\\;{project_name}.sof"', project_path)

    if args.update_mif:
        run(f"quartus_asm --read_settings_files=on --write_settings_files=off {project_name}", project_path)
        
    if args.compile:
        get_output_files(project_path)

        report = generate_report(project_name, project_path, module_name, seed=args.seed)
        table = get_table(report)
        print(table)

        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        with open(REPORTS_DIR / f"{module_name}.rpt", "w") as f:
            f.write(table)


if __name__ == "__main__":
    main()