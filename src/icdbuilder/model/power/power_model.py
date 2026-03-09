from enum import Enum
from dataclasses import dataclass
import math
from pandapower import pandapowerNet

class GenType(Enum):
    THERMAL = "thermal"
    HYDRO = "hydro"
    PV = "photovoltaic"
    WIND = "wind"
    OTHER = "other"

class NonExistingBusException(Exception):
    def __init__(self, busId: int):
        super().__init__(f"Bus with ID {busId} does not exist in the model.")

@dataclass
class Bus:
    id: int
    name: str
    voltageLevelKv: float

@dataclass
class Line:
    id: int
    name: str
    fromBusId: int
    toBusId: int
    maxCurrentKA: float

@dataclass
class GenerationUnit:
    id: int
    name: str
    busId: int
    genType: GenType
    maxApparentPowerKva: float

    def getMaxActivePowerKw(self, powerFactor: float = 0.95) -> float:
        return self.maxApparentPowerKva * powerFactor
    
    def getMaxReactivePowerKvar(self, powerFactor: float = 0.95) -> float:
        return (self.maxApparentPowerKva**2 - (self.maxApparentPowerKva * powerFactor)**2)**0.5

@dataclass
class StorageUnit:
    id: int
    name: str
    busId: int
    activePowerKw: float
    reactivePowerKvar: float
    maxApparentPowerKva: float

    def getMaxActivePowerKw(self, powerFactor: float = 0.95) -> float:
        return self.maxApparentPowerKva * powerFactor

    def getMaxReactivePowerKvar(self, powerFactor: float = 0.95) -> float:
        return (self.maxApparentPowerKva**2 - (self.maxApparentPowerKva * powerFactor)**2)**0.5

@dataclass
class Load:
    id: int
    name: str
    busId: int
    activePowerKw: float
    reactivePowerKvar: float
    maxApparentPowerKva: float

    def getMaxActivePowerKw(self, powerFactor: float = 0.95) -> float:
        return self.maxApparentPowerKva * powerFactor
    
    def getMaxReactivePowerKvar(self, powerFactor: float = 0.95) -> float:
        return (self.maxApparentPowerKva**2 - (self.maxApparentPowerKva * powerFactor)**2)**0.5

