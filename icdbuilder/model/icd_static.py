# Subnetwork informations as part of the communication section
subnetwork = \
"""
<SubNetwork name="{subnetwork}" type="8-MMS" desc="">
  <Text>CCI-DSO bus</Text>
  <BitRate unit="b/s">{bitrate}</BitRate>
  <ConnectedAP iedName="CCI016_01" apName="{apName}">
  <Address>
      <P type="IP">{ip}</P>
      <P type="IP-SUBNET">{subnet}</P>
      <P type="IP-GATEWAY">{gateway}</P>
      <P type="OSI-TSEL">0001</P>
      <P type="OSI-PSEL">00000001</P>
      <P type="OSI-SSEL">0001</P>
      <P type="OSI-AP-Title">000</P>
      <P type="OSI-AE-Qualifier">000</P>
  </Address>
  </ConnectedAP>
</SubNetwork>
"""

# Available services on the CCI
services = \
"""
<Services nameLength="64">
  <DynAssociation />
  <GetDirectory />
  <GetDataObjectDefinition />
  <GetDataSetValue />
  <DataSetDirectory />
  <ConfDataSet max="10" maxAttributes="200" modify="false" />
  <ReadWrite />
  <ConfReportControl max="10" bufMode="both" bufConf="false" />
  <GetCBValues />
  <ConfLogControl max="1" />
  <FileHandling />
  <TimerActivatedControl />
  <ClientServices goose="false" gsse="false" bufReport="true" unbufReport="true" readLog="false" sv="false" supportsLdName="true" rGOOSE="false" rSV="false" noIctBinding="false" maxAttributes="200" maxReports="10" >
    <TimeSyncProt sntp="true" c37_238="false" other="false" iec61850_9_3="true" />
  </ClientServices>
  <DataObjectDirectory />
  <ReportSettings cbName="Fix" datSet="Fix" rptID="Fix" optFields="Fix" bufTime="Fix" trgOps="Fix" intgPd="Fix" resvTms="false" owner="false" />
  <ConfLNs fixPrefix="true" fixLnInst="true" />
  <ConfLdName />
</Services>
"""

# Datasets: alarms, PoC measurements and per-generation macro group measurements
# The single generator/storage measurements datasets are missing since they are 
# dynamically inserted based on the connected devices 
datasets: dict = {
    "alarms": """
      <DataSet name="DS_R_Stato_Allarmi_Segnali" desc="Alarm and signal state of the CCI">
      <!-- that is DS_R_Status_Alarms_Signals of the CCI -->
        <FCDA ldInst="LD_Plant" lnClass="DECP" fc="ST" lnInst="1" prefix="DisFR" doName="Beh" />
        <FCDA ldInst="LD_Plant" lnClass="DGEN" fc="ST" lnInst="1" prefix="DisFR" doName="Beh" />
        <FCDA ldInst="LD_Plant" lnClass="DSTO" fc="ST" lnInst="1" prefix="DisFR" doName="Beh" />
        <FCDA ldInst="LD_Plant" lnClass="XCBR" fc="ST" lnInst="1" prefix="IDG" doName="Pos" />
        <FCDA ldInst="LD_Plant" lnClass="DGEN" fc="ST" lnInst="1" prefix="SSGG" doName="Health" />
        <FCDA ldInst="LD_Plant" lnClass="DGEN" fc="ST" lnInst="2" prefix="SSGG" doName="Health" />
        <FCDA ldInst="LD_Plant" lnClass="DWMX" fc="ST" lnInst="1" prefix="Wlim" doName="Beh" />
        <FCDA ldInst="LD_Plant" lnClass="DWMX" fc="ST" lnInst="1" prefix="Wlim" doName="FctOpStAuto" />
        <FCDA ldInst="LD_Plant" lnClass="DWMX" fc="ST" lnInst="1" prefix="Wlim" doName="FctOpStEx" />
        <FCDA ldInst="LD_Plant" lnClass="DAGC" fc="ST" lnInst="1" prefix="WSd" doName="Beh" />
        <FCDA ldInst="LD_Plant" lnClass="DAGC" fc="ST" lnInst="1" prefix="WSd" doName="FctOpSt" />
        <FCDA ldInst="LD_Plant" lnClass="DVAR" fc="ST" lnInst="1" prefix="VArSd" doName="Beh" />
        <FCDA ldInst="LD_Plant" lnClass="DVAR" fc="ST" lnInst="1" prefix="VArSd" doName="FctOpSt" />
        <FCDA ldInst="LD_Plant" lnClass="DFPF" fc="ST" lnInst="1" prefix="PFSP" doName="Beh" />
        <FCDA ldInst="LD_Plant" lnClass="DFPF" fc="ST" lnInst="1" prefix="PFSP" doName="FctOpSt" />
        <FCDA ldInst="LD_Plant" lnClass="DVVR" fc="ST" lnInst="1" prefix="VArV" doName="Beh" />
        <FCDA ldInst="LD_Plant" lnClass="DVVR" fc="ST" lnInst="1" prefix="VArV" doName="FctOpSt" />
        <FCDA ldInst="LD_Plant" lnClass="DPFW" fc="ST" lnInst="1" prefix="PFW" doName="Beh" />
        <FCDA ldInst="LD_Plant" lnClass="DPFW" fc="ST" lnInst="1" prefix="PFW" doName="FctOpSt" />
      </DataSet>
      """,
      "pocPeriodicMeas": """
        <DataSet name="DS_R_PdC_Mis4sec" desc="Measurements at PoC every 4 sec of the CCI">
        <!-- that is DS_R_PoC_Meas4sec of the CCI -->
          <FCDA ldInst="LD_Plant" lnClass="MMXU" fc="MX" lnInst="1" prefix="PdC" doName="TotW" />
          <FCDA ldInst="LD_Plant" lnClass="MMXU" fc="MX" lnInst="1" prefix="PdC" doName="TotVAr" />
          <FCDA ldInst="LD_Plant" lnClass="MMXU" fc="MX" lnInst="1" prefix="PdC" doName="PPV" />
          <FCDA ldInst="LD_Plant" lnClass="MMXU" fc="MX" lnInst="1" prefix="PdC" doName="A" />
        </DataSet>
      """,
      "genAccPeriodicMeas": """
        <DataSet name="DS_R_GenAcc_Mis4sec" desc="Measurements every 4 sec per generation and storage type of the CCI">
        <!-- that is DS_R_GenSto_Meas4sec of the CCI -->
          <FCDA ldInst="LD_Plant" lnClass="MMXU" fc="MX" lnInst="1" prefix="GenPV" doName="TotW" />
          <FCDA ldInst="LD_Plant" lnClass="MMXU" fc="MX" lnInst="1" prefix="GenTer" doName="TotW" />
          <FCDA ldInst="LD_Plant" lnClass="MMXU" fc="MX" lnInst="1" prefix="GenIdr" doName="TotW" />
          <FCDA ldInst="LD_Plant" lnClass="MMXU" fc="MX" lnInst="1" prefix="St" doName="TotW" />
        </DataSet>
      """
}

