onerror {quit -code 1}
onbreak {quit -code 1}

vsim work.testbench
log -r /*
run -all
quit