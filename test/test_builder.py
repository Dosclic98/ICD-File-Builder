from icdbuilder.utils import create_cigre_network_mv_all_der
from icdbuilder.model.power import SplitMethod
from icdbuilder.builder import FromPPToICDBuilder, FromPPToBinderBuilder, ForAggregatorBinderBuilder, ForAggregatorICDBuilder
from pathlib import Path


if __name__ == "__main__":
    net = create_cigre_network_mv_all_der()
    bldr = FromPPToICDBuilder(net)
    busSplits = bldr.build(splitMethod=SplitMethod.BUS, outputPath=Path("output", "bus_split"))

    bindingsBuilder = FromPPToBinderBuilder(net)
    bindingsBuilder.build(splitMethod=SplitMethod.BUS, outputPath=Path("output", "bus_split_bindings"))

    aggrBindingsBuilder = ForAggregatorBinderBuilder()
    aggrBindingsBuilder.build(cciName="CCI_Main", outputPath=Path("output", "aggregator_bindings"))

    aggrICDBuilder = ForAggregatorICDBuilder()
    aggrICDBuilder.build(cciName="CCI_Main", outputPath=Path("output", "aggregator"))
    