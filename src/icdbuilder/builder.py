from abc import ABC, abstractmethod
from icdbuilder.model.icd import ICD, ICDBuilder
from icdbuilder.model.power import PowerModel, Split, SplitMethod
from icdbuilder.model.binder.binder import PandapowerBinding, PandapowerElementType, PandapowerBinder
from pandapower import pandapowerNet
from pathlib import Path
import os, json

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


    def build(self, splitMethod: SplitMethod, outputPath: Path) -> list[Split]:
        pm: PowerModel = PowerModel.fromPandapowerModel(self.network)
        splits: list[Split] = Split.fromPowerModelSplit(pm, splitMethod)
        # Create the output path directory if it does not exist
        os.makedirs(outputPath, exist_ok=True)
        # Clear existing files in the output directory
        for file in os.listdir(outputPath):
            filePath = os.path.join(outputPath, file)
            if os.path.isfile(filePath):
                os.remove(filePath)

        for split in splits:
            ICDBuilder.build(split=split).toFile(outputPath.joinpath(f"{split.name}.icd.xml"))
        
        return splits

class FromPPToBinderBuilder(Builder):
    def __init__(self, network: pandapowerNet):
        super().__init__(network=network)

    def build(self, splitMethod: SplitMethod, outputPath: Path):
        pm: PowerModel = PowerModel.fromPandapowerModel(self.network)
        splits: list[Split] = Split.fromPowerModelSplit(pm, splitMethod)
        # Create the output path directory if it does not exist
        os.makedirs(outputPath, exist_ok=True)
        # Clear existing files in the output directory
        for file in os.listdir(outputPath):
            filePath = os.path.join(outputPath, file)
            if os.path.isfile(filePath):
                os.remove(filePath)

        for split in splits:
            bindings: list[PandapowerBinding] = PandapowerBinder.buildBindings(split=split)
            # Save bindings to a JSON file
            with open(outputPath.joinpath(f"{split.name}_bindings.json"), 'w') as f:
                json_bindings = [binding.toJSON() for binding in bindings]
                f.write(json.dumps(json_bindings, indent=4))