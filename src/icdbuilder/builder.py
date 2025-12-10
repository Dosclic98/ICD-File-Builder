from abc import ABC, abstractmethod
from icdbuilder.model.icd import ICD, ICDBuilder
from icdbuilder.model.power import PowerModel, Split, SplitMethod
from icdbuilder.model.binder.binder import PandapowerBinding, PandapowerElementType, PandapowerBinder, Binding
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


    def build(self, splitMethod: SplitMethod, outputPath: Path | None) -> list[Split]:
        pm: PowerModel = PowerModel.fromPandapowerModel(self.network)
        splits: list[Split] = Split.fromPowerModelSplit(pm, splitMethod)
        if outputPath is not None:
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

class SplitBindings():
    def __init__(self, split: Split, bindings: list[Binding]):
        self.split = split
        self.bindings = bindings

    def __dict__(self):
        return {"splitName": self.split.name, "bindings": [binding.__dict__() for binding in self.bindings]}

class FromPPToBinderBuilder(Builder):
    def __init__(self, network: pandapowerNet):
        super().__init__(network=network)

    def build(self, splitMethod: SplitMethod, outputPath: Path | None = None) -> dict[str, SplitBindings]:
        pm: PowerModel = PowerModel.fromPandapowerModel(self.network)
        splits: list[Split] = Split.fromPowerModelSplit(pm, splitMethod)
        if outputPath is not None:
            # Create the output path directory if it does not exist
            os.makedirs(outputPath, exist_ok=True)
            # Clear existing files in the output directory
            for file in os.listdir(outputPath):
                filePath = os.path.join(outputPath, file)
                if os.path.isfile(filePath):
                    os.remove(filePath)

        mergedBindings: dict[str, SplitBindings] = dict()
        for split in splits:
            bindings: list[PandapowerBinding] = PandapowerBinder.buildBindings(split=split)
            # Save bindings to a JSON file
            splitBindings: SplitBindings = SplitBindings(split, bindings)
            mergedBindings[split.name] = splitBindings
            if outputPath is not None:
                with open(outputPath.joinpath(f"{split.name}_bindings.json"), 'w') as f:
                    f.write(json.dumps(splitBindings.__dict__(), indent=4))
        if outputPath is not None:
            with open(outputPath.joinpath("bindings.json"), "w") as f:
                f.write(json.dumps({"merged": [mergedBindings[key].__dict__() for key in mergedBindings.keys()]}, indent=4))

        return mergedBindings