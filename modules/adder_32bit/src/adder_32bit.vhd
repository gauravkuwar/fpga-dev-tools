-- Ripple Carry Adder 32-bit 
-- with Carry Chains (FPGA specific hardware optimization)

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- Entity declaration
entity adder_32bit is
  port (
    a      : in  std_logic_vector(31 downto 0);       -- Input operand A
    b      : in  std_logic_vector(31 downto 0);       -- Input operand B
    result : out std_logic_vector(31 downto 0);       -- Output result
    ovf    : out std_logic;
  );
end entity;

-- Architecture definition
architecture combinational of adder_32bit is
  signal carries : std_logic(31 downto 0);
  signal sum_0   : std_logic(31 downto 0);
begin
  -- uses carry chain hardware
  ha0 : entity work.half_adder
  port map (
    a         => a,
    b         => b,
    result    => sum_0,
    carry_out => carry_0
  );

  gen_ripple : for i in 1 to 31 generate
    fa0: entity work.full_adder
    port map(
      a         => a(i),
      b         => b(i),
      carry_in  => carries(i - 1),
      result    => sum_0(i),
      carry_out => carries(i)
    );
  end generate; 

  result <= sum_0;

  -- Overflow detection for signed addition:
  -- Should not slow down addition computation, since it happens in parallel
  -- a(31) = b(31) and result(3115) /= a(31)
  ovf <= not (a(31) xor b(31)) and (a(31) xor sum_0(7));
end architecture;
