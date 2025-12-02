from icdbuilder.utils import create_cigre_network_mv_all_der
from icdbuilder.model.power import SplitMethod
from icdbuilder.builder import FromPPToICDBuilder, FromPPToBinderBuilder
from pathlib import Path


if __name__ == "__main__":
    net = create_cigre_network_mv_all_der()
    bldr = FromPPToICDBuilder(net)
    busSplits = bldr.build(splitMethod=SplitMethod.BUS, outputPath=Path("output", "bus_split"))
    unitSplits = bldr.build(splitMethod=SplitMethod.UNIT, outputPath=Path("output", "unit_split"))

    bindingsBuilder = FromPPToBinderBuilder(net)
    bindingsBuilder.build(splitMethod=SplitMethod.BUS, outputPath=Path("output", "bus_split_bindings"))
    bindingsBuilder.build(splitMethod=SplitMethod.UNIT, outputPath=Path("output", "unit_split_bindings"))
    