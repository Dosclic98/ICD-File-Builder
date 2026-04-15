# Health template for a single generator
singleGenHealthTemplate = "LD_Plant$SSGGDGEN{inst}$ST$Health$stVal"
singleGenHealthTimeTemplate = "LD_Plant$SSGGDGEN{inst}$ST$Health$t"
# Active power template for a single generator measurement
singleGenMeasTemplate = "LD_Plant$SGGMMXU{inst}$MX$TotW$mag$f"
singleGenMeasTimeTemplate = "LD_Plant$SGGMMXU{inst}$MX$TotW$t"
# Identifier template for a single generator
singleGenIdTemplate = "LD_Plant$SSGGDGEN{inst}$ST$GnGrId$stVal"
singleGenIdTimeTemplate = "LD_Plant$SSGGDGEN{inst}$ST$GnGrId$t"

# Availability templates for installation and macro-groups
plantAvailStr = "LD_Plant$DisFRDECP1$ST$Beh$stVal"
plantAvailTimeStr = "LD_Plant$DisFRDECP1$ST$Beh$t"
genAvailStr = "LD_Plant$DisFRDGEN1$ST$Beh$stVal"
genAvailTimeStr = "LD_Plant$DisFRDGEN1$ST$Beh$t"
stoAvailStr = "LD_Plant$DisFRDSTO1$ST$Beh$stVal"
stoAvailTimeStr = "LD_Plant$DisFRDSTO1$ST$Beh$t"

# Active power template for per-gen type generation measurement
perGenTypeTotPTemplate = "LD_Plant${genType}MMXU1$MX$TotW$mag$f"
perGenTypeTotPTimeTemplate = "LD_Plant${genType}MMXU1$MX$TotW$t"

# Active power template for storage measurement
stoTotPStr = "LD_Plant$StMMXU1$MX$TotW$mag$f"
stoToPTimeStr = "LD_Plant$StMMXU1$MX$TotW$t"

# Active power template @ PdC measurement
pdcTotPStr = "LD_Plant$PdCMMXU1$MX$TotW$mag$f"
pdcTotPTimeStr = "LD_Plant$PdCMMXU1$MX$TotW$t"
# Reactive power template @ PdC measurement
pdcTotQStr = "LD_Plant$PdCMMXU1$MX$TotVAr$mag$f"
pdcTotQTimeStr = "LD_Plant$PdCMMXU1$MX$TotVAr$t"

# I'm kind of improperly using the following two data attributes but 
# that's the best solution i have currently found
# Live voltages (magnitude and angles) template @ PdC measurement for each phase
pdcVoltMagStrs = ["LD_Plant$PdCMMXU1$MX$PPV$phsAB$cVal$mag$f", "LD_Plant$PdCMMXU1$MX$PPV$phsBC$cVal$mag$f", "LD_Plant$PdCMMXU1$MX$PPV$phsCA$cVal$mag$f"]
pdcVoltMagTimeStrs = ["LD_Plant$PdCMMXU1$MX$PPV$phsAB$t", "LD_Plant$PdCMMXU1$MX$PPV$phsBC$t", "LD_Plant$PdCMMXU1$MX$PPV$phsCA$t"]
pdcVoltAngStrs = ["LD_Plant$PdCMMXU1$MX$PPV$phsAB$cVal$ang$f", "LD_Plant$PdCMMXU1$MX$PPV$phsBC$cVal$ang$f", "LD_Plant$PdCMMXU1$MX$PPV$phsCA$cVal$ang$f"]
pdcVoltAngTimeStrs = ["LD_Plant$PdCMMXU1$MX$PPV$phsAB$t", "LD_Plant$PdCMMXU1$MX$PPV$phsBC$t", "LD_Plant$PdCMMXU1$MX$PPV$phsCA$t"]

# Line currents template @ PdC measurement array
pdcCurrMagStrs = ["LD_Plant$PdCMMXU1$MX$A$phsA$cVal$mag$f", "LD_Plant$PdCMMXU1$MX$A$phsB$cVal$mag$f", "LD_Plant$PdCMMXU1$MX$A$phsC$cVal$mag$f"]
pdcCurrMagTimeStrs = ["LD_Plant$PdCMMXU1$MX$A$phsA$t", "LD_Plant$PdCMMXU1$MX$A$phsB$t", "LD_Plant$PdCMMXU1$MX$A$phsC$t"]

