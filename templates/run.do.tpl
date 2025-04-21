vsim -gui work.{entity}
add wave -position end sim:/{entity}/*
run 100 ns
