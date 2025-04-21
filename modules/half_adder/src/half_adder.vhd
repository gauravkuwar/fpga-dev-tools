library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- Entity declaration
entity half_adder is
  port (
    a           : in  std_logic;       -- Input operand A
    b           : in  std_logic;       -- Input operand B
    result      : out std_logic;       -- Output result
    carry_out   : out std_logic
  );
end entity;

-- Architecture definition
architecture combinational of half_adder is
begin
  result    <= a xor b;
  carry_out <= a and b;
end architecture;
