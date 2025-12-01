# ICD-File-Builder
Tool to automate IED Capability Description (ICD) file generation starting from a pandapower model and according to the CEI 0-16 norm. 

## Installation
To install the package, run the following command:
```bash
pip install git+https://github.com/Dosclic98/ICD-File-Builder.git#egg=icdbuilder
```

## Usage
You can use the package by importing it in your Python script. 
At the moment just the creation of ICD files from pandapower models is supported.
Here's a simple example:

```python
from icdbuilder.utils import create_cigre_network_mv_all_der
from icdbuilder.model.power import SplitMethod
from icdbuilder.builder import FromPPToICDBuilder
from pathlib import Path

if __name__ == "__main__":
    # Create ICD files from a pandapower model
    bldr = FromPPToICDBuilder(create_cigre_network_mv_all_der())

    # Build ICD files with different splitting methods (per-bus and per-unit)
    bldr.build(splitMethod=SplitMethod.BUS, outputPath=Path("output", "bus_split"))
    bldr.build(splitMethod=SplitMethod.UNIT, outputPath=Path("output", "unit_split"))
```