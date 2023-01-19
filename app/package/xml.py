from xml.dom import minidom
from .rate.transformer import BestChangeDTO
from typing import List

def build_rate_xml(collection: List[BestChangeDTO]):
    root = minidom.Document()

    xml = root.createElement('rates')

    for item in collection:
        subroot = root.createElement('item')
        root.appendChild(subroot)
        xml.appendChild(subroot)

        for field in item.get_dict().keys():
            element = root.createElement(field)
            element.appendChild(root.createTextNode(item.get_dict().get(field)))
            subroot.appendChild(element)

    return xml.toxml()
