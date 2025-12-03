from enum import Enum

class ManipulationFunctionType(Enum):
    DIRECT = "direct" 
    SUM = "sum"

class ManipulationFunction:

    @staticmethod
    def direct(value):
        return value

    @staticmethod
    def sum(*args):
        return sum(args)
    
    @staticmethod
    def getFunction(funcType: ManipulationFunctionType):
        if funcType == ManipulationFunctionType.DIRECT:
            return ManipulationFunction.direct
        elif funcType == ManipulationFunctionType.SUM:
            return ManipulationFunction.sum
        else:
            raise ValueError(f"Unsupported manipulation function type: {funcType}")