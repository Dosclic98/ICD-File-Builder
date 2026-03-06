import pandapower as pp
import numpy as np
from pandapower.networks.cigre_networks import create_cigre_network_mv

def create_cigre_network_mv_all_der() -> pp.pandapowerNet:
    net = create_cigre_network_mv(with_der="all")

    # Transforming bus[0] in a 220kV bus
    net.bus.at[0, "vn_kv"] = 220.0
    # Transforming trafo[0] and trafo[1] in 220 kv --> 20kV busses 
    net.trafo.at[0, "vn_hv_kv"] = 220.0
    net.trafo.at[1, "vn_hv_kv"] = 220.0 

    # Adjusting PV generation values to stay within CEI 0-16 tresholds
    for i in net.sgen.index:
        if net.sgen.at[i, "p_mw"] < 0.1 and net.sgen.at[i, "type"] == "PV": 
            net.sgen.at[i, "p_mw"] = net.sgen.at[i, "p_mw"] + 0.1 # Adding 0.1 MW to each PV generator 
            net.sgen.at[i, "q_mvar"] = net.sgen.at[i, "p_mw"] * 0.1
            net.sgen.at[i, "sn_mva"] = net.sgen.at[i, "p_mw"] * 1.1 # Adjusting the rated apparent power to be 10% higher than the active power
    
    # Adjusting the reactive power capability of the generators to be able to provide reactive power support if needed
    for i in net.sgen.index:
        p = net.sgen.at[i, "p_mw"]
        sn = net.sgen.at[i, "sn_mva"]
        qCap = max(0.0, np.sqrt(max(sn**2 - p**2, 0.0)))
        # Set the active power limits to the current active power (we suppose the flexibility is only in the reactive power)
        net.sgen.at[i, "min_p_mw"] = p
        net.sgen.at[i, "max_p_mw"] = p
        net.sgen.at[i, "min_q_mvar"] = -qCap
        net.sgen.at[i, "max_q_mvar"] =  qCap
    
    # Adjust voltage/loading constraints
    net.bus["min_vm_pu"] = 0.95
    net.bus["max_vm_pu"] = 1.05
    net.line["max_loading_percent"] = 100.0
    net.trafo["max_loading_percent"] = 100.0

    # Clear cost functions
    net.poly_cost.drop(net.poly_cost.index, inplace=True)
    # Penalize |Q| via quadratic cost so OPF avoids unnecessary extreme Q
    for i in net.sgen.index:
        pp.create_poly_cost(
            net, i, "sgen",
            cp1_eur_per_mw=0.0,
            cq1_eur_per_mvar=0.0,
            cq2_eur_per_mvar2=1.0
        )

    return net

def set_controllable_sgen_if_CCI(net: pp.pandapowerNet, bussesWithCCI = []) -> None:
    for i in net.sgen.index:
        if net.sgen.at[i, "bus"] in bussesWithCCI:
            net.sgen.at[i, "controllable"] = True
        else:
            net.sgen.at[i, "controllable"] = False