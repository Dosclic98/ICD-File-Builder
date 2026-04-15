from dataclasses import dataclass
from abc import ABC, abstractmethod
from enum import Enum
from icdbuilder.model.power import Split, GenType, StorageUnit, Line
from icdbuilder.model.binder.binder_static import *
from icdbuilder.model.binder.manipulation import ManipulationFunction, ManipulationFunctionType, HealthType, ModeType, DerFunStateType
from types import FunctionType
import json, logging

class BindingType(Enum):
    MONITOR = "monitor"
    CONTROL = "control"
    BOTH = "both"

# Each binding represents a mapping bween a IEC61850 data attribute and a power model value that can be monitored or controlled.
class Binding(ABC):
    def __init__(self, bindingType: BindingType, dataAttributePath: str, timestampAttributePath: str):
        self.bindingType = bindingType
        self.dataAttributePath = dataAttributePath
        self.timestampAttributePath = timestampAttributePath

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
    def __init__(self, isResult: bool, elementType: PandapowerElementType, elementId: int, attribute: str,
                 sourceExponent: int, destExponent: int, weight: float = 1.0):
        self.isResult = isResult
        self.elementType = elementType
        self.elementId = elementId
        self.attribute = attribute
        self.sourceExponent = sourceExponent
        self.destExponent = destExponent
        self.weight = weight

    def __dict__(self):
        return {
            "isResult": self.isResult,
            "elementType": self.elementType.value,
            "elementId": self.elementId,
            "attribute": self.attribute,
            "sourceExponent": self.sourceExponent,
            "destExponent": self.destExponent,
            "weight": self.weight
        }
    
    def __str__(self):
        return f"PandapowerComponent(isResult={self.isResult}, elementType={self.elementType}, elementId={self.elementId}, attribute={self.attribute}, sourceExponent={self.sourceExponent}, destExponent={self.destExponent}, weight={self.weight})"

# Each binding represents a mapping between a IEC61850 data attribute and a list of pandapower components 
# that can be monitored or controlled. The elements are combined using a specified manipulation function.
# For example, a binding can map the total active power generation of a split to the sum of the active power
# of all generators in that split. Or it can equally distribute the reactive power setpoint at the Point of Connection
# to all generators in the split.  
class PandapowerBinding(Binding):
    def __init__(self, bindingType: BindingType, dataAttributePath: str, timestampAttributePath: str,
                    components: list[PandapowerComponent], combFunction: ManipulationFunctionType, 
                    defaultValue, scalingFactor: float = 1.0):
        super().__init__(bindingType, dataAttributePath, timestampAttributePath)
        self.components: list[PandapowerComponent] = components
        self.combFunction: ManipulationFunctionType = combFunction
        self.defaultValue = defaultValue
        self.scalingFactor = scalingFactor

    def __dict__(self):
        return {
            "bindingType": self.bindingType.value,
            "dataAttributePath": self.dataAttributePath,
            "timestampAttributePath": self.timestampAttributePath,
            "components": [m.__dict__() for m in self.components],
            "combFunction": self.combFunction.value,
            "defaultValue": self.defaultValue,
            "scalingFactor": self.scalingFactor
        }

    def __str__(self):
        return f"PandapowerBinding(splitName={self.splitName}, bindingType={self.bindingType}, dataAttributePath={self.dataAttributePath}, timestampAttributePath={self.timestampAttributePath}, components=[{', '.join(str(m) for m in self.components)}], combFunction={self.combFunction}, defaultValue={self.defaultValue}, scalingFactor={self.scalingFactor})"

# The aggregator binding is a special type of binding used to interact with 
# the RSE power simulator (components and combFunction are not used here)
class AggregatorBinding(Binding):
    def __init__(self, bindingType: BindingType, dataAttributePath: str, timestampAttributePath: str, defaultValue):
        super().__init__(bindingType, dataAttributePath, timestampAttributePath)
        self.defaultValue = defaultValue

    def __dict__(self):
        return {
            "bindingType": self.bindingType.value,
            "dataAttributePath": self.dataAttributePath,
            "timestampAttributePath": self.timestampAttributePath,
            "defaultValue": self.defaultValue
        }

