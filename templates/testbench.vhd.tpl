library ieee;
use ieee.std_logic_1164.all;

entity testbench is
end entity;

architecture sim of testbench is
  -- signal declarations
  {{SIGNAL_DECLS}}
begin
  -- instantiate and test {{MODULE_NAME}}
  uut: entity work.{{MODULE_NAME}}
  port map (
    {{PORT_MAP}}
  );

  -- Stimulus process to apply test cases
  stim_proc: process
  begin
    -- Stimulus process here
    wait;
  end process;
end architecture;
