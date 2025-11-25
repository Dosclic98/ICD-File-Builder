from icdbuilder.model.icd import ICD, ICDBuilder
from icdbuilder.model.power import PowerModel, Split, SplitMethod
from icdbuilder.utils import create_cigre_network_mv_all_der

def main():
    net = create_cigre_network_mv_all_der()

    pm: PowerModel = PowerModel.fromPandapowerModel(net)
    splits: list[Split] = Split.fromPowerModelSplit(pm, SplitMethod.BUS)
    for split in splits:
        ICDBuilder.build(split=split).toFile(f"output/{split.name}.icd.xml")
