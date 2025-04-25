library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity top is
    port (
      clk : in std_logic;
      a : in std_logic;
      b : in std_logic;
      result : out std_logic;
      carry_out : out std_logic
    );
end entity;

architecture rtl of top is
  signal reg_a, reg_b : std_logic;
  signal sig_result, sig_carry_out : std_logic;
  signal reg_result, reg_carry_out : std_logic;
begin

  process(clk)
  begin
    if rising_edge(clk) then
      reg_a     <= a;
      reg_b     <= b;
      reg_result <= sig_result;
      reg_carry_out <= sig_carry_out;
    end if;
  end process;

  uut: entity work.half_adder
  port map (
    a         => reg_a,
    b         => reg_b,
    result    => sig_result,
    carry_out => sig_carry_out
  );

  result    <= reg_result;
  carry_out <= reg_carry_out;
end architecture;
