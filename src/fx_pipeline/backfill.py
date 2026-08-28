import logging
import time

import httpx

from fx_pipeline.extract import HEADERS
from fx_pipeline.load import load_rates
from fx_pipeline.parse import parse_all_cubes

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

YEAR_URL = "https://curs.bnr.ro/files/xml/years/nbrfxrates{year}.xml"

def fetch_year(year: int) ->str:
    url = YEAR_URL.format(year=year)
    logger.info("Downloading %s", url)
    response = httpx.get(url, headers=HEADERS, timeout=60.0)
    response.raise_for_status()
    return response.text

def backfill(start_year: int, end_year: int) -> None:
    total = 0
    for year in range(start_year, end_year + 1):
        xml_text = fetch_year(year)
        rates = parse_all_cubes(xml_text)
        loaded = load_rates(rates)
        total += loaded
        logger.info("Year %d: %d rows loaded", year, loaded)
        time.sleep(2)

    logger.info("Total: %d rows", total)

if __name__ == "__main__":
    backfill(2020, 2026)