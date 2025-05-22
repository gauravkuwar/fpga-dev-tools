set_global_assignment -name FAMILY "{{FAMILY}}"
set_global_assignment -name DEVICE "{{DEVICE}}"
set_global_assignment -name TOP_LEVEL_ENTITY {{TOP_LEVEL_ENTITY}}
set_global_assignment -name SEED {{SEED}}


{{VHDL_FILES}}


# PIN MAPPINGS
set_location_assignment PIN_J15 -to key[0]
set_location_assignment PIN_E1 -to key[1]

set_location_assignment PIN_R8 -to clk
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to clk

set_location_assignment PIN_A15 -to led[0]
set_location_assignment PIN_A13 -to led[1]
set_location_assignment PIN_B13 -to led[2]
set_location_assignment PIN_A11 -to led[3]
set_location_assignment PIN_D1  -to led[4]
set_location_assignment PIN_F3  -to led[5]
set_location_assignment PIN_B1  -to led[6]
set_location_assignment PIN_L3  -to led[7]