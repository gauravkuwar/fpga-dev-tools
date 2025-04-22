library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- Entity declaration
entity full_adder is
  port (
    a           : in  std_logic;       -- Input operand A
    b           : in  std_logic;       -- Input operand B
    carry_in    : in  std_logic;
    result      : out std_logic;       -- Output result
    carry_out   : out std_logic
  );
end entity;

-- Architecture definition
architecture combinational of full_adder is
  signal sum_0    : std_logic;
  signal carry_0  : std_logic;
  signal carry_1  : std_logic;
begin
  ha0 : entity work.half_adder
  port map (
    a         => a,
    b         => b,
    result    => sum_0,
    carry_out => carry_0
  );

  ha1 : entity work.half_adder
  port map (
    a         => sum_0,
    b         => carry_in,
    result    => result,
    carry_out => carry_1
  );

  carry_out <= carry_0 or carry_1;
end architecture;
