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