class Binder(ABC):

    @staticmethod
    def buildBindings(split: Split) -> list[Binding]:
        pass

class PandapowerBinder(Binder):
    @staticmethod
    def buildBindings(split: Split) -> list[PandapowerBinding]:
        bindings: list[PandapowerBinding] = []

        bindings = PandapowerBinder._buildPdCBindings(split, bindings)

        bindings = PandapowerBinder._buildSingleGenBindings(split, bindings)
        
        bindings = PandapowerBinder._buildPerTypeBindings(split, bindings)

        bindings = PandapowerBinder._buildAvailabilityBindings(split, bindings)

        bindings = PandapowerBinder._buildSetpointBindings(split, bindings)

        return bindings
    
    @staticmethod
    def _buildPdCBindings(split: Split, bindings: list[Binding]) -> list[Binding]:
        mainBus = split.getMainBus()
        if mainBus is not None:
            # TotW/TotVAr at PdC from generators and storage only.
            # Component weight is an orientation sign: +1 positive contribution, -1 negative contribution.
            totPcomponents: list[PandapowerComponent] = []
            totQomponents: list[PandapowerComponent] = []
            for gen in split.generationUnits.values():
                componentP = PandapowerComponent(True, PandapowerElementType.SGEN, gen.id, "p_mw", 6, 3, weight=1.0)
                componentQ = PandapowerComponent(True, PandapowerElementType.SGEN, gen.id, "q_mvar", 6, 3, weight=1.0)
                totPcomponents.append(componentP)
                totQomponents.append(componentQ)
            for sto in split.storageUnits.values():
                componentP = PandapowerComponent(True, PandapowerElementType.STORAGE, sto.id, "p_mw", 6, 3, weight=-1.0)
                componentQ = PandapowerComponent(True, PandapowerElementType.STORAGE, sto.id, "q_mvar", 6, 3, weight=-1.0)
                totPcomponents.append(componentP)
                totQomponents.append(componentQ)
            binding = PandapowerBinding(BindingType.MONITOR, pdcTotPStr, pdcTotPTimeStr, totPcomponents, ManipulationFunctionType.WEIGHTED_SUM, 0.0)
            bindings.append(binding)
            # Adding TotQ @ PdC binding (it's the total active power from generation and storage units and we must convert it from kW to MW)
            binding = PandapowerBinding(BindingType.MONITOR, pdcTotQStr, pdcTotQTimeStr, totQomponents, ManipulationFunctionType.WEIGHTED_SUM, 0.0)
            bindings.append(binding)
            lines: dict[int, Line] = split.getLines()
            if len(lines) == 0:
                logging.warning("No lines connected to the main bus, skipping line-related bindings at PdC.")
            
            # Get the first line and replicate the voltage magnitude, angle and current bindings for the three phases
            firstKey = next(iter(lines))
            line = lines[firstKey]
            for i in range(min(len(pdcVoltAngStrs), len(pdcVoltMagStrs), len(pdcCurrMagStrs))):
                # Adding line voltages @ PdC (we get them from the lines connected to the bus)
                # TODO: These should be converted to phase-to-phase voltages and angles!
                componentMag = PandapowerComponent(True, PandapowerElementType.LINE, line.id, "vm_from_pu", 1, 1) 
                bindingMag = PandapowerBinding(BindingType.MONITOR, pdcVoltMagStrs[i], pdcVoltMagTimeStrs[i], [componentMag], ManipulationFunctionType.SUM, 0.0)
                componentAng = PandapowerComponent(True, PandapowerElementType.LINE, line.id, "va_from_degree", 1, 1)
                bindingAng = PandapowerBinding(BindingType.MONITOR, pdcVoltAngStrs[i], pdcVoltAngTimeStrs[i], [componentAng], ManipulationFunctionType.SUM, 0.0)
                bindings.append(bindingMag)
                bindings.append(bindingAng)
                # Adding line currents @ PdC (we get them from the lines connected to the bus and we must convert them from kA to A)
                componentCurr = PandapowerComponent(True, PandapowerElementType.LINE, line.id, "i_ka", 3, 1) 
                bindingCurr = PandapowerBinding(BindingType.MONITOR, pdcCurrMagStrs[i], pdcCurrMagTimeStrs[i], [componentCurr], ManipulationFunctionType.SUM, 0.0)
                bindings.append(bindingCurr)

        return bindings
        
    
    @staticmethod
    def _buildSingleGenBindings(split: Split, bindings: list[Binding]) -> list[Binding]:
        genUnits = split.getObsGenUnits()
        for id, (index, gen) in genUnits.items():
            # Create a component binding for the health of the single generator
            component = PandapowerComponent(False, PandapowerElementType.SGEN, gen.id, "in_service", 1, 1)
            dataAttributePath = singleGenHealthTemplate.format(inst=index)
            timeAttributePath = singleGenHealthTimeTemplate.format(inst=index)
            binding = PandapowerBinding(BindingType.MONITOR, dataAttributePath, timeAttributePath,
                                        [component], ManipulationFunctionType.S2H, HealthType.OK.value)
            bindings.append(binding)

            # Create component and binding for active power monitoring (at source it is in MW, at dest in kW)
            component = PandapowerComponent(True, PandapowerElementType.SGEN, gen.id, "p_mw", 6, 3)
            dataAttributePath = singleGenMeasTemplate.format(inst=index)
            timeAttributePath = singleGenMeasTimeTemplate.format(inst=index)
            binding = PandapowerBinding(BindingType.MONITOR, dataAttributePath, timeAttributePath,
                                        [component], ManipulationFunctionType.DIRECT, 0.0)
            bindings.append(binding)

            # Create a component and binding for grid identifier for the single generation unit
            dataAttributePath = singleGenIdTemplate.format(inst=index)
            timeAttributePath = singleGenIdTimeTemplate.format(inst=index)
            binding = PandapowerBinding(BindingType.MONITOR, dataAttributePath, timeAttributePath, [], ManipulationFunctionType.DIRECT, index)
            bindings.append(binding)

        return bindings
    
    def _buildPerTypeBindings(split: Split, bindings: list[Binding]) -> list[Binding]:
        # Adding total active power per generation type binding
        genTypes = [GenType.PV, GenType.WIND, GenType.THERMAL, GenType.HYDRO]
        for genType in genTypes:
            genUnitrOfType = split.genGenUnitsPerType(genType)
            
            components: list[PandapowerComponent] = []
            for id, gen in genUnitrOfType.items():
                component = PandapowerComponent(True, PandapowerElementType.SGEN, gen.id, "p_mw", 6, 3)
                components.append(component)
                
            if genType == GenType.PV:
                genTypeStr = "GenPV"
            elif genType == GenType.WIND:
                genTypeStr = "GenWi"
            elif genType == GenType.THERMAL:
                genTypeStr = "GenTer"
            else:
                genTypeStr = "GenIdr"
            dataAttributePath = perGenTypeTotPTemplate.format(genType=genTypeStr)
            timeAttributePath = perGenTypeTotPTimeTemplate.format(genType=genTypeStr)
            binding = PandapowerBinding(BindingType.MONITOR, dataAttributePath, timeAttributePath,
                                        components, ManipulationFunctionType.SUM, 0.0)
            bindings.append(binding)

        # Add total active power for storage units
        stoUnits: dict[int, StorageUnit] = split.getStoUnits()
        components: list[PandapowerComponent] = [PandapowerComponent(True, PandapowerElementType.STORAGE, stoUnit.id, "p_mw", 6, 3) for id, stoUnit in stoUnits.items()] 
        binding = PandapowerBinding(BindingType.MONITOR, stoTotPStr, stoToPTimeStr, components, ManipulationFunctionType.SUM, 0.0)
        bindings.append(binding)

        return bindings

    @staticmethod
    def _buildAvailabilityBindings(split: Split, bindings: list[Binding]) -> list[Binding]:
        genEligibleCount = sum(
            1 for gen in split.generationUnits.values()
            if gen.getMaxActivePowerKw() >= Split.powerGenTresholdKw
        )
        stoEligibleCount = sum(
            1 for sto in split.storageUnits.values()
            if sto.getMaxActivePowerKw() >= Split.powerStoTresholdKw
        )

        genAvailDefault = 1 if genEligibleCount > 0 else 5
        stoAvailDefault = 1 if stoEligibleCount > 0 else 5
        plantAvailDefault = 1 if (genEligibleCount + stoEligibleCount) > 0 else 5

        bindings.append(PandapowerBinding(
            BindingType.MONITOR,
            genAvailStr,
            genAvailTimeStr,
            [],
            ManipulationFunctionType.DIRECT,
            genAvailDefault
        ))

        bindings.append(PandapowerBinding(
            BindingType.MONITOR,
            stoAvailStr,
            stoAvailTimeStr,
            [],
            ManipulationFunctionType.DIRECT,
            stoAvailDefault
        ))

        bindings.append(PandapowerBinding(
            BindingType.MONITOR,
            plantAvailStr,
            plantAvailTimeStr,
            [],
            ManipulationFunctionType.DIRECT,
            plantAvailDefault
        ))

        return bindings
    
    def _buildSetpointBindings(split: Split, bindings: list[Binding]) -> list[Binding]:
        genUnits = split.generationUnits
        maxApparentPowerKva = split.getMaxApparentPowerKva()
        if maxApparentPowerKva > 0:
            # Convert aggregated reactive power [kVAr] to percentage of Smax [kVA].
            reactivePctScalingFactor = 100.0 / maxApparentPowerKva
        else:
            logging.warning(
                "Split %s has non-positive Smax; reactive setpoint bindings keep unitary scaling.",
                split.name,
            )
            reactivePctScalingFactor = 1.0

        # Add read-only reactive power setpoint
        componentsRO = [PandapowerComponent(True, PandapowerElementType.SGEN, id, "q_mvar", 6, 3) for id, gen in genUnits.items()]
        bindingRO = PandapowerBinding(
            BindingType.MONITOR,
            qSetReadStr,
            qSetReadTimeStr,
            componentsRO,
            ManipulationFunctionType.WEIGHTED_SUM,
            0.0,
            scalingFactor=reactivePctScalingFactor,
        )
        # Add write-only reactive power setpoint
        componentsWO = [PandapowerComponent(True, PandapowerElementType.SGEN, id, "q_mvar", 6, 3) for id, gen in genUnits.items()]
        bindingWO = PandapowerBinding(
            BindingType.CONTROL,
            qSetWriteStr,
            qSetWriteTimeStr,
            componentsWO,
            ManipulationFunctionType.WEIGHTED_SUM,
            0.0,
            scalingFactor=reactivePctScalingFactor,
        )

        bindings.append(bindingRO)
        bindings.append(bindingWO)

        return bindings