class PowerModel:
    def __init__(self):
        self.buses: dict = {}
        self.generationUnits: dict = {}
        self.storageUnits: dict = {}
        self.loads: dict = {}
        self.lines: dict = {}
    
    def addBus(self, id: int, name: str, voltageLevelKv: float):
        self.buses[id] = Bus(id, name, voltageLevelKv)

    def addLine(self, id: int, name: str, fromBusId: int, toBusId: int, maxCurrentKA: float):
        if fromBusId not in self.buses.keys():
            raise NonExistingBusException(fromBusId)
        if toBusId not in self.buses.keys():
            raise NonExistingBusException(toBusId)
        self.lines[id] = Line(id, name, fromBusId, toBusId, maxCurrentKA)
    
    def addGenerationUnit(self, id: int, name: str, busId: int, genType: GenType, maxApparentPowerKva: float):
        if busId not in self.buses.keys():
            raise NonExistingBusException(busId)
        self.generationUnits[id] = GenerationUnit(id, name, busId, genType, maxApparentPowerKva)

    def addStorageUnit(self, id: int, name: str, busId: int, activePowerKw: float, reactivePowerKvar: float, maxApparentPowerKva: float = None):
        if busId not in self.buses.keys():
            raise NonExistingBusException(busId)
        
        if maxApparentPowerKva is None:
            maxApparentPowerKva = (activePowerKw**2 + reactivePowerKvar**2)**0.5
        self.storageUnits[id] = StorageUnit(id, name, busId, activePowerKw, reactivePowerKvar, maxApparentPowerKva=maxApparentPowerKva)
    
    def addLoad(self, id: int, name: str, busId: int, activePowerKw: float, reactivePowerKvar: float, maxApparentPowerKva: float = None):
        if busId not in self.buses.keys():
            raise NonExistingBusException(busId)
        if maxApparentPowerKva is None:
            maxApparentPowerKva = (activePowerKw**2 + reactivePowerKvar**2)**0.5
        self.loads[id] = Load(id, name, busId, activePowerKw, reactivePowerKvar, maxApparentPowerKva=maxApparentPowerKva)

    def __str__(self):
        # Print each element in a different line
        buses_str = "\n".join(str(bus) for bus in self.buses.values())
        lines_str = "\n".join(str(line) for line in self.lines.values())
        gen_units_str = "\n".join(str(gen) for gen in self.generationUnits.values())
        storage_units_str = "\n".join(str(storage) for storage in self.storageUnits.values())
        return f"## PowerModel:\n-- Buses:\n{buses_str}\-- Lines:\n{lines_str}\n-- Generation Units:\n{gen_units_str}\n-- Storage Units:\n{storage_units_str}"

    @staticmethod
    def fromPandapowerModel(network: pandapowerNet) -> 'PowerModel':
        model = PowerModel()

        for i in range(len(network.bus)):
            bus = network.bus.iloc[i]
            model.addBus(i, bus["name"], bus["vn_kv"])

        for i in range(len(network.line)):
            line = network.line.iloc[i]
            model.addLine(
                id=i,
                name=line["name"],
                fromBusId=line["from_bus"],
                toBusId=line["to_bus"],
                maxCurrentKA=line["max_i_ka"]
            )
        
        for i in range(len(network.sgen)):
            gen = network.sgen.iloc[i]
            genType: GenType = None
            if gen["type"] == "WP":
                genType = GenType.WIND
            elif gen["type"] == "PV":
                genType = GenType.PV
            elif gen["type"] == "hydro":
                genType = GenType.HYDRO
            elif gen["type"] == "CHP diesel":
                genType = GenType.THERMAL
            else:
                genType = GenType.OTHER

            model.addGenerationUnit(
                id=i,
                name=gen["name"],
                busId=gen["bus"],
                genType=genType,
                maxApparentPowerKva=gen["sn_mva"] * 1000  # Convert MVA to kVA
            )

        for i in range(len(network.storage)):
            storage = network.storage.iloc[i]
            model.addStorageUnit(
                id=i,
                name=storage["name"],
                busId=storage["bus"],
                activePowerKw=storage["p_mw"] * 1000,  # Convert MW to kW
                reactivePowerKvar=storage["q_mvar"] * 1000,  # Convert MVar to kVar
                maxApparentPowerKva=storage["sn_mva"] * 1000  # Convert MVA to kVA
            )

        for i in range(len(network.load)):
            load = network.load.iloc[i]
            model.addLoad(
                id=i,
                name=load["name"],
                busId=load["bus"],
                activePowerKw=load["p_mw"] * 1000,  # Convert MW to kW
                reactivePowerKvar=load["q_mvar"] * 1000,  # Convert MVar to kVar
                maxApparentPowerKva=load["sn_mva"] * 1000  # Convert MVA to kVA
            )

        return model
        
class SplitMethod(Enum):
    BUS = "bus"

