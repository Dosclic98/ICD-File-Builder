# Health template for a single generator
singleGenHealthTemplate = "LD_Plant$SSGGDGEN{inst}$ST$Health$stVal"
# Active power template for a single generator measurement
singleGenMeasTemplate = "LD_Plant$SGGMMXU{inst}$MX$TotW$mag$f"
# Identifier template for a single generator
singleGenIdTemplate = "LD_Plant$SSGGDGEN{inst}$ST$GnGrId$stVal"

# Active power template for per-gen type generation measurement
perGenTypeTotPTemplate = "LD_Plant${genType}MMXU1$MX$TotW$mag$f"
# Active power template for storage measurement
stoTotPStr = "LD_Plant$StMMXU1$MX$TotW$mag$f"

# Active power template @ PdC measurement
pdcTotPStr = "LD_Plant$PdCMMXU1$MX$TotW$mag$f"
# Reactive power template @ PdC measurement
pdcTotQStr = "LD_Plant$PdCMMXU1$MX$TotVAr$mag$f"

# I'm kind of improperly using the following two data attributes but 
# that's the best solution i have currently found
# Live voltages (magnitude and angles) template @ PdC measurement for each phase
pdcVoltMagStrs = ["LD_Plant$PdCMMXU1$MX$PPV$phsAB$cVal$mag$f", "LD_Plant$PdCMMXU1$MX$PPV$phsBC$cVal$mag$f", "LD_Plant$PdCMMXU1$MX$PPV$phsCA$cVal$mag$f"]
pdcVoltAngStrs = ["LD_Plant$PdCMMXU1$MX$PPV$phsAB$cVal$ang$f", "LD_Plant$PdCMMXU1$MX$PPV$phsBC$cVal$ang$f", "LD_Plant$PdCMMXU1$MX$PPV$phsCA$cVal$ang$f"]
# Line currents template @ PdC measurement array
pdcCurrMagStrs = ["LD_Plant$PdCMMXU1$MX$A$phsA$cVal$mag$f", "LD_Plant$PdCMMXU1$MX$A$phsB$cVal$mag$f", "LD_Plant$PdCMMXU1$MX$A$phsC$cVal$mag$f"]

# Reactive power setpoint attributes (respectively for read and write poerations)
qSetReadStr = "LD_Plant$VArSdDVAR1$VArTgtSptPct$mxVal$f"
qSetWriteStr = "LD_Plant$VArSdDVAR1$VArTgtSptPct$Oper$ctlVal$f"