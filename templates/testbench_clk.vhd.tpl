library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity testbench is
end entity;

architecture sim of testbench is
  constant CLK_PERIOD : time := 20 ns; 
  signal done_testing : std_logic := '0';

  -- signal declarations
  {{SIGNAL_DECLS}}
begin
  -- Instantiate and test {{MODULE_NAME}}
  uut: entity work.{{MODULE_NAME}}
  port map (
    {{PORT_MAP}}
  );

  -- Clock generation process
  clk_process : process
  begin
    while done_testing = '0' loop
        clk <= '1'; wait for CLK_PERIOD / 2;
        clk <= '0'; wait for CLK_PERIOD / 2;
    end loop;
    wait;
  end process;

  -- Stimulus process
  stim_proc : process
  begin
    -- Wait for a few cycles
    wait for 2 * CLK_PERIOD;

    -- TODO: apply inputs here

    -- End simulation
    done_testing <= '1';
    wait;
  end process;
end sim;
