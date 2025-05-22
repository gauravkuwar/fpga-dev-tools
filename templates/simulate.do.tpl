vsim work.testbench

# Set time units to ns
set units ns

{{CLOCK_WAVE}}

# Add input/output signals automatically
# Assuming top-level testbench is called 'testbench'
add wave -divider Inputs
{{INPUTS}}

add wave -divider Outputs
{{OUTPUTS}}

add wave -divider Other

run -all

# Zoom to fit all waves
wave zoom full