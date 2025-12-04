# TODO: Add alarm bindings for those alarms not having a default 
# value and that must be connected to a pandapower value (e.g. 
# health state of the single generators)  

# Active power template for a single generator measurement
singleGenMeasTemplate = "LD_Plant$SGGMMXU{inst}$MX$TotW"
# Identifier template for a single generator
singleGenIdTemplate = "LD_Plant$SSGGDGEN{inst}$ST$GnGrId"

# Active power template for per-gen type generation measurement
perGenTypeTotPTemplate = "LD_Plant${genType}MMXU1$MX$TotW"
# Active power template for storage measurement
stoTotPStr = "LD_Plant$StMMXU1$MX$TotW"

# Active power template @ PdC measurement
pdcTotPStr = "LD_Plant$PdCMMXU1$MX$TotW"
# Reactive power template @ PdC measurement
pdcTotQStr = "LD_Plant$PdCMMXU1$MX$TotVAr"
# Live voltages template @ PdC measurement array
pdcVoltStr = "LD_Plant$PdCMMXU1$MX$PPV" #TODO: Fix this. It is not right
# Line currents template @ PdC measurement array
pdcCurrQStr = "LD_Plant$PdCMMXU1$MX$A" #TODO: Fix this. It is not right