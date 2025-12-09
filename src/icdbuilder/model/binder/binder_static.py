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

# I'm kind of improperly using the following two data attributes but 
# that's the best solution i have currently found
# Live voltages (magnitude and angles) template @ PdC measurement for each phase
pdcVoltMagStrs = ["LD_Plant$PdCMMXU1$MX$PPV$phsAB$cVal$mag", "LD_Plant$PdCMMXU1$MX$PPV$phsBC$cVal$mag", "LD_Plant$PdCMMXU1$MX$PPV$phsCA$cVal$mag"]
pdcVoltAngStrs = ["LD_Plant$PdCMMXU1$MX$PPV$phsAB$cVal$ang", "LD_Plant$PdCMMXU1$MX$PPV$phsBC$cVal$ang", "LD_Plant$PdCMMXU1$MX$PPV$phsCA$cVal$ang"]
# Line currents template @ PdC measurement array
pdcCurrMagStrs = ["LD_Plant$PdCMMXU1$MX$A$phsA$cVal$mag", "LD_Plant$PdCMMXU1$MX$A$phsB$cVal$mag", "LD_Plant$PdCMMXU1$MX$A$phsC$cVal$mag"]