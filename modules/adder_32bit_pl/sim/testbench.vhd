library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity testbench is
end entity;

architecture sim of testbench is
  constant CLK_PERIOD : time := 20 ns; 
  signal done_testing : std_logic := '0';

  -- signal declarations
  signal clk : std_logic;
	signal rst : std_logic;
	signal start : std_logic;
	signal a : std_logic_vector(31 downto 0);
	signal b : std_logic_vector(31 downto 0);
	signal result : std_logic_vector(31 downto 0);
	signal done : std_logic;
	signal busy : std_logic;
begin
  -- Instantiate and test adder_32bit_pl
  uut: entity work.adder_32bit_pl
  port map (
    clk => clk,
		rst => rst,
		start => start,
		a => a,
		b => b,
		result => result,
		done => done,
		busy => busy
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

    start <= '1';
    a     <= std_logic_vector(to_unsigned(4, 32));
    b     <= std_logic_vector(to_unsigned(6, 32));
    wait for CLK_PERIOD * 2;
    start <= '0';

    wait for 40 * CLK_PERIOD;
    -- End simulation
    done_testing <= '1';
    wait;
  end process;
end sim;
