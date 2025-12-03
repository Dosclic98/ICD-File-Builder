from dataclasses import dataclass
from abc import ABC, abstractmethod
from enum import Enum
from icdbuilder.model.power import Split, GenType
from icdbuilder.model.binder.binder_static import *
from icdbuilder.model.binder.manipulation import ManipulationFunction, ManipulationFunctionType
from types import FunctionType
import json

class BindingType(Enum):
    MONITOR = "monitor"
    CONTROL = "control"
    BOTH = "both"

# Each binding represents a mapping bween a IEC61850 data attribute and a power model value that can be monitored or controlled.
class Binding(ABC):
    def __init__(self, bindingType: BindingType, dataAttributePath: str):
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

# Component representation for pandapower measurements / controllable elements
# Each component maps a pandapower element attribute (both in terms of result and setpoint) to/from an IEC61850 data attribute
class PandapowerComponent:
    # TODO: Add if the measurements is a result or a setpoint (if derives from the "res_" dataframe or not)
    def __init__(self, elementType: PandapowerElementType, elementId: int, attribute: str, sourceExponent: int, destExponent: int):
        self.elementType = elementType
        self.elementId = elementId
        self.attribute = attribute
        self.sourceExponent = sourceExponent
        self.destExponent = destExponent

    def __dict__(self):
        return {
            "elementType": self.elementType.value,
            "elementId": self.elementId,
            "attribute": self.attribute,
            "sourceExponent": self.sourceExponent,
            "destExponent": self.destExponent
        }
    
    def __str__(self):
        return f"PandapowerComponent(elementType={self.elementType}, elementId={self.elementId}, attribute={self.attribute}, sourceExponent={self.sourceExponent}, destExponent={self.destExponent})"

# Each binding represents a mapping between a IEC61850 data attribute and a list of pandapower components 
# that can be monitored or controlled. The elements are combined using a specified manipulation function.
# For example, a binding can map the total active power generation of a split to the sum of the active power
# of all generators in that split. Or it can equally distribute the reactive power setpoint at the Point of Connection
# to all generators in the split.  
class PandapowerBinding(Binding):
    def __init__(self, bindingType: BindingType, dataAttributePath: str, 
                    components: list[PandapowerComponent], combFunction: ManipulationFunctionType):
        super().__init__(bindingType, dataAttributePath)
        self.components: list[PandapowerComponent] = components
        self.combFunction: ManipulationFunctionType = combFunction

    def __dict__(self):
        return {
            "bindingType": self.bindingType.value,
            "dataAttributePath": self.dataAttributePath,
            "components": [m.__dict__() for m in self.components],
            "combFunction": self.combFunction.value
        }

    def __str__(self):
        return f"PandapowerBinding(splitName={self.splitName}, bindingType={self.bindingType}, dataAttributePath={self.dataAttributePath}, components=[{', '.join(str(m) for m in self.components)}], combFunction={self.combFunction})"


class Binder(ABC):

    @staticmethod
    def buildBindings(split: Split) -> list[Binding]:
        pass

class PandapowerBinder(Binder):
    @staticmethod
    def buildBindings(split: Split) -> list[PandapowerBinding]:
        bindings: list[PandapowerBinding] = []

        # Adding single observable generator components bindings
        genUnits = split.getObsGenUnits()
        for id, (index, gen) in genUnits.items():
            # Create component and binding for active power monitoring (at source it is in kW, at dest in MW)
            component = PandapowerComponent(PandapowerElementType.SGEN, gen.id, "p_mw", 3, 6)
            dataAttributePath = singleGenMeasTemplate.format(inst=index)
            binding = PandapowerBinding(BindingType.MONITOR, dataAttributePath, 
                                        [component], ManipulationFunctionType.DIRECT)
            bindings.append(binding)
            # TODO: Probably here I should also add the health status of each gen unit (binded to the pandapower "in_service" attribute)
        
        # Adding total active power per generation type binding
        genTypes = [GenType.PV, GenType.WIND, GenType.THERMAL]
        for genType in genTypes:
            genUnitrOfType = split.genGenUnitsPerType(genType)
            if len(genUnitrOfType) != 0:
                components: list[PandapowerComponent] = []
                for id, gen in genUnitrOfType.items():
                    component = PandapowerComponent(PandapowerElementType.SGEN, gen.id, "p_mw", 3, 6)
                    components.append(component)
                if genType == GenType.PV:
                    genTypeStr = "GenPV"
                elif genType == GenType.WIND:
                    genTypeStr = "GenWind"
                else:
                    genTypeStr = "GenTer"
                dataAttributePath = perGenTypeMeasTemplate.format(genType=genTypeStr)
                binding = PandapowerBinding(BindingType.MONITOR, dataAttributePath,
                                            components, ManipulationFunctionType.SUM)
                bindings.append(binding)

        return bindings