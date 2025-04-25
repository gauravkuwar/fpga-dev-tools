library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity target is
    port (
        {{PORT_LIST}}
    );
end entity;

architecture rtl of target is
    {{SIG_DECLS}}
    {{FLOP_DECLS}}
begin

    -- Output registering to ensure timing paths
    process({{CLK_NAME}})
    begin
        if rising_edge({{CLK_NAME}}) then
            {{FLOP_LOGIC}}
        end if;
    end process;

    uut: entity work.{{MODULE_NAME}}
    port map (
        {{PORT_MAP}}
    );

    {{FLOP_OUT}}
end architecture;