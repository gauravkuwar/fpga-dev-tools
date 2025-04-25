library ieee;
use ieee.std_logic_1164.all;

entity testbench is
end entity;

architecture sim of testbench is
  -- signal declarations
  signal a : std_logic;
	signal b : std_logic;
	signal carry_in : std_logic;
	signal result : std_logic;
	signal carry_out : std_logic;
begin
  -- instantiate and test top
  uut: entity work.top
  port map (
    a => a,
		b => b,
		carry_in => carry_in,
		result => result,
		carry_out => carry_out
  );

  -- Stimulus process to apply test cases
  stim_proc: process
  begin
    -- Stimulus process here
    wait;
  end process;
end architecture;
