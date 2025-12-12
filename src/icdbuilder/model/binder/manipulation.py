from enum import Enum
from typing import Union

class HealthType(Enum):
    OK = 1
    WARNING = 2
    ALARM = 3

class ManipulationFunctionType(Enum):
    DIRECT = "direct" 
    SUM = "sum"
    S2H = "s2h"

class ManipulationFunction:

    @staticmethod
    def direct(value):
        if type(value) in [list] and len(value) == 1:
            return value[0]
        else:
            raise ValueError("Direct manipulation function expects a list of size 1 as input.")

    @staticmethod
    def sum(values: list[Union[int, float]]) -> Union[int, float]:
        return sum(values)
    
    @staticmethod
    def serviceToHealth(value, isInverse: bool = False):
        if not isInverse:
            return HealthType.OK.value if value else HealthType.ALARM.value
        else:
            return True if value == HealthType.OK else False
    
    @staticmethod
    def getFunction(funcType: ManipulationFunctionType):
        if funcType == ManipulationFunctionType.DIRECT:
            return ManipulationFunction.direct
        elif funcType == ManipulationFunctionType.SUM:
            return ManipulationFunction.sum
        elif funcType == ManipulationFunctionType.S2H:
            return ManipulationFunction.serviceToHealth
        else:
            raise ValueError(f"Unsupported manipulation function type: {funcType}")