import logging

from fx_pipeline.extract import fetch_raw_xml
from fx_pipeline.load import load_rates
from fx_pipeline.parse import parse_rates

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

def run() -> int:
    logger.info("Starting the data extraction from the BNR")
    xml_text = fetch_raw_xml()
    logger.info("Received %d characters", len(xml_text))

    rates = parse_rates(xml_text)
    logger.info("Parsed %d rates for %s", len(rates), rates[0]["rate_date"])

    loaded = load_rates(rates)
    logger.info("Loaded %d rows in raw.fx_rates", loaded)

    return loaded

if __name__ == "__main__":
    run()