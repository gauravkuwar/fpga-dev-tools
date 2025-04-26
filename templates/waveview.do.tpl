# waveview.do

onerror {quit -code 1}
onbreak {quit -code 1}

# Load the WLF file
vsim -view vsim.wlf

# Set time units to ns
set units ns

# Add input/output signals automatically
# Assuming top-level testbench is called 'testbench'
add wave -divider Inputs
{{INPUTS}}

add wave -divider Outputs
{{OUTPUTS}}

# Zoom to fit all waves
wave zoom full