import pandapower as pp
from pandapower.networks.cigre_networks import create_cigre_network_mv
from icdbuilder.model.icd import ICD, ICDBuilder
from icdbuilder.model.power import PowerModel 

def main():
    net = create_cigre_network_mv(with_der="all")
    
    icd = ICDBuilder.build()
    icd.toFile("output.icd.xml")

    pm: PowerModel = PowerModel.fromPandapowerModel(net)