# Periodic Reports linked to the previously defined datasets
reportControlBlocks = {
    "alarms": """
      <ReportControl name="brcb_Stato_Allarmi_Segnali" confRev="1" datSet="DS_R_Stato_Allarmi_Segnali" rptID="CCI016_01LD_Plant/LLN0.brcb_Stato_Allarmi_Segnali" buffered="true" intgPd="0" bufTime="250" desc="Stato Allarmi e Segnali del CCI">
      <!-- that is brcb_Status_Alarms_Signals of the CCI -->
        <TrgOps dchg="true" qchg="true" gi="true" />
        <OptFields seqNum="true" timeStamp="true" dataSet="true" reasonCode="true" dataRef="true" entryID="true" configRef="true" bufOvfl="true" />
        <RptEnabled max="2" desc="Client DSO" />
      </ReportControl>
    """,
    "pocPeriodicMeas": """
      <ReportControl name="urcb_PdC_Mis4sec" confRev="1" datSet="DS_R_PdC_Mis4sec" rptID="CCI016_01LD_Plant/LLN0.urcb_PdC_Mis4sec" intgPd="4000" bufTime="0" desc="Misure al PdC a 4sec del CCI">
      <!-- that is urcb_PoC_Meas4sec of the CCI -->
        <TrgOps period="true" gi="true" />
        <OptFields seqNum="true" timeStamp="true" dataSet="true" reasonCode="true" dataRef="true" entryID="true" configRef="true" />
        <RptEnabled max="2" desc="Client DSO" />
      </ReportControl>
    """,
    "genAccPeriodicMeas": """
      <ReportControl name="urcb_GenAcc_Mis4sec" confRev="1" datSet="DS_R_GenAcc_Mis4sec" rptID="CCI016_01LD_Plant/LLN0.urcb_GenAcc_Mis4sec" intgPd="4000" bufTime="0" desc="Misure a 4sec per Tipo Generazione e Accumulo del CCI">
      <!-- that is urcb_GenSto_Meas4sec of the CCI -->
        <TrgOps period="true" gi="true" />
        <OptFields seqNum="true" timeStamp="true" dataSet="true" reasonCode="true" dataRef="true" entryID="true" configRef="true" />
        <RptEnabled max="2" desc="Client DSO" />
      </ReportControl>
    """,
    "genSingPeriodicMeas": """
      <ReportControl name="urcb_SingGen_Mis4sec" confRev="1" datSet="DS_R_SingGen_Mis4sec" rptID="CCI016_01LD_Plant/LLN0.urcb_SingGen_Mis4sec" intgPd="4000" bufTime="0" desc="Misure a 4sec per Singolo Generatore del CCI">
      <!-- that is urcb_SingGen_Meas4sec of the CCI -->
        <TrgOps period="true" gi="true" />
        <OptFields seqNum="true" timeStamp="true" dataSet="true" reasonCode="true" dataRef="true" entryID="true" configRef="true" />
        <RptEnabled max="2" desc="Client DSO" />
      </ReportControl>    
    """    
}

ln0OtherDois = \
"""
<DOI name="Mod" desc="">
  <DAI name="stVal">
    <Val>on</Val>
  </DAI>
  <DAI name="ctlModel">
    <Val>status-only</Val>
  </DAI>
</DOI>
<DOI name="Beh" desc="">
  <DAI name="stVal">
    <Val>on</Val>
  </DAI>
</DOI>
<DOI name="Health" desc="">
  <DAI name="stVal">
    <Val>Ok</Val>
  </DAI>
</DOI>
<DOI name="NamPlt" desc="">
  <DAI name="ldNs">
    <Val>IEC 61850-7-4:2007</Val>
  </DAI>
  <DAI name="configRev">
    <Val>V.2.1</Val>
  </DAI>
</DOI>
"""

# CCI device characteristics (manufacturer, software version 
# and connection point identifier)
phyDevInfos = """
<LN lnClass="LPHD" lnType="LPHD1" inst="1" prefix="">
  <DOI name="PhyHealth" desc="">
    <DAI name="stVal">
      <Val>Ok</Val>
    </DAI>
  </DOI>
  <DOI name="PhyNam">
    <DAI name="vendor">
      <Val>DummyVendor_01</Val>
    </DAI>
    <DAI name="swRev">
      <Val>1.0</Val>
    </DAI>
    <DAI name="location">
      <Val>IT000E123456789</Val>
    </DAI>
  </DOI>
</LN>
"""
# Plant characteristics (derived by the power grid elements connected to it)
plantChar = """
<LN lnClass="DPCC" lnType="DPCC1" inst="1" prefix="PdC_Wi">
  <DOI name="NamPlt">
    <DAI name="lnNs">
      <Val>IEC 61850-7-420:2019A</Val>
    </DAI>
  </DOI>
  <DOI name="Beh" desc="">
    <DAI name="stVal">
      <Val>on</Val>
    </DAI>
  </DOI>
  <DOI name="WRtg" desc="PdC - maximum Active Power generated by the Plant (kW)">
<!-- that is PdC - maximum Active Power generated by the Plant (kW) -->
    <SDI name="setMag" desc="">
      <DAI name="f" desc="Valore caratteristico di Impianto">
<!-- that is Plant-specific value -->
        <Val>{maxGenP}</Val>
      </DAI>
    </SDI>
  </DOI>
</LN>
<LN lnClass="DPCC" lnType="DPCC1" inst="1" prefix="PdC_Wa">
  <DOI name="NamPlt">
    <DAI name="lnNs">
      <Val>IEC 61850-7-420:2019A</Val>
    </DAI>
  </DOI>
  <DOI name="Beh" desc="">
    <DAI name="stVal">
      <Val>on</Val>
    </DAI>
  </DOI>
  <DOI name="WRtg" desc="PdC - Maximum active power absorption (kW)">
    <SDI name="setMag" desc="">
<!-- that is ... -->
      <DAI name="f" desc="Plant-characteristic value">
<!-- that is ... -->
        <Val>{maxAbsP}</Val>
      </DAI>
    </SDI>
  </DOI>
</LN>
<LN lnClass="DPCC" lnType="DPCC2" inst="1" prefix="PdC_Qi">
  <DOI name="NamPlt">
    <DAI name="lnNs">
      <Val>IEC 61850-7-420:2019A</Val>
    </DAI>
  </DOI>
  <DOI name="Beh" desc="">
    <DAI name="stVal">
      <Val>on</Val>
    </DAI>
  </DOI>
  <DOI name="VArRtg" desc="PdC - Maximum reactive inductive power (kVAr)">
    <SDI name="setMag" desc="">
      <DAI name="f" desc="Plant-characteristic value">
        <Val>{maxIndQ}</Val>
      </DAI>
    </SDI>
  </DOI>
</LN>
<LN lnClass="DPCC" lnType="DPCC2" inst="1" prefix="PdC_Qc">
  <DOI name="NamPlt">
    <DAI name="lnNs">
      <Val>IEC 61850-7-420:2019A</Val>
    </DAI>
  </DOI>
  <DOI name="Beh" desc="">
    <DAI name="stVal">
      <Val>on</Val>
    </DAI>
  </DOI>
  <DOI name="VArRtg" desc="PdC - Maximum reactive capacitive power (kVAr)">
    <SDI name="setMag" desc="">
      <DAI name="f" desc="Plant-characteristic value">
        <Val>{maxCapQ}</Val>
      </DAI>
    </SDI>
  </DOI>
</LN>
<LN lnClass="DPCC" lnType="DPCC3" inst="1" prefix="PdC_VA">
  <DOI name="NamPlt">
    <DAI name="lnNs">
      <Val>IEC 61850-7-420:2019A</Val>
    </DAI>
  </DOI>
  <DOI name="Beh" desc="">
    <DAI name="stVal">
      <Val>on</Val>
    </DAI>
  </DOI>
  <DOI name="VARtg" desc="PdC - Maximum apparent power (kVA)">
    <SDI name="setMag" desc="">
      <DAI name="f" desc="Plant-characteristic value">
        <Val>{maxS}</Val>
      </DAI>
    </SDI>
  </DOI>
</LN>
"""
# Availability of control functions in general, for generation and for storage macrogroup
ctrlFunAvail = """
<LN lnClass="DECP" lnType="DECP1" inst="1" prefix="DisFR">
  <DOI name="NamPlt">
    <DAI name="lnNs">
      <Val>IEC 61850-7-420:2019A</Val>
    </DAI>
  </DOI>
  <DOI name="Beh" desc="">
    <DAI name="stVal">
      <Val>on</Val>
    </DAI>
  </DOI>
</LN>
<LN lnClass="DGEN" lnType="DGEN1" inst="1" prefix="DisFR">
  <DOI name="NamPlt">
    <DAI name="lnNs">
      <Val>IEC 61850-7-420:2019A</Val>
    </DAI>
  </DOI>
  <DOI name="Beh" desc="">
    <DAI name="stVal">
      <Val>on</Val>
    </DAI>
  </DOI>
</LN>
<LN lnClass="DSTO" lnType="DSTO1" inst="1" prefix="DisFR">
  <DOI name="NamPlt">
    <DAI name="lnNs">
      <Val>IEC 61850-7-420:2019A</Val>
    </DAI>
  </DOI>
  <DOI name="Beh" desc="">
    <DAI name="stVal">
      <Val>on</Val>
    </DAI>
  </DOI>
</LN>
"""

