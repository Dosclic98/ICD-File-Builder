import xml.etree.ElementTree as ET
from datetime import datetime

# Class containing an IED Capability Description (ICD) file representation according to the 
# Substation Configuration Language (SCL)
class ICD:
    def __init__(self, contentDescription: str = "ICD File"):
        self.root = ET.Element("SCL", attrib = {
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xmlns:sxi": "http://www.iec.ch/61850/2003/SCLcoordinates",
            "xmlns": "http://www.iec.ch/61850/2003/SCL",
            "xsi:schemaLocation": "http://www.iec.ch/61850/2003/SCL SCL.xsd",
            "version": "2007",
            "revision": "B",
            "release": "4"
        })
        self.header = ET.SubElement(self.root, "Header")
        self.history = ET.SubElement(self.header, "History")
        self.hitem = ET.SubElement(self.history, "Hitem", attrib={
            "version": "1",
            "revision": "0",
            "when": datetime.now().isoformat(),
            "who": "ICD-File-Builder",
            "what": contentDescription
        })

        self.tree = ET.ElementTree(self.root)
    
    def toFile(self, filename):
        # Write to file prettified
        ET.indent(self.tree, space="  ")
        self.tree.write(filename, encoding="utf-8", xml_declaration=True)
