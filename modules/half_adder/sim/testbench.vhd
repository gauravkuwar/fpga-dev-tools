library ieee;
use ieee.std_logic_1164.all;

entity testbench is
end entity;

architecture sim of testbench is
  -- signal declarations
  signal a : std_logic;
	signal b : std_logic;
	signal result : std_logic;
	signal carry_out : std_logic;
begin
  -- instantiate and test half_adder
  uut: entity work.half_adder
  port map (
    a => a,
		b => b,
		result => result,
		carry_out => carry_out
  );

  -- initialize inputs
  a <= '0';
	b <= '0'; 

  -- Stimulus process to apply test cases
  stim_proc: process
  begin
      -- Stimulus process here
      wait;
  end process;
end architecture;
