# Health template for a single generator
singleGenHealthTemplate = "LD_Plant$SSGGDGEN{inst}$ST$Health$stVal"
singleGenHealthTimeTemplate = "LD_Plant$SSGGDGEN{inst}$ST$Health$t"
# Active power template for a single generator measurement
singleGenMeasTemplate = "LD_Plant$SGGMMXU{inst}$MX$TotW$mag$f"
singleGenMeasTimeTemplate = "LD_Plant$SGGMMXU{inst}$MX$TotW$t"
# Identifier template for a single generator
singleGenIdTemplate = "LD_Plant$SSGGDGEN{inst}$ST$GnGrId$stVal"
singleGenIdTimeTemplate = "LD_Plant$SSGGDGEN{inst}$ST$GnGrId$t"

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
