library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity testbench is
end entity;

architecture sim of testbench is
  -- signal declarations
  signal a : std_logic_vector(31 downto 0);
	signal b : std_logic_vector(31 downto 0);
	signal result : std_logic_vector(31 downto 0);
	signal ovf : std_logic;
begin
  -- instantiate and test adder_32bit
  uut: entity work.adder_32bit
  port map (
    a => a,
		b => b,
		result => result,
		ovf => ovf
  );

  -- Stimulus process to apply test cases
  stim_proc: process
  begin
    -- Stimulus process here
    a <= std_logic_vector(to_unsigned(1, 32));
    b <= std_logic_vector(to_unsigned(2, 32));
    wait for 10 ns;

    a <= std_logic_vector(to_unsigned(1, 32));
    b <= std_logic_vector(to_unsigned(2, 32));
    wait for 10 ns;

    a <= std_logic_vector(to_unsigned(1, 32));
    b <= std_logic_vector(to_unsigned(2, 32));
    wait for 10 ns;

    a <= std_logic_vector(to_unsigned(1, 32));
    b <= std_logic_vector(to_unsigned(2, 32));
    wait for 10 ns;

    assert result = std_logic_vector(to_unsigned(3, 32))
    report "Adder result incorrect: expected 3"
    severity error;
    wait;
  end process;
end architecture;