measAvailPerGroup = """
<LN lnClass="MMXU" lnType="MMXU1" inst="1" prefix="PdC">
  <DOI name="Beh" desc="">
    <DAI name="stVal">
      <Val>on</Val>
    </DAI>
  </DOI>
</LN>
<LN lnClass="MMXU" lnType="MMXU2" inst="1" prefix="GenPV">
  <DOI name="Beh" desc="">
    <DAI name="stVal">
      <Val>on</Val>
    </DAI>
  </DOI>
</LN>
<LN lnClass="MMXU" lnType="MMXU2" inst="1" prefix="GenWi">
  <DOI name="Beh" desc="">
    <DAI name="stVal">
      <Val>on</Val>
    </DAI>
  </DOI>
</LN>
<LN lnClass="MMXU" lnType="MMXU2" inst="1" prefix="GenTer">
  <DOI name="Beh" desc="">
    <DAI name="stVal">
      <Val>on</Val>
    </DAI>
  </DOI>
</LN>
<LN lnClass="MMXU" lnType="MMXU2" inst="1" prefix="GenIdr">
  <DOI name="Beh" desc="">
    <DAI name="stVal">
      <Val>on</Val>
    </DAI>
  </DOI>
</LN>
<LN lnClass="MMXU" lnType="MMXU2" inst="1" prefix="St">
  <DOI name="Beh" desc="">
    <DAI name="stVal">
      <Val>on</Val>
    </DAI>
  </DOI>
</LN>
"""

# Measure of P for each generator over the observability treshold (100 kW)
singleGenMeasTemplate = """
<LN lnClass="MMXU" lnType="MMXU2" inst="{ints}" prefix="SGG" desc="Measure of P per single generation group {name}">
  <DOI name="Beh" desc="">
    <DAI name="stVal">
      <Val>on</Val>
    </DAI>
  </DOI>
</LN>
"""

# Should depend on the number of CBRs but for the moment it is set statically
mainCbrStatus = """
<LN lnClass="XCBR" lnType="XCBR1" inst="1" prefix="IDG">
  <DOI name="Beh" desc="">
    <DAI name="stVal">
      <Val>on</Val>
    </DAI>
  </DOI>
  <DOI name="Pos" desc="">
    <DAI name="ctlModel">
      <Val>status-only</Val>
    </DAI>
  </DOI>
  <DOI name="BlkOpn" desc="">
    <DAI name="ctlModel">
      <Val>status-only</Val>
    </DAI>
  </DOI>
  <DOI name="BlkCls" desc="">
    <DAI name="ctlModel">
      <Val>status-only</Val>
    </DAI>
  </DOI>
</LN>
"""

