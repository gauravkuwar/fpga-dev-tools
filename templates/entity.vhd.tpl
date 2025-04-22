library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- Entity declaration
entity {{MODULE_NAME}} is
  port (
    a      : in  std_logic_vector(7 downto 0);       -- Input operand A
    b      : in  std_logic_vector(7 downto 0);       -- Input operand B
    result : out std_logic_vector(15 downto 0);      -- Output result
  );
end entity;

-- Architecture definition
architecture combinational of {{MODULE_NAME}} is
begin
  -- Structural code here
end architecture;
