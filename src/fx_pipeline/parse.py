import xml.etree.ElementTree as ET
from datetime import date
from decimal import Decimal
from pathlib import Path

NAMESPACE = {"bnr": "https://www.bnr.ro/xsd"}

def parse_rates(xml_text: str) -> list[dict]:
    root = ET.fromstring(xml_text)

    cube = root.find(".//bnr:Cube", NAMESPACE)
    if cube is None: 
        raise ValueError("The Cube element was not found in the XML.")

    rate_date = date.fromisoformat(cube.attrib["date"])

    rates = []
    for element in cube.findall("bnr:Rate", NAMESPACE):
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