singleGenStatusTemplate = """
<LN lnClass="DGEN" lnType="DGEN2" inst="{inst}" prefix="SSGG" desc="Single Generarion Group {name}">
  <DOI name="NamPlt">
    <DAI name="lnNs">
      <Val>(Tr)IEC 61850-CEI016:2022</Val>
    </DAI>
  </DOI>
  <DOI name="Beh" desc="">
    <DAI name="stVal">
      <Val>on</Val>
    </DAI>
  </DOI>
  <DOI name="Health" desc="Operational Status">
    <DAI name="stVal">
      <Val>Ok</Val>
    </DAI>
  </DOI>
  <DOI name="GnGrId" desc="Identification Number">
    <DAI name="stVal">
      <Val>{inst}</Val>
    </DAI>
  </DOI>
</LN>
"""
# Configuration of the active control function (currently "voltage regulation with respect to Inductive/Capacitive reactive power setpoint")
controlFunConfigTemplate = """
<LN lnClass="DWMX" lnType="DWMX1" inst="1" prefix="Wlim" desc="Control Function - W limitation - from DSO">
  <DOI name="NamPlt">
    <DAI name="lnNs">
      <Val>(Tr)IEC 61850-CEI016:2022</Val>
    </DAI>
  </DOI>
  <DOI name="Beh" desc="">
    <DAI name="stVal">
      <Val>off</Val>
    </DAI>
  </DOI>
  <DOI name="WMaxSptPct" desc="Limit Setopoint of W (percemtage with sign with respect to Smax) [0..100]">
    <DAI name="ctlModel">
      <Val>sbo-with-enhanced-security</Val>
    </DAI>
  </DOI>
  <DOI name="Mod" desc="Activation/deactivation [5 = Inactive, 1 = Active]">
    <DAI name="stVal">
      <Val>off</Val>
    </DAI>
    <DAI name="ctlModel">
      <Val>sbo-with-enhanced-security</Val>
    </DAI>
  </DOI>
</LN>
<LN lnClass="DAGC" lnType="DAGC1" inst="1" prefix="WSd" desc="Control Function - modulation of W in feed/absorbtion at PoC - from DSO">
  <DOI name="NamPlt">
    <DAI name="lnNs">
      <Val>(Tr)IEC 61850-CEI016:2022</Val>
    </DAI>
  </DOI>
  <DOI name="Beh" desc="">
    <DAI name="stVal">
      <Val>off</Val>
    </DAI>
  </DOI>
  <DOI name="WSptPct" desc="Setpoint of W in feed/absorbtion at PoC (percentage with sign with respect to Smax) [0..100]">
    <DAI name="ctlModel">
      <Val>sbo-with-enhanced-security</Val>
    </DAI>
    <SDI name="mxVal" desc="Setpoint of W in feed/absorbtion at PoC (percentage with sign with respect to Smax) [0..100]">
      <DAI name="f" desc="Valore default set-point">
        <Val>20</Val>
      </DAI>
    </SDI>
  </DOI>
  <DOI name="Mod" desc="Activation/deactivation [5 = Inactive, 1 = Active]">
    <DAI name="stVal">
      <Val>off</Val>
    </DAI>
    <DAI name="ctlModel">
      <Val>sbo-with-enhanced-security</Val>
    </DAI>
  </DOI>
</LN>
<LN lnClass="DVAR" lnType="DVAR1" inst="1" prefix="VArSd" desc="Control Function - voltage regulation with respect to Inductive/Capacitive reactive power - from DSO">
  <DOI name="NamPlt">
    <DAI name="lnNs">
      <Val>(Tr)IEC 61850-CEI016:2022</Val>
    </DAI>
  </DOI>
  <DOI name="Beh" desc="">
    <DAI name="stVal">
      <Val>on</Val>
    </DAI>
  </DOI>
  <DOI name="VArTgtSptPct" desc="Inductive/Capacitive VAr setpoint (percentage with sign with respect to Smax) [0..100]">
    <DAI name="ctlModel">
      <Val>sbo-with-enhanced-security</Val>
    </DAI>
  </DOI>
  <DOI name="Mod" desc="Activation/deactivation [5 = Inactive, 1 = Active]">
    <DAI name="stVal">
      <Val>on</Val>
    </DAI>
    <DAI name="ctlModel">
      <Val>sbo-with-enhanced-security</Val>
    </DAI>
  </DOI>
</LN>
<LN lnClass="DFPF" lnType="DFPF1" inst="1" prefix="PFSP" desc="Control Function - power factor setpoint - from DSO">
  <DOI name="NamPlt">
    <DAI name="lnNs">
      <Val>(Tr)IEC 61850-CEI016:2022</Val>
    </DAI>
  </DOI>
  <DOI name="Beh" desc="">
    <DAI name="stVal">
      <Val>off</Val>
    </DAI>
  </DOI>
  <DOI name="PFGnTgtSpt" desc="FdP setpoint in case of active power generation [-1.00..0.00]">
    <DAI name="ctlModel">
      <Val>sbo-with-enhanced-security</Val>
    </DAI>
  </DOI>
  <DOI name="PFLodTgtSpt" desc="FdP setpoint in case of active power absorbtion [0.00..1.00]">
    <DAI name="ctlModel">
      <Val>sbo-with-enhanced-security</Val>
    </DAI>
  </DOI>
  <DOI name="Mod" desc="Activation/deactivation [5 = Inactive, 1 = Active]">
    <DAI name="stVal">
      <Val>off</Val>
    </DAI>
    <DAI name="ctlModel">
      <Val>sbo-with-enhanced-security</Val>
    </DAI>
  </DOI>
</LN>
<LN lnClass="DVVR" lnType="DVVR1" inst="1" prefix="VArV" desc="Control Function - Q(V) - from DSO">
  <DOI name="NamPlt">
    <DAI name="lnNs">
      <Val>(Tr)IEC 61850-CEI016:2022</Val>
    </DAI>
  </DOI>
  <DOI name="Beh" desc="">
    <DAI name="stVal">
      <Val>off</Val>
    </DAI>
  </DOI>
  <DOI name="Mod" desc="Activation/deactivation [5 = Inactive, 1 = Active]">
    <DAI name="stVal">
      <Val>off</Val>
    </DAI>
    <DAI name="ctlModel">
      <Val>sbo-with-enhanced-security</Val>
    </DAI>
  </DOI>
  <DOI name="VArTgtSptPct" desc="XXXX []">
    <DAI name="ctlModel">
      <Val>sbo-with-enhanced-security</Val>
    </DAI>
  </DOI>
  <DOI name="K" desc="Parameter K of Q(V) function [-1.00..1.00]" />
</LN>
<LN lnClass="DPMC" lnType="DPMC1" inst="1" prefix="VArV" desc="Control Function - Q(V) - from DSO">
  <DOI name="NamPlt">
    <DAI name="lnNs">
      <Val>IEC 61850-7-420:2019A</Val>
    </DAI>
  </DOI>
  <DOI name="Beh" desc="">
    <DAI name="stVal">
      <Val>off</Val>
    </DAI>
  </DOI>
  <DOI name="WSpt1" desc="Lock-in power of Q(V) function - [0.00..max] of nominal P (p.u.)">
    <DAI name="ctlModel">
      <Val>sbo-with-enhanced-security</Val>
    </DAI>
  </DOI>
</LN>
<LN lnClass="DPMC" lnType="DPMC1" inst="2" prefix="VArV" desc="Control Function - Q(V) - from DSO">
  <DOI name="NamPlt">
    <DAI name="lnNs">
      <Val>IEC 61850-7-420:2019A</Val>
    </DAI>
  </DOI>
  <DOI name="Beh" desc="">
    <DAI name="stVal">
      <Val>off</Val>
    </DAI>
  </DOI>
  <DOI name="WSpt1" desc="Lock-out power of Q(V) function - [0.00..max] of nominal P (p.u.)">
    <DAI name="ctlModel">
      <Val>sbo-with-enhanced-security</Val>
    </DAI>
  </DOI>
</LN>
<LN lnClass="DECP" lnType="DECP2" inst="1" prefix="VArV" desc="Control Function - Q(V) - from DSO">
  <DOI name="NamPlt">
    <DAI name="lnNs">
      <Val>IEC 61850-7-420:2019A</Val>
    </DAI>
  </DOI>
  <DOI name="Beh" desc="">
    <DAI name="stVal">
      <Val>off</Val>
    </DAI>
  </DOI>
  <DOI name="VMax" desc="Upper voltage 1 of Q(V) function [0.00..max] of nominal V (p.u.)" />
  <DOI name="VMin" desc="Lower voltage 1 of Q(V) function [0.00..max] of nominal V (p.u.)" />
</LN>
<LN lnClass="DECP" lnType="DECP2" inst="2" prefix="VArV" desc="Control Function - Q(V) - from DSO">
  <DOI name="NamPlt">
    <DAI name="lnNs">
      <Val>IEC 61850-7-420:2019A</Val>
    </DAI>
  </DOI>
  <DOI name="Beh" desc="">
    <DAI name="stVal">
      <Val>off</Val>
    </DAI>
  </DOI>
  <DOI name="VMax" desc="Upper voltage 2 of Q(V) function [0.00..max] of nominal V (p.u.)" />
  <DOI name="VMin" desc="Lower voltage 2 of Q(V) function [0.00..max] of nominal V (p.u.)" />
</LN>
<LN lnClass="DPFW" lnType="DPFW1" inst="1" prefix="PFW" desc="Control Function - cosfi = f(P) - from DSO">
  <DOI name="NamPlt">
    <DAI name="lnNs">
      <Val>(Tr)IEC 61850-CEI016:2022</Val>
    </DAI>
  </DOI>
  <DOI name="Beh" desc="">
    <DAI name="stVal">
      <Val>off</Val>
    </DAI>
  </DOI>
  <DOI name="Mod" desc="Activation/deactivation [5 = Inactive, 1 = Active]">
    <DAI name="stVal">
      <Val>off</Val>
    </DAI>
    <DAI name="ctlModel">
      <Val>sbo-with-enhanced-security</Val>
    </DAI>
  </DOI>
  <DOI name="WSetA" desc="P value (point A) [0.00..max] of nominal P (p.u.)" />
  <DOI name="PFSetA" desc="cosfi value (point A) [-1.00..1.00]" />
  <DOI name="WSetB" desc="P value (point B) [0.00..max] of nominal P (p.u.)" />
  <DOI name="PFSetB" desc="cosfi value (point B) [-1.00..1.00]" />
  <DOI name="WSetC" desc="P value (point C) [0.00..max] of nominal P (p.u.)" />
  <DOI name="PFSetC" desc="cosfi value (point C) [-1.00..1.00]" />
  <DOI name="VLkIn" desc="Lock-in voltage of cosfi = f(P) [1.00..1.10] of nominal V (p.u.)" />
  <DOI name="VLkOut" desc="Lock-out voltage of cosfi = f(P) [0.90..1.00] of nominal V (p.u.)" />
</LN>
"""

