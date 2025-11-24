import xml.etree.ElementTree as ET
from datetime import datetime
import pandapower as pp
from icdbuilder.model.icd_static import *


# Class containing an IED Capability Description (ICD) file representation according to the 
# Substation Configuration Language (SCL)
class ICD: 
    def __init__(self, root: ET.Element):
        self.tree = ET.ElementTree(root)
    
    def toFile(self, filename):
        # Write to file prettified
        ET.indent(self.tree, space="  ")
        self.tree.write(filename, encoding="utf-8", xml_declaration=True)

class ICDBuilder:
    @staticmethod
    def build(contentDescription: str = "ICD File") -> ICD:
        root = ET.Element("SCL", attrib = {
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xmlns:sxi": "http://www.iec.ch/61850/2003/SCLcoordinates",
            "xmlns": "http://www.iec.ch/61850/2003/SCL",
            "xsi:schemaLocation": "http://www.iec.ch/61850/2003/SCL SCL.xsd",
            "version": "2007",
            "revision": "B",
            "release": "4"
        })
        header = ET.SubElement(root, "Header")
        history = ET.SubElement(header, "History")
        hitem = ET.SubElement(history, "Hitem", attrib={
            "version": "1",
            "revision": "0",
            "when": datetime.now().isoformat(),
            "who": "ICD-File-Builder",
            "what": contentDescription
        })
        ICDBuilder._buildCommunication(root)
        ICDBuilder._buildIED(root)
        ICDBuilder._buildDataTypeTemplates(root)
        return ICD(root)

    @staticmethod
    def _buildCommunication(parent: ET.Element):
        communication = ET.SubElement(parent, "Communication")
        subnet_xml = subnetwork.format(
            subnetwork="subNetwork1",
            bitrate="100000",
            apName="accessPoint1",
            ip="192.168.1.101",
            subnet="255.255.255.0",
            gateway="192.188.1.1")
        communication.append(ET.fromstring(subnet_xml))

    def _buildIED(parent: ET.Element):
        ied = ET.SubElement(parent, "IED", attrib={
            "name": "CCI016_01",
            "engRight": "full",
            "originalSclRevision": "B",
            "originalSclVersion": "2007",
            "originalSclRelease": "4"
        })
        ied.append(ET.fromstring(services))
        accessPoint = ET.SubElement(ied, "AccessPoint", attrib={"name": "accessPoint1", "desc": ""})
        server = ET.SubElement(accessPoint, "Server", attrib={"desc": "CCI CEI 0-16 Obs. and Contr."})
        _ = ET.SubElement(server, "Authentication")
        plantLD = ET.SubElement(server, "LDevice", attrib={"inst": "LD_Plant", "desc": ""})
        ln0 = ET.SubElement(plantLD, "LN0", attrib={"lnClass": "LLN0", "lnType": "LLN01", "inst": ""})
        ICDBuilder._completeLN0(ln0)

        plantLD.append(ET.fromstring(phyDevInfos))
        # TODO: Modify these values depending on the plant characteristics derived 
        # by the elements connected to it
        ICDBuilder._appendMultipleElements(plantLD, plantChar.format(
            maxGenP = 200,
            maxAbsP = 200,
            maxIndQ = 50,
            maxCapQ = 50,
            maxS = 210
        ))
        ICDBuilder._appendMultipleElements(plantLD, ctrlFunAvail)
        ICDBuilder._appendMultipleElements(plantLD, measAvailPerGroup)
        # TODO: For each single generation unit add a singleGenMeasTemplate LN accordingly
        plantLD.append(ET.fromstring(mainCbrStatus))
        # TODO: For each single generation unit add a singleGenStatusTemplate LN accordingly
        ICDBuilder._appendMultipleElements(plantLD, controlFunConfigTemplate)
    
    @staticmethod
    def _buildDataTypeTemplates(parent: ET.Element):
        dtt_xml = dataTypeTemplates.format()
        parent.append(ET.fromstring(dtt_xml))

    @staticmethod
    def _completeLN0(ln0: ET.Element):
        for key in datasets.keys():
            ln0.append(ET.fromstring(datasets[key]))
        # TODO: Add dataset whose elements depends on the number of single generators present
        # Building the ReportControl section
        for key in reportControlBlocks:
            ln0.append(ET.fromstring(reportControlBlocks[key]))
        ICDBuilder._appendMultipleElements(ln0, ln0OtherDois)

    @staticmethod
    def _appendMultipleElements(parent: ET.Element, toParse: str):
        # Parse and append other DOIs
        # Wrap in a dummy root because it contains multiple top-level elements
        elems_root = ET.fromstring(f"<root>{toParse}</root>")
        for elem in elems_root:
            parent.append(elem)