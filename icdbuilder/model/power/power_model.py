from enum import Enum
from dataclasses import dataclass
from pandapower import pandapowerNet

class GenType(Enum):
    THERMAL = "thermal"
    HYDRO = "hydro"
    PV = "photovoltaic"
    WIND = "wind"

class SplitMethod(Enum):
    BUS = "bus"
    UNIT = "unit"

class NonExistingBusException(Exception):
    def __init__(self, busId: int):
        super().__init__(f"Bus with ID {busId} does not exist in the PowerModel.")

@dataclass
class Bus:
    id: int
    name: str
    voltageLevelKv: float

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
    
    def addBus(self, id: int, name: str, voltageLevelKv: float):
        self.buses[id] = Bus(id, name, voltageLevelKv)
    
    def addGenerationUnit(self, id: int, name: str, busId: int, genType: GenType, installedCapacityKw: float):
        if busId not in self.buses.keys():
            raise NonExistingBusException(busId)
        self.generationUnits[id] = GenerationUnit(id, name, busId, genType, installedCapacityKw)

    def addStorageUnit(self, id: int, name: str, busId: int, capacityKwh: float, maxPowerKw: float):
        if busId not in self.buses.keys():
            raise NonExistingBusException(busId)
        self.storageUnits[id] = StorageUnit(id, name, busId, capacityKwh, maxPowerKw)

    @staticmethod
    def fromPandapowerModel(network: pandapowerNet) -> 'PowerModel':
        return PowerModel()