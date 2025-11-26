from icdbuilder.utils import create_cigre_network_mv_all_der
from icdbuilder.model.power import SplitMethod
from icdbuilder.builder import FromPPToICDBuilder
from pathlib import Path


if __name__ == "__main__":
    bldr = FromPPToICDBuilder(create_cigre_network_mv_all_der())
    bldr.build(splitMethod=SplitMethod.BUS, outputPath=Path("output", "bus_split"))
    bldr.build(splitMethod=SplitMethod.UNIT, outputPath=Path("output", "unit_split"))