import pandapower as pp
from pandapower.networks.cigre_networks import create_cigre_network_mv
from icdbuilder.model.icd import ICD, ICDBuilder

def main():
    net = create_cigre_network_mv(with_der="all")
    
    icd = ICDBuilder.build()
    icd.toFile("output.icd.xml")
