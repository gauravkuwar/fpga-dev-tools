# FPGA Dev Tools

This repo provides a streamlined FPGA development workflow using **Quartus**, **GHDL**, and **GTKWave**, with automation scripts to accelerate iteration.

It is tailored for a split setup where most development is done on **macOS**, and **Quartus commands are offloaded to a Windows machine**.

The idea is to use this as a startup template.

## Modular Structure

Each FPGA component is organized as a module containing:
- The VHDL entity
- A corresponding testbench, and its sim files

## Scripts Overview

| Script            | Purpose |
|-------------------|---------|
| `create_module.py` | Scaffold a new module with template VHDL code |
| `create_tb.py`     | Scaffold a testbench from an existing entity with pre-defined signals|
| `gen_waveform.py`  | Run GHDL simulation and launch GTKWave with preloaded signals |
| `offloader.py`     | Helper script to offload Quartus commands to Windows |
| `quartus.py`       | Abstracts Quartus execution and offloading, and report results |

## Test Modes (in `quartus.py`)

- **Component Testing**: Generates a wrapper to test a single component (especially useful for timing analysis of combinational logic.)
- **Top-Level Testing**: Runs Quartus flow on the main top-level module.

## Automation Features (in `quartus.py`)

- Auto-generates `.sdc` and `.qsf` files
- `.qsf` includes only VHDL files required for the given top level (fast compilation)
- Targets a specific FPGA family/device (customizable via template)
- Parses Quartus output to extract Fmax, resource usage, and key metrics and generates report.