# Reactive power setpoint attributes (respectively for read and write poerations)
qSetReadStr = "LD_Plant$VArSdDVAR1$VArTgtSptPct$mxVal$f"
qSetReadTimeStr = "LD_Plant$VArSdDVAR1$VArTgtSptPct$t"
qSetWriteStr = "LD_Plant$VArSdDVAR1$VArTgtSptPct$Oper$ctlVal$f"
qSetWriteTimeStr = "LD_Plant$VArSdDVAR1$VArTgtSptPct$Oper$T"

# DAGC1 (WSa prefix): active power control function state and setpoint at aggregator side.
# Beh: function availability/behavior state (ENS/stVal)
dagcBehReadStr = "LD_Plant$WSaDAGC1$ST$Beh$stVal"
dagcBehReadTimeStr = "LD_Plant$WSaDAGC1$ST$Beh$t"
# Health: logical node health state (ENS/stVal)
dagcHealthReadStr = "LD_Plant$WSaDAGC1$ST$Health$stVal"
dagcHealthReadTimeStr = "LD_Plant$WSaDAGC1$ST$Health$t"
# FctOpSt: function operational status (ENS/stVal)
dagcFctOpStReadStr = "LD_Plant$WSaDAGC1$ST$FctOpSt$stVal"
dagcFctOpStReadTimeStr = "LD_Plant$WSaDAGC1$ST$FctOpSt$t"
# Mod: function activation mode [typically 1=on, 5=off]
dagcModReadStr = "LD_Plant$WSaDAGC1$ST$Mod$stVal"
dagcModReadTimeStr = "LD_Plant$WSaDAGC1$ST$Mod$t"
dagcModWriteStr = "LD_Plant$WSaDAGC1$ST$Mod$Oper$ctlVal$f"
dagcModWriteTimeStr = "LD_Plant$WSaDAGC1$ST$Mod$Oper$T"
# WSptPct: active power setpoint in percentage of Smax (APC)
aggPSetReadStr = "LD_Plant$WSaDAGC1$WSptPct$mxVal$f"
aggPSetReadTimeStr = "LD_Plant$WSaDAGC1$WSptPct$t"
aggPSetWriteStr = "LD_Plant$WSaDAGC1$WSptPct$Oper$ctlVal$f"
aggPSetWriteTimeStr = "LD_Plant$WSaDAGC1$WSptPct$Oper$T"

# DVAR1 (VArSa prefix): reactive power control function state at aggregator side.
# Reactive power setpoint attributes for Aggregator-reserved DVAR1 (VArSa prefix)
aggQSetReadStr = "LD_Plant$VArSaDVAR1$VArTgtSptPct$mxVal$f"
aggQSetReadTimeStr = "LD_Plant$VArSaDVAR1$VArTgtSptPct$t"
aggQSetWriteStr = "LD_Plant$VArSaDVAR1$VArTgtSptPct$Oper$ctlVal$f"
aggQSetWriteTimeStr = "LD_Plant$VArSaDVAR1$VArTgtSptPct$Oper$T"
# Beh: function availability/behavior state (ENS/stVal)
dvarBehReadStr = "LD_Plant$VArSaDVAR1$ST$Beh$stVal"
dvarBehReadTimeStr = "LD_Plant$VArSaDVAR1$ST$Beh$t"
# Health: logical node health state (ENS/stVal)
dvarHealthReadStr = "LD_Plant$VArSaDVAR1$ST$Health$stVal"
dvarHealthReadTimeStr = "LD_Plant$VArSaDVAR1$ST$Health$t"
# FctOpSt: function operational status (ENS/stVal)
dvarFctOpStReadStr = "LD_Plant$VArSaDVAR1$ST$FctOpSt$stVal"
dvarFctOpStReadTimeStr = "LD_Plant$VArSaDVAR1$ST$FctOpSt$t"
# Mod: function activation mode [typically 1=on, 5=off]
dvarModReadStr = "LD_Plant$VArSaDVAR1$ST$Mod$stVal"
dvarModReadTimeStr = "LD_Plant$VArSaDVAR1$ST$Mod$t"
dvarModWriteStr = "LD_Plant$VArSaDVAR1$ST$Mod$Oper$ctlVal$f"
dvarModWriteTimeStr = "LD_Plant$VArSaDVAR1$ST$Mod$Oper$T"
