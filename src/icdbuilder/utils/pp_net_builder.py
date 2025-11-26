import pandapower as pp
from pandapower.networks.cigre_networks import create_cigre_network_mv

def create_cigre_network_mv_all_der() -> pp.pandapowerNet:
    net = create_cigre_network_mv(with_der="all")

    # Transforming bus[0] in a 220kV bus
    net.bus.at[0, "vn_kv"] = 220.0
    # Transforming trafo[0] and trafo[1] in 220 kv --> 20kV busses 
    net.trafo.at[0, "vn_hv_kv"] = 220.0
    net.trafo.at[1, "vn_hv_kv"] = 220.0 

    # Adjusting PV generation values to stay within CEI 0-16 tresholds
    for i in range(0, 8):
        if net.sgen.at[i, "p_mw"] < 0.1: 
            net.sgen.at[i, "p_mw"] = net.sgen.at[i, "p_mw"] + 0.1 # Adding 0.1 MW to each PV generator 
            net.sgen.at[i, "q_mvar"] = net.sgen.at[i, "p_mw"] * 0.1

    return net