class AggregatorBinder(Binder):
    # Does not need the split parameter since it does not build the components array
    @staticmethod
    def buildBindings() -> list[AggregatorBinding]:
        bindings: list[AggregatorBinding] = []
        bindings = AggregatorBinder._buildPdCBindings(bindings)
        bindings = AggregatorBinder._buildSetpointBindings(bindings)
        

        return bindings
    
    def _buildPdCBindings(bindings: list[Binding]) -> list[Binding]:
        # Adding total active power at PdC from the RSE power simulator
        binding = AggregatorBinding(BindingType.MONITOR, pdcTotPStr, pdcTotPTimeStr, 0.0)
        bindings.append(binding)
        # Adding total reactive power at PdC from the RSE power simulator
        binding = AggregatorBinding(BindingType.MONITOR, pdcTotQStr, pdcTotQTimeStr, 0.0)
        bindings.append(binding)

        return bindings
    
    #def _buildAvailabilityBindings(bindings: list[Binding]) -> list[Binding]:

        
        
    def _buildSetpointBindings(bindings: list[Binding]) -> list[Binding]:
        # Add read-only and write-only reactive power setpoint at PdC
        bindingQRO = AggregatorBinding(BindingType.MONITOR, aggQSetReadStr, aggQSetReadTimeStr, 0.0)
        bindingQWO = AggregatorBinding(BindingType.CONTROL, aggQSetWriteStr, aggQSetWriteTimeStr, 0.0)
        # Add read-only and write-only mode parameter for reactive power control function at PdC
        bindingModRO = AggregatorBinding(BindingType.MONITOR, dvarModReadStr, dvarModReadTimeStr, ModeType.ON.value)
        bindingModWO = AggregatorBinding(BindingType.CONTROL, dvarModWriteStr, dvarModWriteTimeStr, ModeType.ON.value)
        # Add read-only parameter for health state of the reactive power control function at PdC (we don't need a write operation for this parameter since it's an output)
        bindingHealthRO = AggregatorBinding(BindingType.MONITOR, dvarHealthReadStr, dvarHealthReadTimeStr, HealthType.OK.value)
        # Add read-only function operational status of the reactive power control function at PdC (we don't need a write operation for this parameter since it's an output)
        bindingFctOpStRO = AggregatorBinding(BindingType.MONITOR, dvarFctOpStReadStr, dvarFctOpStReadTimeStr, DerFunStateType.SLAVE.value)

        # Add read-only active power setpoint at PdC from the RSE power simulator
        bindingPRO = AggregatorBinding(BindingType.MONITOR, aggPSetReadStr, aggPSetReadTimeStr, 0.0)
        # Add write-only active power setpoint at PdC for the RSE power simulator
        bindingPWO = AggregatorBinding(BindingType.CONTROL, aggPSetWriteStr, aggPSetWriteTimeStr, 0.0)
        # Add read-only and write-only mode parameter for active power control function at PdC
        bindingPModRO = AggregatorBinding(BindingType.MONITOR, dagcModReadStr, dagcModReadTimeStr, ModeType.ON.value)
        bindingPModWO = AggregatorBinding(BindingType.CONTROL, dagcModWriteStr, dagcModWriteTimeStr, ModeType.ON.value)
        # Add read-only parameter for health state of the active power control function at PdC (we don't need a write operation for this parameter since it's an output)
        bindingPHealthRO = AggregatorBinding(BindingType.MONITOR, dagcHealthReadStr, dagcHealthReadTimeStr, HealthType.OK.value)
        # Add read-only function operational status of the active power control function at PdC (we don't need a write operation for this parameter since it's an output)
        bindingPFctOpStRO = AggregatorBinding(BindingType.MONITOR, dagcFctOpStReadStr, dagcFctOpStReadTimeStr, DerFunStateType.SLAVE.value)


        bindings.append(bindingQRO)
        bindings.append(bindingQWO)
        bindings.append(bindingModRO)
        bindings.append(bindingModWO)
        bindings.append(bindingHealthRO)
        bindings.append(bindingFctOpStRO)

        bindings.append(bindingPRO)
        bindings.append(bindingPWO)
        bindings.append(bindingPModRO)
        bindings.append(bindingPModWO)
        bindings.append(bindingPHealthRO)
        bindings.append(bindingPFctOpStRO)


        return bindings
    