vsim -gui work.{entity}
log -r /*
add wave -position end sim:/{entity}/*
run 1 ms
write list wave_out.wlf