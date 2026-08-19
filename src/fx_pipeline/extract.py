import httpx

BNR_URL = "https://curs.bnr.ro/nbrfxrates.xml"
HEADERS = {"User-Agent": "fx-pipeline/0.1 (educational project)"}

def fetch_raw_xml() -> str:
    response = httpx.get(BNR_URL, headers=HEADERS, timeout=30.0)
    response.raise_for_status()
    return response.text

if __name__ == "__main__":
    xml = fetch_raw_xml()
    print(xml[:500])