from enum import Enum
from typing import Union

class HealthType(Enum):
    OK = 1
    WARNING = 2
    ALARM = 3

class ManipulationFunctionType(Enum):
    DIRECT = "direct" 
    SUM = "sum"
    WEIGHTED_SUM = "weighted_sum"
    S2H = "s2h"

class ManipulationFunction:

    @staticmethod
    def direct(value, isInverse: bool = False):
        if not isInverse:
            if type(value) in [list] and len(value) == 1:
                return value[0]
            else:
                raise ValueError("Direct manipulation function expects a list of size 1 as input.")
        else:
            return [value]

    @staticmethod
    def sum(values: Union[int, float] | list[Union[int, float]], isInverse: bool = False, numOut: int = 1) -> Union[int, float] | list[Union[int, float]]:
        if not isInverse:
            return sum(values)
        else:
            # Distribute the single value equally over numOut outputs
            if numOut <= 0:
                raise ValueError("numOut must be a positive integer.")
            else:
                return [values / numOut for _ in range(numOut)]

    @staticmethod
    def weightedSum(values: Union[int, float] | list[Union[int, float]], isInverse: bool = False,
                    weights: list[float] | None = None) -> Union[tuple[float, list[float]], list[Union[int, float]]]:
        if not isInverse:
            if not isinstance(values, list):
                raise ValueError("Weighted sum expects a list of values as input.")

            # Input weights are orientation signs (+1/-1) used for net aggregation.
            signs = [1.0 for _ in values] if weights is None else [float(w) for w in weights]
            if len(values) != len(signs):
                raise ValueError("Weighted sum expects values and weights with the same length.")

            aggregate = float(sum(float(v) * s for v, s in zip(values, signs)))

            # Return runtime real weights with orientation included so disaggregation can replay signs.
            # For aggregate != 0: realWeight_i = (orientation_i * value_i) / aggregate.
            if aggregate != 0.0:
                realWeights = [(float(v) * s) / aggregate for v, s in zip(values, signs)]
            else:
                # When aggregate is zero, ratios are undefined; persist signed contributions.
                realWeights = [float(v) * s for v, s in zip(values, signs)]

            return aggregate, realWeights
        else:
            if weights is not None:
                if len(weights) == 0:
                    raise ValueError("Weighted sum inverse expects a non-empty weights list.")
                if values == 0:
                    # For zero aggregate, forward path stored signed contributions.
                    # Without extra info we can reconstruct signed contributions only.
                    return list(weights)
                # For non-zero aggregate, forward path stored (orientation_i * value_i) / aggregate.
                # Output is signed contribution (orientation_i * value_i).
                return [values * w for w in weights]

            raise ValueError("Weighted sum inverse expects stored weights from the aggregation phase.")
    
    @staticmethod
    def serviceToHealth(value, isInverse: bool = False) -> Union[int, list[bool]]:
        if not isInverse:
            return HealthType.OK.value if value else HealthType.ALARM.value
        else:
            return [True] if value == HealthType.OK else [False]

    @staticmethod
    def getFunction(funcType: ManipulationFunctionType):
        if funcType == ManipulationFunctionType.DIRECT:
            return ManipulationFunction.direct
        elif funcType == ManipulationFunctionType.SUM:
            return ManipulationFunction.sum
        elif funcType == ManipulationFunctionType.WEIGHTED_SUM:
            return ManipulationFunction.weightedSum
        elif funcType == ManipulationFunctionType.S2H:
            return ManipulationFunction.serviceToHealth
        else:
            raise ValueError(f"Unsupported manipulation function type: {funcType}")