class Split:
    # Tresholds according to CEI 0-16
    powerGenTresholdAllKw: float = 1000
    powerGenTresholdKw: float = 100
    powerStoTresholdKw: float = 50

    def __init__(self, name: str):
        self.name = name
        self.splitMethod: SplitMethod | None = None
        self.buses:  dict[int, Bus] = {}
        self.generationUnits:  dict[int, GenerationUnit] = {}
        self.storageUnits:  dict[int, StorageUnit] = {}
        self.lines: dict[int, Line] = {}

    def setSplitMethod(self, splitMethod: SplitMethod):
        self.splitMethod = splitMethod

    def addBus(self, bus: Bus):
        self.buses[bus.id] = bus
    
    def addLine(self, line: Line):
        if line.fromBusId not in self.buses.keys():
            raise NonExistingBusException(line.fromBusId)
        
        self.lines[line.id] = line

    def addGenerationUnit(self, genUnit: GenerationUnit):
        if genUnit.busId not in self.buses.keys():
            raise NonExistingBusException(genUnit.busId)
        self.generationUnits[genUnit.id] = genUnit

    def addStorageUnit(self, storageUnit: StorageUnit):
        if storageUnit.busId not in self.buses.keys():
            raise NonExistingBusException(storageUnit.busId)
        self.storageUnits[storageUnit.id] = storageUnit
    
    # Get the maximum active power that can be absorbed
    def getMaxAbsPowerKw(self, powerFactor: float = 0.95) -> float:
        totalAbsPowerKw: float = sum(storage.getMaxActivePowerKw(powerFactor) for storage in self.storageUnits.values())
        return totalAbsPowerKw
    
    # Get the maximum active power that can be generated
    def getMaxGenPowerKw(self, powerFactor: float = 0.95) -> float:
        totalImmPowerKw: float = sum(gen.getMaxActivePowerKw(powerFactor) for gen in self.generationUnits.values())
        return totalImmPowerKw
    
    def getMaxInductivePowerKvar(self, powerFactor: float = 0.95) -> float:
        # Inductive support is the aggregated positive reactive capability.
        genQ: float = sum(gen.getMaxReactivePowerKvar(powerFactor) for gen in self.generationUnits.values())
        stoQ: float = sum(storage.getMaxReactivePowerKvar(powerFactor) for storage in self.storageUnits.values())
        return genQ + stoQ

    def getMaxCapacitivePowerKvar(self, powerFactor: float = 0.95) -> float:
        # With symmetric Q capability assumptions, capacitive and inductive magnitudes are equal.
        return self.getMaxInductivePowerKvar(powerFactor)

    def getMaxReactivePowerKvar(self, powerFactor: float = 0.95) -> float:
        return self.getMaxInductivePowerKvar(powerFactor)

    def getMaxApparentPowerKva(self) -> float:
        maxImmP = self.getMaxGenPowerKw()
        maxAssP = self.getMaxAbsPowerKw()
        maxIndQ = self.getMaxInductivePowerKvar()
        maxCapQ = self.getMaxCapacitivePowerKvar()

        # CEI 0-16 conventional base power at PdC:
        # Smax = sqrt(max(Pimm^2, Pass^2) + max(Qind^2, Qcap^2))
        return math.sqrt(max(maxImmP**2, maxAssP**2) + max(maxIndQ**2, maxCapQ**2))
    
    def getObsGenUnits(self) -> dict[int, (int, GenerationUnit)]:
        # Return only the generation units whose active power surpasses the observability treshold
        obsGenUnits: dict[int, GenerationUnit] = {}
        i = 1
        for id, gen in self.generationUnits.items():
            if gen.getMaxActivePowerKw() >= Split.powerGenTresholdKw:
                obsGenUnits[id] = (i, gen)
                i += 1
        return obsGenUnits
    
    def genGenUnitsPerType(self, genType: GenType) -> dict[int, GenerationUnit]:
        genUnitsPerType: dict[int, GenerationUnit] = {}
        for id, gen in self.generationUnits.items():
            if gen.genType == genType:
                genUnitsPerType[id] = gen
        return genUnitsPerType

    def getStoUnits(self) -> dict[int, StorageUnit]:
        return self.storageUnits
    
    def getMainBus(self) -> Bus | None:
        if len(self.buses) > 0:
            return self.buses[list(self.buses)[0]]
        return None

    def getLines(self) -> dict[int, Line]:
        return self.lines
    
    @staticmethod
    def fromPowerModelSplit(powerModel: PowerModel, splitMethod: SplitMethod) -> list['Split']:
        splits: list[Split] = []
        
        if splitMethod == SplitMethod.BUS:
            for bus in powerModel.buses.values():
                split = Split(name=f"CCI_Bus_{bus.id}")
                split.setSplitMethod(SplitMethod.BUS)
                split.addBus(bus)
                for line in powerModel.lines.values():
                    # Add lines whose bus is in the direction of HV
                    if line.fromBusId == bus.id:
                        split.addLine(line)

                for gen in powerModel.generationUnits.values():
                    if gen.busId == bus.id:
                        split.addGenerationUnit(gen)

                for storage in powerModel.storageUnits.values():
                    if storage.busId == bus.id:
                        split.addStorageUnit(storage)

                # A CCI must be installed only if the aggregated nominal power of per generation types surpasses 1000kW
                # For PV and Wind unit the treshold is 100kW 
                isInstalled = False
                for genType in GenType:
                    genUnitsPerType = split.genGenUnitsPerType(genType)
                    if genType in [GenType.PV, GenType.WIND]:
                        if sum(gen.getMaxActivePowerKw() for gen in genUnitsPerType.values()) >= Split.powerGenTresholdKw:
                            isInstalled = True
                    else:
                        if sum(gen.getMaxActivePowerKw() for gen in genUnitsPerType.values()) >= Split.powerGenTresholdAllKw:
                            isInstalled = True
                if isInstalled:
                    splits.append(split)

        else:
            raise NotImplementedError(f"Split method {splitMethod} not implemented yet.")

        return splits
    
    def __str__(self):
        # Print each element in a different line
        buses_str = "\n".join(str(bus) for bus in self.buses.values())
        lines_str = "\n".join(str(line) for line in self.lines.values())
        gen_units_str = "\n".join(str(gen) for gen in self.generationUnits.values())
        storage_units_str = "\n".join(str(storage) for storage in self.storageUnits.values())
        return f"## Split {self.name}:\n- Buses:\n{buses_str}\n- Lines:\n{lines_str}\n- Generation Units:\n{gen_units_str}\n- Storage Units:\n{storage_units_str}"

    
