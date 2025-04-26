onerror {quit -code 1}
onbreak {quit -code 1}

vlib work
vmap work work

{{DEPS}}

vcom testbench.vhd
quit
