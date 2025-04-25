def is_clock_port(name):
    return name.lower() in ["clk", "clock"]

def get_vector_idx(port_type):
    j, i = port_type.split('(')[-1].replace(')', '').split('downto')
    return int(i), int(j)
