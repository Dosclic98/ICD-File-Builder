from abc import ABC, abstractmethod
from icdbuilder.model.icd import ICD, ICDBuilder
from icdbuilder.model.power import PowerModel, Split, SplitMethod
from pandapower import pandapowerNet
from pathlib import Path
import os

class Builder(ABC):

    def __init__(self, network):
        self.network = network
    
    def setNetwork(self, network):
        self.network = network

    @abstractmethod
    def build(self, splitMethod):
        pass

class FromPPToICDBuilder(Builder):
    def __init__(self, network: pandapowerNet):
        super().__init__(network)


    def build(self, splitMethod: SplitMethod, outputPath: Path):
        pm: PowerModel = PowerModel.fromPandapowerModel(self.network)
        splits: list[Split] = Split.fromPowerModelSplit(pm, splitMethod)
        # Create the output path directory if it does not exist
        os.makedirs(outputPath, exist_ok=True)

        for split in splits:
            ICDBuilder.build(split=split).toFile(outputPath.joinpath(f"{split.name}.icd.xml"))