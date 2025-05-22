set_global_assignment -name FAMILY "{{FAMILY}}"
set_global_assignment -name DEVICE "{{DEVICE}}"
set_global_assignment -name TOP_LEVEL_ENTITY {{TOP_LEVEL_ENTITY}}
set_global_assignment -name SEED {{SEED}}

{{VHDL_FILES}}

{{PIN_MAPPINGS}}