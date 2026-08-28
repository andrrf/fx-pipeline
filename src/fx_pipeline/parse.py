import xml.etree.ElementTree as ET
from datetime import date
from decimal import Decimal
from pathlib import Path

NAMESPACE = [
    {"bnr": "https://www.bnr.ro/xsd"},
    {"bnr": "http://www.bnr.ro/xsd"},
]

def detect_namespace(root: ET.Element) -> dict:
    for ns in NAMESPACE:
        if root.findall(".//bnr:Cube", ns):
            return ns
    raise ValueError(f"Unknown namespace in XML: {root.tag}")

def parse_rates(xml_text: str) -> list[dict]:
    root = ET.fromstring(xml_text)
    ns = detect_namespace(root)

    cube = root.find(".//bnr:Cube", ns)
    if cube is None: 
        raise ValueError("The Cube element was not found in the XML.")

    rate_date = date.fromisoformat(cube.attrib["date"])

    rates = []
    for element in cube.findall("bnr:Rate", ns):
        rates.append(
            {
                "rate_date": rate_date,
                "currency": element.attrib["currency"],
                "multiplier": int(element.attrib.get("multiplier", 1)),
                "value": Decimal(element.text),
            }
        )
    return rates

def parse_all_cubes(xml_text: str) -> list[dict]:
    root = ET.fromstring(xml_text)
    ns = detect_namespace(root)

    cubes = root.findall(".//bnr:Cube", ns)
    if not cubes:
        raise ValueError("No Cube elements were found in the XML.")
    
    rates = []
    for cube in cubes:
        rate_date = date.fromisoformat(cube.attrib["date"])
        for element in cube.findall("bnr:Rate", ns):
            rates.append(
                {
                    "rate_date": rate_date,
                    "currency": element.attrib["currency"],
                    "multiplier": int(element.attrib.get("multiplier", 1)),
                    "value": Decimal(element.text),
                }
            )
    return rates

if __name__ == "__main__":
    xml_text = Path("data/sample.xml").read_text(encoding="utf-8")
    rates = parse_rates(xml_text)

    print(f"I found {len(rates)} rates for date {rates[0]['rate_date']}")
    for rate in rates[:3]:
        print(rate)
    for rate in rates:
        if rate["multiplier"] != 1:
            print("with multiplier: ", rate)