library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity target is
    port (
        a : in std_logic_vector(7 downto 0);
		b : in std_logic_vector(7 downto 0);
		start : in std_logic;
		clk : in std_logic;
		y : out std_logic_vector(15 downto 0);
		y_valid : out std_logic
    );
end entity;

architecture rtl of target is
    signal sig_y : std_logic_vector(15 downto 0);
	signal sig_y_valid : std_logic;
    signal reg_a : std_logic_vector(7 downto 0);
	signal reg_b : std_logic_vector(7 downto 0);
	signal reg_start : std_logic;
	signal reg_y : std_logic_vector(15 downto 0);
	signal reg_y_valid : std_logic;
begin

    -- Output registering to ensure timing paths
    process(clk)
    begin
        if rising_edge(clk) then
            reg_a <= a;
			reg_b <= b;
			reg_start <= start;
			reg_y <= sig_y;
			reg_y_valid <= sig_y_valid;
        end if;
    end process;

    uut: entity work.array_mul_8x8_pl
    port map (
        a => reg_a,
		b => reg_b,
		start => reg_start,
		clk => clk,
		y => sig_y,
		y_valid => sig_y_valid
    );

    y <= reg_y;
	y_valid <= reg_y_valid;
end architecture;