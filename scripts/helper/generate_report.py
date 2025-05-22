from tabulate import tabulate
import os
import re

def parse_helper(line):
    a, b = line.split(":")[-1].split("/")
    count = int(a.replace(",", ""))
    total = int(b.split("(")[0].replace(",", ""))
    percent = round(count / total, 5)
    return count, total, percent

def generate_report(project_name, project_path, top_entity, seed=1):
    fit_rpt_file = os.path.join(project_path, f"{project_name}.fit.rpt")
    fit_summary_file = os.path.join(project_path, f"{project_name}.fit.summary")
    sta_rpt_file = os.path.join(project_path, f"{project_name}.sta.rpt")

    result = {
        "Top Level Entity": top_entity,
        "Initial Fitter Seed": seed
    }

    # Parse Fitter Resource Usage Report
    include = {
        # 'Oscillator blocks', 
        # 'Clock pins', 
        'Total block memory implementation bits',
        'I/O pins', 
        'Total registers*', 
        # 'Total LABs:  partially or completely used', 
        'M9Ks', 
        # 'ASMI blocks', 
        # 'Dedicated input pins', 
        'Embedded Multiplier 9-bit elements', 
        'Total logic elements', 
        # 'JTAGs', 
        # 'PLLs', 
        'Total block memory bits', 
        'Dedicated logic registers', 
        # 'CRC blocks', 
        'Global clocks', 
        # 'Impedance control blocks', 
        'I/O registers',
        }
    
    usage_block = False
    div_count = 0

    with open(fit_rpt_file, 'r', encoding="latin-1") as f:
        for line in f:
            if not usage_block and "; Fitter Resource Usage Summary" in line:
                usage_block = True
            if usage_block:
                match = re.match(r";\s*(.+?)\s*;\s*([\d,]+)\s*/\s*([\d,]+)\s*\(", line)
                if match:
                    # print(line)
                    label, used, total = match.groups()
                    label = label.strip().lstrip("-").strip()
                    used, total = int(used.replace(",", "")), int(total.replace(",", ""))
                    if label in include:
                        result[label] = f"{used} / {total} ({used / total:.5f})"

                if re.match(r"^\+\s*[-+]+\s*\+$", line):
                    div_count += 1
                if div_count > 2:
                    usage_block = False

    # Parse Fmax from STA report
    fmax_list = []
    with open(sta_rpt_file) as f:
        lines = f.readlines()

    for i in range(len(lines)):
        line = lines[i]

        if "Restricted Fmax" in line:
            timing_cat = lines[i-2].replace(";", "").split("Model")[0].strip()
            parts = []
            for part in lines[i+2].split(";"):
                if "hz" in part.lower():
                    parts.append(part.strip())

            result[f"{timing_cat} - Fmax"] = parts[0]
            result[f"{timing_cat} - Restricted Fmax"] = parts[1]

    return result
    
def get_table(result):
    table = [(k, v) for k, v in result.items()]
    return tabulate(table, headers=["Metric", "Value"], tablefmt="grid")

if __name__ == "__main__":
    result = generate_report("component_test", "quartus/component_test", "test")
    print(get_table(result))