dataTypeTemplates = \
"""
<DataTypeTemplates>
  <LNodeType id="LLN01" lnClass="LLN0">
    <DO name="NamPlt" type="LPL_4_NamPlt" />

    <DO name="Beh" type="ENS_2_Beh" />
    <DO name="Health" type="ENS_1_Health" />
    <DO name="Mod" type="ENC_1_Mod" />
  </LNodeType>
  <LNodeType id="LPHD1" lnClass="LPHD">
    <DO name="PhyNam" type="DPL_1_PhyNam" />
    <DO name="PhyHealth" type="ENS_1_PhyHealth" />
    <DO name="Proxy" type="SPS_1_Proxy" />
  </LNodeType>
  <LNodeType id="DPCC1" lnClass="DPCC">
    <DO name="NamPlt" type="LPL_5_NamPlt" />
    <DO name="Beh" type="ENS_2_Beh" />
    <DO name="AreaEpsEcpId" type="VSG_2_AreaEpsEcp" />
    <DO name="AreaEpsWMax" type="ASG_2_WMaxSet" />
    <DO name="VRef" type="ASG_2_WMaxSet" />
    <DO name="WRtg" type="ASG_2_WMaxSet" />
    <DO name="RefFrm" type="SPG_2_RefFrm" />
    <DO name="ElcRefId" type="VSG_2_AreaEpsEcp" />
  </LNodeType>
  <LNodeType id="DPCC2" lnClass="DPCC">
    <DO name="NamPlt" type="LPL_5_NamPlt" />
    <DO name="Beh" type="ENS_2_Beh" />
    <DO name="AreaEpsEcpId" type="VSG_2_AreaEpsEcp" />
    <DO name="AreaEpsWMax" type="ASG_2_WMaxSet" />
    <DO name="VRef" type="ASG_2_WMaxSet" />
    <DO name="VArRtg" type="ASG_2_WMaxSet" />
    <DO name="RefFrm" type="SPG_2_RefFrm" />
    <DO name="ElcRefId" type="VSG_2_AreaEpsEcp" />
  </LNodeType>
  <LNodeType id="DPCC3" lnClass="DPCC">
    <DO name="NamPlt" type="LPL_5_NamPlt" />
    <DO name="Beh" type="ENS_2_Beh" />
    <DO name="AreaEpsEcpId" type="VSG_2_AreaEpsEcp" />
    <DO name="AreaEpsWMax" type="ASG_2_WMaxSet" />
    <DO name="VRef" type="ASG_2_WMaxSet" />
    <DO name="VARtg" type="ASG_2_WMaxSet" />
    <DO name="RefFrm" type="SPG_2_RefFrm" />
    <DO name="ElcRefId" type="VSG_2_AreaEpsEcp" />
  </LNodeType>
  <LNodeType id="DECP1" lnClass="DECP">
    <DO name="NamPlt" type="LPL_5_NamPlt" />
    <DO name="Beh" type="ENS_2_Beh" />
    <DO name="VRef" type="ASG_2_WMaxSet" />
    <DO name="RefFrm" type="SPG_2_RefFrm" />
    <DO name="ElcRefId" type="VSG_2_AreaEpsEcp" />
  </LNodeType>
  <LNodeType id="DGEN1" lnClass="DGEN">
    <DO name="NamPlt" type="LPL_5_NamPlt" />
    <DO name="DEROpSt" type="ENS_2_DEROpSt" />
    <DO name="Beh" type="ENS_2_Beh" />
    <DO name="WMaxRtg" type="ASG_2_WMaxSet" />
    <DO name="VMaxRtg" type="ASG_2_WMaxSet" />
    <DO name="WMax" type="ASG_2_WMaxSet" />
    <DO name="WRmp" type="ASG_2_WMaxSet" />
    <DO name="VMax" type="ASG_2_WMaxSet" />
    <DO name="OutEcpRef" type="ORG_2_ElcMsRef" />
    <DO name="PhsConnTyp" type="ENG_2_PhsConnTyp" />
    <DO name="DERTyp" type="ENG_2_DERTyp" />
  </LNodeType>
  <LNodeType id="DSTO1" lnClass="DSTO">
    <DO name="NamPlt" type="LPL_5_NamPlt" />
    <DO name="DEROpSt" type="ENS_2_DEROpSt" />
    <DO name="Beh" type="ENS_2_Beh" />
    <DO name="EffWh" type="MV_2_CtbWPct" />
    <DO name="EffWhPct" type="MV_2_CtbWPct" />
    <DO name="EqSto" type="ORG_2_ElcMsRef" />
    <DO name="ChaWMax" type="ASG_2_WMaxSet" />
    <DO name="OutEcpRef" type="ORG_2_ElcMsRef" />
    <DO name="PhsConnTyp" type="ENG_2_PhsConnTyp" />
    <DO name="DERTyp" type="ENG_2_DERTyp" />
  </LNodeType>
  <LNodeType id="MMXU1" lnClass="MMXU">
    <DO name="Beh" type="ENS_2_Beh" />
    <DO name="TotW" type="MV_2_CtbWPct" />
    <DO name="TotVAr" type="MV_2_CtbWPct" />
    <DO name="PPV" type="DEL_1_PPV" />
    <DO name="A" type="WYE_1_A" />
  </LNodeType>
  <LNodeType id="MMXU2" lnClass="MMXU">
    <DO name="Beh" type="ENS_2_Beh" />
    <DO name="TotW" type="MV_2_CtbWPct" />
  </LNodeType>
  <LNodeType id="XCBR1" lnClass="XCBR">
    <DO name="Loc" type="SPS_1_Proxy" />
    <DO name="OpCnt" type="INS_1_OpCnt" />
    <DO name="Beh" type="ENS_2_Beh" />
    <DO name="Pos" type="DPC_1_Pos" />
    <DO name="BlkOpn" type="SPC_1_BlkOpn" />
    <DO name="BlkCls" type="SPC_1_BlkOpn" />
  </LNodeType>
  <LNodeType id="DGEN2" lnClass="DGEN">
    <DO name="NamPlt" type="LPL_5_NamPlt" />
    <DO name="DEROpSt" type="ENS_2_DEROpSt" />
    <DO name="Beh" type="ENS_2_Beh" />
    <DO name="Health" type="ENS_1_Health" />
    <DO name="WMaxRtg" type="ASG_2_WMaxSet" />
    <DO name="VMaxRtg" type="ASG_2_WMaxSet" />
    <DO name="WMax" type="ASG_2_WMaxSet" />
    <DO name="WRmp" type="ASG_2_WMaxSet" />
    <DO name="VMax" type="ASG_2_WMaxSet" />
    <DO name="OutEcpRef" type="ORG_2_ElcMsRef" />
    <DO name="PhsConnTyp" type="ENG_2_PhsConnTyp" />
    <DO name="DERTyp" type="ENG_2_DERTyp" />
    <DO name="GnGrId" type="INS_1_OpCnt" />
  </LNodeType>
  <LNodeType id="DWMX1" lnClass="DWMX">
    <DO name="NamPlt" type="LPL_5_NamPlt" />
    <DO name="Beh" type="ENS_2_Beh" />
    <DO name="WMaxSptPct" type="APC_1_WMaxSpt" />
    <DO name="Mod" type="ENC_2_Mod" />
    <DO name="RmpRteUse" type="SPG_2_RefFrm" />
    <DO name="InEcpRef" type="ORG_2_ElcMsRef" />
    <DO name="FctOpStAuto" type="ENS_2_FctOpSt" />
    <DO name="FctOpStEx" type="ENS_2_FctOpSt" />
  </LNodeType>
  <LNodeType id="DAGC1" lnClass="DAGC">
    <DO name="NamPlt" type="LPL_5_NamPlt" />
    <DO name="Beh" type="ENS_2_Beh" />
    <DO name="ReqW" type="MV_2_CtbWPct" />
    <DO name="WSptPct" type="APC_1_WMaxSpt" />
    <DO name="Mod" type="ENC_2_Mod" />
    <DO name="RmpRteUse" type="SPG_2_RefFrm" />
    <DO name="InEcpRef" type="ORG_2_ElcMsRef" />
    <DO name="FctOpSt" type="ENS_2_FctOpSt" />
  </LNodeType>
  <LNodeType id="DVAR1" lnClass="DVAR">
    <DO name="NamPlt" type="LPL_5_NamPlt" />
    <DO name="Beh" type="ENS_2_Beh" />
    <DO name="ReqVAr" type="MV_2_CtbWPct" />
    <DO name="VArTgtSptPct" type="APC_1_WMaxSpt" />
    <DO name="Mod" type="ENC_2_Mod" />
    <DO name="RmpRteUse" type="SPG_2_RefFrm" />
    <DO name="InEcpRef" type="ORG_2_ElcMsRef" />
    <DO name="FctOpSt" type="ENS_2_FctOpSt" />
  </LNodeType>
  <LNodeType id="DFPF1" lnClass="DFPF">
    <DO name="NamPlt" type="LPL_5_NamPlt" />
    <DO name="ReqPFExt" type="SPS_1_Proxy" />
    <DO name="Beh" type="ENS_2_Beh" />
    <DO name="ReqPF" type="MV_2_CtbWPct" />
    <DO name="PFGnTgtSpt" type="APC_1_WMaxSpt" />
    <DO name="PFLodTgtSpt" type="APC_1_WMaxSpt" />
    <DO name="Mod" type="ENC_2_Mod" />
    <DO name="RmpRteUse" type="SPG_2_RefFrm" />
    <DO name="InEcpRef" type="ORG_2_ElcMsRef" />
    <DO name="FctOpSt" type="ENS_2_FctOpSt" />
  </LNodeType>
  <LNodeType id="DVVR1" lnClass="DVVR">
    <DO name="NamPlt" type="LPL_5_NamPlt" />
    <DO name="Beh" type="ENS_2_Beh" />
    <DO name="VRefEsp" type="MV_2_CtbWPct" />
    <DO name="ReqVAr" type="MV_2_CtbWPct" />
    <DO name="VArTgtSptPct" type="APC_1_WMaxSpt" />
    <DO name="Mod" type="ENC_2_Mod" />
    <DO name="VVArCrvDel" type="CSG_1_VVArCrv" />
    <DO name="RmpRteUse" type="SPG_2_RefFrm" />
    <DO name="InEcpRef" type="ORG_2_ElcMsRef" />
    <DO name="FctOpSt" type="ENS_2_FctOpSt" />
    <DO name="K" type="ASG_2_WMaxSet" />
  </LNodeType>
  <LNodeType id="DPMC1" lnClass="DPMC">
    <DO name="NamPlt" type="LPL_5_NamPlt" />
    <DO name="Beh" type="ENS_2_Beh" />
    <DO name="WSpt1" type="APC_1_WMaxSpt" />
    <DO name="DERRef" type="ORG_2_ElcMsRef" />
    <DO name="OutEcpRef" type="ORG_2_ElcMsRef" />
  </LNodeType>
  <LNodeType id="DECP2" lnClass="DECP">
    <DO name="NamPlt" type="LPL_5_NamPlt" />
    <DO name="Beh" type="ENS_2_Beh" />
    <DO name="VRef" type="ASG_2_WMaxSet" />
    <DO name="VMax" type="ASG_2_WMaxSet" />
    <DO name="VMin" type="ASG_2_WMaxSet" />
    <DO name="RefFrm" type="SPG_2_RefFrm" />
    <DO name="ElcRefId" type="VSG_2_AreaEpsEcp" />
  </LNodeType>
  <LNodeType id="DPFW1" lnClass="DPFW">
    <DO name="NamPlt" type="LPL_5_NamPlt" />
    <DO name="Beh" type="ENS_2_Beh" />
    <DO name="FctOpSt" type="ENS_2_FctOpSt" />
    <DO name="Mod" type="ENC_2_Mod" />
    <DO name="WSetA" type="ASG_2_WMaxSet" />
    <DO name="PFSetA" type="ASG_2_WMaxSet" />
    <DO name="WSetB" type="ASG_2_WMaxSet" />
    <DO name="PFSetB" type="ASG_2_WMaxSet" />
    <DO name="WSetC" type="ASG_2_WMaxSet" />
    <DO name="PFSetC" type="ASG_2_WMaxSet" />
    <DO name="VLkIn" type="ASG_2_WMaxSet" />
    <DO name="VLkOut" type="ASG_2_WMaxSet" />
    <DO name="RmpRteUse" type="SPG_2_RefFrm" />
    <DO name="InEcpRef" type="ORG_2_ElcMsRef" />
  </LNodeType>
  <DOType id="ENC_1_Mod" cdc="ENC">
    <DA name="stVal" type="Mod" bType="Enum" fc="ST" dchg="true" />
    <DA name="q" bType="Quality" fc="ST" qchg="true" />
    <DA name="t" bType="Timestamp" fc="ST" />
    <DA name="ctlModel" type="CtlModelKind_SO" bType="Enum" fc="CF" dchg="true" />
  </DOType>
  <DOType id="ENS_2_Beh" cdc="ENS">
    <DA name="stVal" type="Beh" bType="Enum" fc="ST" dchg="true" />
    <DA name="q" bType="Quality" fc="ST" qchg="true" />
    <DA name="t" bType="Timestamp" fc="ST" />
  </DOType>
  <DOType id="ENS_1_Health" cdc="ENS">
    <DA name="stVal" type="Health" bType="Enum" fc="ST" dchg="true" />
    <DA name="q" bType="Quality" fc="ST" qchg="true" />
    <DA name="t" bType="Timestamp" fc="ST" />
  </DOType>
  <DOType id="DPL_1_PhyNam" cdc="DPL">
    <DA name="vendor" bType="VisString255" fc="DC" />
    <DA name="swRev" bType="VisString255" fc="DC" />
    <DA name="location" bType="VisString255" fc="DC" />
  </DOType>
  <DOType id="ENS_1_PhyHealth" cdc="ENS">
    <DA name="stVal" type="PhyHealth" bType="Enum" fc="ST" dchg="true" />
    <DA name="q" bType="Quality" fc="ST" qchg="true" />
    <DA name="t" bType="Timestamp" fc="ST" />
  </DOType>
  <DOType id="SPS_1_Proxy" cdc="SPS">
    <DA name="stVal" bType="BOOLEAN" fc="ST" dchg="true" />
    <DA name="q" bType="Quality" fc="ST" qchg="true" />
    <DA name="t" bType="Timestamp" fc="ST" />
  </DOType>
  <DOType id="LPL_4_NamPlt" cdc="LPL">
    <DA name="vendor" bType="VisString255" fc="DC" />
    <DA name="swRev" bType="VisString255" fc="DC" />
    <DA name="ldNs" bType="VisString255" fc="EX"/>
    <DA name="configRev" bType="VisString255" fc="DC" />
  </DOType>
  <DOType id="LPL_5_NamPlt" cdc="LPL">
    <DA name="vendor" bType="VisString255" fc="DC" />
    <DA name="swRev" bType="VisString255" fc="DC" />
    <DA name="lnNs" bType="VisString255" fc="EX"/>
  </DOType>
  <DOType id="VSG_2_AreaEpsEcp" cdc="VSG">
    <DA name="setVal" bType="VisString255" fc="SP" dchg="true" />
  </DOType>
  <DOType id="ASG_2_WMaxSet" cdc="ASG">
    <DA name="setMag" type="AnalogueValue_1" bType="Struct" fc="SP" dchg="true" />
  </DOType>
  <DOType id="ENG_2_PhsConnTyp" cdc="ENG">
    <DA name="setVal" type="PhaseKind" bType="Enum" fc="SP" dchg="true" />
  </DOType>
  <DOType id="ENG_2_DERTyp" cdc="ENG">
    <DA name="setVal" type="DERUnitKind" bType="Enum" fc="SP" dchg="true" />
  </DOType>
  <DOType id="ORG_2_ElcMsRef" cdc="ORG">
    <DA name="setSrcRef" bType="VisString129" fc="SP" dchg="true" />
  </DOType>
  <DOType id="SPG_2_RefFrm" cdc="SPG">
    <DA name="setVal" bType="BOOLEAN" fc="SP" dchg="true" />
  </DOType>
  <DOType id="MV_2_CtbWPct" cdc="MV">
    <DA name="mag" type="AnalogueValue_1" bType="Struct" fc="MX" dchg="true" />
    <DA name="q" bType="Quality" fc="MX" qchg="true" />
    <DA name="t" bType="Timestamp" fc="MX" />
  </DOType>
  <DOType id="ENS_2_DEROpSt" cdc="ENS">
    <DA name="stVal" type="DERStateKind" bType="Enum" fc="ST" dchg="true" />
    <DA name="q" bType="Quality" fc="ST" qchg="true" />
    <DA name="t" bType="Timestamp" fc="ST" />
  </DOType>
  <DOType id="DEL_1_PPV" cdc="DEL">
    <SDO name="phsAB" type="CMV_1_phsAB" />
    <SDO name="phsBC" type="CMV_1_phsAB" />
    <SDO name="phsCA" type="CMV_1_phsAB" />
  </DOType>
  <DOType id="CMV_1_phsAB" cdc="CMV">
    <DA name="cVal" type="Vector_1" bType="Struct" fc="MX" dchg="true" />
    <DA name="q" bType="Quality" fc="MX" qchg="true" />
    <DA name="t" bType="Timestamp" fc="MX" />
  </DOType>
  <DOType id="WYE_1_A" cdc="WYE">
    <SDO name="phsA" type="CMV_1_phsAB" />
    <SDO name="phsB" type="CMV_1_phsAB" />
    <SDO name="phsC" type="CMV_1_phsAB" />
  </DOType>
  <DOType id="INS_1_OpCnt" cdc="INS">
    <DA name="stVal" bType="INT32" fc="ST" dchg="true" />
    <DA name="q" bType="Quality" fc="ST" qchg="true" />
    <DA name="t" bType="Timestamp" fc="ST" />
  </DOType>
  <DOType id="DPC_1_Pos" cdc="DPC">
    <DA name="stVal" bType="Dbpos" fc="ST" dchg="true" />
    <DA name="q" bType="Quality" fc="ST" qchg="true" />
    <DA name="t" bType="Timestamp" fc="ST" />
    <DA name="ctlModel" type="CtlModelKind_SO" bType="Enum" fc="CF" dchg="true" />
  </DOType>
  <DOType id="SPC_1_BlkOpn" cdc="SPC">
    <DA name="stVal" bType="BOOLEAN" fc="ST" dchg="true" />
    <DA name="q" bType="Quality" fc="ST" qchg="true" />
    <DA name="t" bType="Timestamp" fc="ST" />
    <DA name="ctlModel" type="CtlModelKind_SO" bType="Enum" fc="CF" dchg="true" />
  </DOType>
  <DOType id="APC_1_WMaxSpt" cdc="APC">
    <DA name="mxVal" type="AnalogueValue_1" bType="Struct" fc="MX" dchg="true" />
    <DA name="q" bType="Quality" fc="MX" qchg="true" />
    <DA name="t" bType="Timestamp" fc="MX" />
    <DA name="ctlModel" type="CtlModelKind_SBOw" bType="Enum" fc="CF" />
    <DA name="SBOw" type="APCSelectWithValue_1" bType="Struct" fc="CO" />
    <DA name="Oper" type="APCOperate_1" bType="Struct" fc="CO" />
    <DA name="Cancel" type="APCCancel_1" bType="Struct" fc="CO" />
  </DOType>
  <DOType id="ENC_2_Mod" cdc="ENC">
    <DA name="stVal" type="Mod" bType="Enum" fc="ST" dchg="true" />
    <DA name="q" bType="Quality" fc="ST" qchg="true" />
    <DA name="t" bType="Timestamp" fc="ST" />
    <DA name="ctlModel" type="CtlModelKind_SBOw" bType="Enum" fc="CF" />
    <DA name="SBOw" type="ENCSelectWithValue_1" bType="Struct" fc="CO" />
    <DA name="Oper" type="ENCOperate_1" bType="Struct" fc="CO" />
    <DA name="Cancel" type="ENCCancel_1" bType="Struct" fc="CO" />
  </DOType>
  <DOType id="ENS_2_FctOpSt" cdc="ENS">
    <DA name="stVal" type="DERFunctionState" bType="Enum" fc="ST" dchg="true" />
    <DA name="q" bType="Quality" fc="ST" qchg="true" />
    <DA name="t" bType="Timestamp" fc="ST" />
  </DOType>
  <DOType id="CSG_1_VVArCrv" cdc="CSG">
    <DA name="numPts" bType="INT16U" fc="SP" />
    <DA name="crvPts" type="Point_2" bType="Struct" count="16" fc="SP" />
    <DA name="xUnits" type="Unit_3" bType="Struct" fc="CF" />
    <DA name="yUnits" type="Unit_3" bType="Struct" fc="CF" />
    <DA name="maxPts" bType="INT16U" fc="CF" />
    <DA name="xD" bType="VisString255" fc="DC" />
    <DA name="yD" bType="VisString255" fc="DC" />
  </DOType>
  <DAType id="Vector_1">
    <BDA name="mag" type="AnalogueValue_1" bType="Struct" />
    <BDA name="ang" type="AnalogueValue_1" bType="Struct" />
  </DAType>
  <DAType id="Point_2">
    <BDA name="xVal" bType="FLOAT32" />
    <BDA name="yVal" bType="FLOAT32" />
  </DAType>
  <DAType id="Unit_3">
    <BDA name="SIUnit" type="SIUnitKind" bType="Enum" />
  </DAType>
  <DAType id="APCCancel_1">
    <BDA name="ctlVal" type="AnalogueValue_1" bType="Struct" />
    <BDA name="origin" type="Originator_1" bType="Struct" />
    <BDA name="ctlNum" bType="INT8U" />
    <BDA name="T" bType="Timestamp" />
    <BDA name="Test" bType="BOOLEAN" />
  </DAType>
  <DAType id="APCOperate_1">
    <BDA name="ctlVal" type="AnalogueValue_1" bType="Struct" />
    <BDA name="origin" type="Originator_1" bType="Struct" />
    <BDA name="ctlNum" bType="INT8U" />
    <BDA name="T" bType="Timestamp" />
    <BDA name="Test" bType="BOOLEAN" />
    <BDA name="Check" bType="Check" />
  </DAType>
  <DAType id="APCSelectWithValue_1">
    <BDA name="ctlVal" type="AnalogueValue_1" bType="Struct" />
    <BDA name="origin" type="Originator_1" bType="Struct" />
    <BDA name="ctlNum" bType="INT8U" />
    <BDA name="T" bType="Timestamp" />
    <BDA name="Test" bType="BOOLEAN" />
    <BDA name="Check" bType="Check" />
  </DAType>
  <DAType id="ENCSelectWithValue_1">
    <BDA name="ctlVal" type="Mod" bType="Enum" />
    <BDA name="origin" type="Originator_1" bType="Struct" />
    <BDA name="ctlNum" bType="INT8U" />
    <BDA name="T" bType="Timestamp" />
    <BDA name="Test" bType="BOOLEAN" />
    <BDA name="Check" bType="Check" />
  </DAType>
  <DAType id="ENCOperate_1">
    <BDA name="ctlVal" type="Mod" bType="Enum" />
    <BDA name="origin" type="Originator_1" bType="Struct" />
    <BDA name="ctlNum" bType="INT8U" />
    <BDA name="T" bType="Timestamp" />
    <BDA name="Test" bType="BOOLEAN" />
    <BDA name="Check" bType="Check" />
  </DAType>
  <DAType id="ENCCancel_1">
    <BDA name="ctlVal" type="Mod" bType="Enum" />
    <BDA name="origin" type="Originator_1" bType="Struct" />
    <BDA name="ctlNum" bType="INT8U" />
    <BDA name="T" bType="Timestamp" />
    <BDA name="Test" bType="BOOLEAN" />
  </DAType>
  <DAType id="Originator_1">
    <BDA name="orCat" type="OriginatorCategoryKind" bType="Enum" />
    <BDA name="orIdent" bType="Octet64" />
  </DAType>
  <DAType id="AnalogueValue_1">
    <BDA name="f" bType="FLOAT32" desc="The value of f shall be the FLOAT representation of the measured value. f shall represent the technological value in SI units." />
  </DAType>
  <EnumType id="Mod">
    <EnumVal ord="1">on</EnumVal>
    <EnumVal ord="2">on-blocked</EnumVal>
    <EnumVal ord="3">test</EnumVal>
    <EnumVal ord="4">test/blocked</EnumVal>
    <EnumVal ord="5">off</EnumVal>
  </EnumType>
  <EnumType id="CtlModelKind_SO">
    <EnumVal ord="0">status-only</EnumVal>
  </EnumType>
  <EnumType id="CtlModelKind_SBOw">
    <EnumVal ord="0">status-only</EnumVal>
    <EnumVal ord="1">direct-with-normal-security</EnumVal>
    <EnumVal ord="2">sbo-with-normal-security</EnumVal>
    <EnumVal ord="3">direct-with-enhanced-security</EnumVal>
    <EnumVal ord="4">sbo-with-enhanced-security</EnumVal>
  </EnumType>
  <EnumType id="Beh">
    <EnumVal ord="1">on</EnumVal>
    <EnumVal ord="2">on-blocked</EnumVal>
    <EnumVal ord="3">test</EnumVal>
    <EnumVal ord="4">test/blocked</EnumVal>
    <EnumVal ord="5">off</EnumVal>
  </EnumType>
  <EnumType id="Health">
    <EnumVal ord="1">Ok</EnumVal>
    <EnumVal ord="2">Warning</EnumVal>
    <EnumVal ord="3">Alarm</EnumVal>
  </EnumType>
  <EnumType id="PhyHealth">
    <EnumVal ord="1">Ok</EnumVal>
    <EnumVal ord="2">Warning</EnumVal>
    <EnumVal ord="3">Alarm</EnumVal>
  </EnumType>
  <EnumType id="DERStateKind">
    <EnumVal ord="1">on but disconnected and not ready</EnumVal>
    <EnumVal ord="2">starting up</EnumVal>
    <EnumVal ord="3">disconnected and available</EnumVal>
    <EnumVal ord="4">disconnected and authorized</EnumVal>
    <EnumVal ord="5">synchronizing</EnumVal>
    <EnumVal ord="6">running</EnumVal>
    <EnumVal ord="7">stopping and disconnecting under emergency conditions</EnumVal>
    <EnumVal ord="8">stopping</EnumVal>
    <EnumVal ord="9">disconnected and blocked</EnumVal>
    <EnumVal ord="10">disconnected and in maintenance</EnumVal>
    <EnumVal ord="11">failed</EnumVal>
    <EnumVal ord="98">Not applicable or not known</EnumVal>
  </EnumType>
  <EnumType id="PhaseKind">
    <EnumVal ord="1">Single phase to neutral</EnumVal>
    <EnumVal ord="2">Split phase</EnumVal>
    <EnumVal ord="3">2-phase</EnumVal>
    <EnumVal ord="4">3-phase delta</EnumVal>
    <EnumVal ord="5">3-phase wye / 4-wires</EnumVal>
    <EnumVal ord="6">3-phase wye / 5-wires</EnumVal>
    <EnumVal ord="9">DC</EnumVal>
    <EnumVal ord="98">Not applicable or not known</EnumVal>
  </EnumType>
  <EnumType id="DERUnitKind">
    <EnumVal ord="1">Diesel / gas engine</EnumVal>
    <EnumVal ord="2">Gas Turbine engine</EnumVal>
    <EnumVal ord="3">PV</EnumVal>
    <EnumVal ord="4">PV plus Storage</EnumVal>
    <EnumVal ord="5">Lithium Ion Battery Storage</EnumVal>
    <EnumVal ord="6">Fuel cell</EnumVal>
    <EnumVal ord="7">Hydro generator</EnumVal>
    <EnumVal ord="8">Wind turbine</EnumVal>
    <EnumVal ord="9">Flow battery storage</EnumVal>
    <EnumVal ord="10">Air compression storage</EnumVal>
    <EnumVal ord="11">Flywheel storage</EnumVal>
    <EnumVal ord="12">Capacitor storage</EnumVal>
    <EnumVal ord="13">Vehicle-to-Grid (V2G)</EnumVal>
    <EnumVal ord="50">Mixed, hybrid DER</EnumVal>
    <EnumVal ord="98">Not applicable or not known</EnumVal>
  </EnumType>
  <EnumType id="OriginatorCategoryKind">
    <EnumVal ord="0">not-supported</EnumVal>
    <EnumVal ord="1">bay-control</EnumVal>
    <EnumVal ord="2">station-control</EnumVal>
    <EnumVal ord="3">remote-control</EnumVal>
    <EnumVal ord="4">automatic-bay</EnumVal>
    <EnumVal ord="5">automatic-station</EnumVal>
    <EnumVal ord="6">automatic-remote</EnumVal>
    <EnumVal ord="7">maintenance</EnumVal>
    <EnumVal ord="8">process</EnumVal>
  </EnumType>
  <EnumType id="DERFunctionState">
    <EnumVal ord="0">Not Available</EnumVal>
    <EnumVal ord="1">Autonomous</EnumVal>
    <EnumVal ord="2">Slave</EnumVal>
  </EnumType>
  <EnumType id="SIUnitKind">
    <EnumVal ord="1" />
    <EnumVal ord="10">rad</EnumVal>
    <EnumVal ord="11">sr</EnumVal>
    <EnumVal ord="2">m</EnumVal>
    <EnumVal ord="21">Gy</EnumVal>
    <EnumVal ord="22">Bq</EnumVal>
    <EnumVal ord="23">°C</EnumVal>
    <EnumVal ord="24">Sv</EnumVal>
    <EnumVal ord="25">F</EnumVal>
    <EnumVal ord="26">C</EnumVal>
    <EnumVal ord="27">S</EnumVal>
    <EnumVal ord="28">H</EnumVal>
    <EnumVal ord="29">V</EnumVal>
    <EnumVal ord="3">kg</EnumVal>
    <EnumVal ord="30">ohm</EnumVal>
    <EnumVal ord="31">J</EnumVal>
    <EnumVal ord="32">N</EnumVal>
    <EnumVal ord="33">Hz</EnumVal>
    <EnumVal ord="34">Ix</EnumVal>
    <EnumVal ord="35">Lm</EnumVal>
    <EnumVal ord="36">Wb</EnumVal>
    <EnumVal ord="37">T</EnumVal>
    <EnumVal ord="38">W</EnumVal>
    <EnumVal ord="39">Pa</EnumVal>
    <EnumVal ord="4">s</EnumVal>
    <EnumVal ord="41">m²</EnumVal>
    <EnumVal ord="42">m³</EnumVal>
    <EnumVal ord="43">m/s</EnumVal>
    <EnumVal ord="44">m/s²</EnumVal>
    <EnumVal ord="45">m³/s</EnumVal>
    <EnumVal ord="46">m/m³</EnumVal>
    <EnumVal ord="47">M</EnumVal>
    <EnumVal ord="48">kg/m³</EnumVal>
    <EnumVal ord="49">m²/s</EnumVal>
    <EnumVal ord="5">A</EnumVal>
    <EnumVal ord="50">W/m K</EnumVal>
    <EnumVal ord="51">J/K</EnumVal>
    <EnumVal ord="52">ppm</EnumVal>
    <EnumVal ord="53">1/s</EnumVal>
    <EnumVal ord="54">rad/s</EnumVal>
    <EnumVal ord="55">W/m²</EnumVal>
    <EnumVal ord="56">J/m²</EnumVal>
    <EnumVal ord="57">S/m</EnumVal>
    <EnumVal ord="58">K/s</EnumVal>
    <EnumVal ord="59">Pa/s</EnumVal>
    <EnumVal ord="60">J/kg K</EnumVal>
    <EnumVal ord="6">K</EnumVal>
    <EnumVal ord="61">VA</EnumVal>
    <EnumVal ord="62">Watts</EnumVal>
    <EnumVal ord="63">VAr</EnumVal>
    <EnumVal ord="64">phi</EnumVal>
    <EnumVal ord="65">cos(phi)</EnumVal>
    <EnumVal ord="66">Vs</EnumVal>
    <EnumVal ord="67">V²</EnumVal>
    <EnumVal ord="68">As</EnumVal>
    <EnumVal ord="69">A²</EnumVal>
    <EnumVal ord="7">mol</EnumVal>
    <EnumVal ord="70">A²t</EnumVal>
    <EnumVal ord="71">VAh</EnumVal>
    <EnumVal ord="72">Wh</EnumVal>
    <EnumVal ord="73">VArh</EnumVal>
    <EnumVal ord="74">V/Hz</EnumVal>
    <EnumVal ord="75">Hz/s</EnumVal>
    <EnumVal ord="76">char</EnumVal>
    <EnumVal ord="77">char/s</EnumVal>
    <EnumVal ord="78">kgm²</EnumVal>
    <EnumVal ord="79">dB</EnumVal>
    <EnumVal ord="80">J/Wh</EnumVal>
    <EnumVal ord="81">W/s</EnumVal>
    <EnumVal ord="82">l/s</EnumVal>
    <EnumVal ord="83">dBm</EnumVal>
    <EnumVal ord="8">cd</EnumVal>
    <EnumVal ord="9">deg</EnumVal>
  </EnumType>
</DataTypeTemplates>"""