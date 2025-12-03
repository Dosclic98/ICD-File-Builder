from enum import Enum
from dataclasses import dataclass
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
    installedCapacityKw: float

@dataclass
class StorageUnit:
    id: int
    name: str
    busId: int
    capacityKwh: float
    maxPowerKw: float

class PowerModel:
    def __init__(self):
        self.buses: dict = {}
        self.generationUnits: dict = {}
        self.storageUnits: dict = {}
        self.lines: dict = {}
    
    def addBus(self, id: int, name: str, voltageLevelKv: float):
        self.buses[id] = Bus(id, name, voltageLevelKv)

    def addLine(self, id: int, name: str, fromBusId: int, toBusId: int, maxCurrentKA: float):
        if fromBusId not in self.buses.keys():
            raise NonExistingBusException(fromBusId)
        if toBusId not in self.buses.keys():
            raise NonExistingBusException(toBusId)
        self.lines[id] = Line(id, name, fromBusId, toBusId, maxCurrentKA)
    
    def addGenerationUnit(self, id: int, name: str, busId: int, genType: GenType, installedCapacityKw: float):
        if busId not in self.buses.keys():
            raise NonExistingBusException(busId)
        self.generationUnits[id] = GenerationUnit(id, name, busId, genType, installedCapacityKw)

    def addStorageUnit(self, id: int, name: str, busId: int, capacityKwh: float, maxPowerKw: float):
        if busId not in self.buses.keys():
            raise NonExistingBusException(busId)
        self.storageUnits[id] = StorageUnit(id, name, busId, capacityKwh, maxPowerKw)

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
                installedCapacityKw=gen["p_mw"] * 1000  # Convert MVA to kW
            )

        for i in range(len(network.storage)):
            storage = network.storage.iloc[i]
            model.addStorageUnit(
                id=i,
                name=storage["name"],
                busId=storage["bus"],
                capacityKwh=storage["max_e_mwh"] * 1000,  # Convert MWh to kWh
                maxPowerKw=storage["p_mw"] * 1000  # Convert MW to kW
            )

        return model
        
class SplitMethod(Enum):
    BUS = "bus"
    UNIT = "unit"

class Split:
    # Tresholds according to 
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

    def getMaxGenerationCapacityKw(self) -> float:
        totalCapacityKw: float = 0.0
        for gen in self.generationUnits.values():
            totalCapacityKw += gen.installedCapacityKw
        return totalCapacityKw
    
    def getMaxReactivePowerKw(self, powerFactor: float = 0.95) -> float:
        totalReactivePowerKw: float = self.getMaxGenerationCapacityKw() * ((1-powerFactor**2)**0.5 / powerFactor)
        
        return totalReactivePowerKw
    
    def getMaxNominalPowerKw(self) -> float:
        totalPowerKw: float = (self.getMaxGenerationCapacityKw()**2 + self.getMaxReactivePowerKw()**2)**0.5
        return totalPowerKw
    
    def getObsGenUnits(self) -> dict[int, (int, GenerationUnit)]:
        # Return only the generation units whose active power surpasses the observability treshold
        obsGenUnits: dict[int, GenerationUnit] = {}
        i = 1
        for id, gen in self.generationUnits.items():
            if gen.installedCapacityKw >= Split.powerGenTresholdKw:
                obsGenUnits[id] = (i, gen)
                i += 1
        return obsGenUnits
    
    def genGenUnitsPerType(self, genType: GenType) -> dict[int, GenerationUnit]:
        genUnitsPerType: dict[int, GenerationUnit] = {}
        for id, gen in self.generationUnits.items():
            if gen.genType == genType:
                genUnitsPerType[id] = gen
        return genUnitsPerType
    
    @staticmethod
    def fromPowerModelSplit(powerModel: PowerModel, splitMethod: SplitMethod) -> list['Split']:
        splits: list[Split] = []
        
        if splitMethod == SplitMethod.BUS:
            for bus in powerModel.buses.values():
                split = Split(name=f"Split_Bus_{bus.id}")
                split.setSplitMethod(SplitMethod.BUS)
                split.addBus(bus)
                for line in powerModel.lines.values():
                    # Add lines whose bus is in the direction of HV
                    if line.fromBusId == bus.id:
                        split.addLine(line)

                existsValidGen = False
                for gen in powerModel.generationUnits.values():
                    if gen.busId == bus.id:
                        if gen.installedCapacityKw >= Split.powerGenTresholdKw:
                            existsValidGen = True
                        split.addGenerationUnit(gen)

                existsValidSto = False
                for storage in powerModel.storageUnits.values():
                    if storage.busId == bus.id:
                        if storage.maxPowerKw >= Split.powerStoTresholdKw:
                            existsValidSto = True
                        split.addStorageUnit(storage)

                if existsValidGen or existsValidSto:
                    splits.append(split)

        elif splitMethod == SplitMethod.UNIT:
            for gen in powerModel.generationUnits.values():
                if gen.installedCapacityKw >= Split.powerGenTresholdKw:    
                    split = Split(name=f"Split_Gen_{gen.id}")
                    split.setSplitMethod(SplitMethod.UNIT)
                    split.addBus(powerModel.buses[gen.busId])
                    split.addGenerationUnit(gen)
                    splits.append(split)

            for storage in powerModel.storageUnits.values():
                if storage.maxPowerKw >= Split.powerStoTresholdKw:
                    split = Split(name=f"Split_Storage_{storage.id}")
                    split.setSplitMethod(SplitMethod.UNIT)
                    split.addBus(powerModel.buses[storage.busId])
                    split.addStorageUnit(storage)
                    splits.append(split)

            # Add lines of the present busses in each split
            for split in splits:
                # Add lines whose bus is in the direction of HV
                for bus in split.buses.values():
                    for line in powerModel.lines.values():
                        if line.fromBusId == bus.id:
                            split.addLine(line)

        return splits
    
    def __str__(self):
        # Print each element in a different line
        buses_str = "\n".join(str(bus) for bus in self.buses.values())
        lines_str = "\n".join(str(line) for line in self.lines.values())
        gen_units_str = "\n".join(str(gen) for gen in self.generationUnits.values())
        storage_units_str = "\n".join(str(storage) for storage in self.storageUnits.values())
        return f"## Split {self.name}:\n- Buses:\n{buses_str}\n- Lines:\n{lines_str}\n- Generation Units:\n{gen_units_str}\n- Storage Units:\n{storage_units_str}"

    
