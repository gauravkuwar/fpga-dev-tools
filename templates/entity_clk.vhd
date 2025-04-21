library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- Entity declaration
entity {{MODULE_NAME}} is
  port (
    clk    : in  std_logic;                          -- Clock input
    rst    : in  std_logic;                          -- Synchronous reset
    start  : in std_logic;                           -- Start processing (for pipelining)
    a      : in  std_logic_vector(7 downto 0);       -- Input operand A
    b      : in  std_logic_vector(7 downto 0);       -- Input operand B
    result : out std_logic_vector(15 downto 0);      -- Output result
    done   : out std_logic;                          -- Output flag - pipeline completed 1 result
    busy   : out std_logic;                          -- Output flag - pipeline is busy
  );
end entity;

-- Architecture definition
architecture rtl of {{MODULE_NAME}} is
begin
  -- Structural code here
  process(clk)
  begin
    if rising_edge(clk) then
      if rst = '1' then
        -- Reset internal state
        result <= (others => '0');
        done   <= '0';
        busy   <= '0';
      else
        -- TODO: RTL code
      end if;
    end if;
  end process;
end architecture;
