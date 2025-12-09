from enum import Enum

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
        return value

    @staticmethod
    def sum(*args):
        return sum(args)
    
    @staticmethod
    def serviceToHealth(value, isInverse: bool = False):
        if not isInverse:
            return HealthType.OK if value else HealthType.ALARM
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