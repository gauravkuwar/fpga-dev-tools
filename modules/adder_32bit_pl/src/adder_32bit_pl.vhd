library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- Entity declaration
entity adder_32bit_pl is
  port (
    clk    : in  std_logic;                          -- Clock input
    rst    : in  std_logic;                          -- Synchronous reset
    start  : in std_logic;                           -- Start processing (for pipelining)
    a      : in  std_logic_vector(31 downto 0);       -- Input operand A
    b      : in  std_logic_vector(31 downto 0);       -- Input operand B
    result : out std_logic_vector(31 downto 0);      -- Output result
    done   : out std_logic;                          -- Output flag - pipeline completed 1 result
    busy   : out std_logic                           -- Output flag - pipeline is busy
  );
end entity;

-- Architecture definition
architecture rtl of adder_32bit_pl is
  type pl_reg_t is array (0 to 31) of std_logic_vector(31 downto 0);
  signal a_reg  : pl_reg_t := (others => (others => '0'));
  signal b_reg  : pl_reg_t := (others => (others => '0'));
  signal y_reg  : pl_reg_t := (others => (others => '0'));

  signal carries : std_logic_vector(31 downto 0);
  signal sum_0   : std_logic_vector(31 downto 0);

  -- ensure it doesn't get infered as BRAM
  attribute ramstyle : string;
  attribute ramstyle of a_reg : signal is "logic";
  attribute ramstyle of b_reg : signal is "logic";
begin
  -- Structural code here

  -- stage 0
  ha0 : entity work.half_adder
  port map (
    a         => a_reg(0)(0),
    b         => b_reg(0)(0),
    result    => sum_0(0),
    carry_out => carries(0)
  );

  gen_ripple : for i in 1 to 31 generate
    fa0: entity work.full_adder
    port map(
      a         => a_reg(i)(i),
      b         => a_reg(i)(i),
      carry_in  => carries(i - 1),
      result    => sum_0(i),
      carry_out => carries(i)
    );
  end generate;

  process(clk)
  begin
    if rising_edge(clk) then
      if rst = '1' then
        -- Reset internal state
        result <= (others => '0');
        done   <= '0';
        busy   <= '0';

        for i in 0 to 31 loop
          a_reg(i) <= (others => '0');
          b_reg(i) <= (others => '0');
          y_reg(i) <= (others => '0');
        end loop;
      else
        if start = '1' then
          a_reg(0) <= a;
          b_reg(0) <= b;
        else
          for i in 1 to 31 loop
            a_reg(i) <= a_reg(i-1);
            b_reg(i) <= b_reg(i-1);
          end loop ;
        end if;
      end if;
    end if;
  end process;

  result <= sum_0;
  -- overflow detection would be an extra stage
  -- we can leave that for last to see its affect on fmax
end architecture;
