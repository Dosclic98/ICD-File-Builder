from dataclasses import dataclass
from abc import ABC, abstractmethod
from enum import Enum
from icdbuilder.model.power import Split
from icdbuilder.model.binder.binder_static import *
import json

class BindingType(Enum):
    MONITOR = "monitor"
    CONTROL = "control"
    BOTH = "both"

# Each binding represents a mapping bween a IEC61850 data attribute and a power model value that can be monitored or controlled.
class Binding(ABC):
    def __init__(self, splitName: str, bindingType: BindingType, dataAttributePath: str):
        self.splitName = splitName
        self.bindingType = bindingType
        self.dataAttributePath = dataAttributePath

    def isMonitorable(self) -> bool:
        return self.bindingType in [BindingType.MONITOR, BindingType.BOTH]
    
    def isControllable(self) -> bool:
        return self.bindingType in [BindingType.CONTROL, BindingType.BOTH]

class PandapowerElementType(Enum):
    BUS = "bus"
    GEN = "gen"
    SGEN = "sgen"
    STORAGE = "storage"
    LOAD = "load"
    LINE = "line"
    TRAFO = "trafo"

class PandapowerBinding(Binding):
    def __init__(self, splitName: str, bindingType: BindingType, dataAttributePath: str, 
                    pandapowerElementType: PandapowerElementType, pandapowerElementId: int, 
                    isResult: bool, pandapowerAttribute: str):
        super().__init__(splitName, bindingType, dataAttributePath)
        self.pandapowerElementType = pandapowerElementType
        self.pandapowerElementId = pandapowerElementId
        self.isResult = isResult
        self.pandapowerAttribute = pandapowerAttribute

    def __dict__(self):
        return {
            "splitName": self.splitName,
            "bindingType": self.bindingType.value,
            "dataAttributePath": self.dataAttributePath,
            "pandapowerElementType": self.pandapowerElementType.value,
            "pandapowerElementId": self.pandapowerElementId,
            "isResult": self.isResult,
            "pandapowerAttribute": self.pandapowerAttribute
        }

    def toJSON(self):
        return json.dumps(
            self.__dict__(),
            indent=4,
            sort_keys=True
        )

    def __str__(self):
        return f"PandapowerBinding(splitName={self.splitName}, bindingType={self.bindingType}, dataAttributePath={self.dataAttributePath}, pandapowerElementType={self.pandapowerElementType}, pandapowerElementId={self.pandapowerElementId}, pandapowerAttribute={self.pandapowerAttribute})"
    
class Binder(ABC):

    @staticmethod
    def buildBindings(split: Split) -> list[Binding]:
        pass

class PandapowerBinder(Binder):
    @staticmethod
    def buildBindings(split: Split) -> list[PandapowerBinding]:
        bindings: list[PandapowerBinding] = []

        genUnits = split.getObsGenUnits()
        for id, (index, gen) in genUnits.items():
            dataAttributePath = singleGenMeasTemplate.format(inst=index)
            binding = PandapowerBinding(split.name, BindingType.MONITOR, dataAttributePath, 
                                        PandapowerElementType.SGEN, gen.id, True, "p_mw")
            bindings.append(binding)
        return bindings