from fx_pipeline.db import get_connection

UPSERT_SQL = """
    INSERT INTO raw.fx_rates (rate_date, currency, multiplier, value)
    VALUES (%(rate_date)s, %(currency)s, %(multiplier)s, %(value)s)
    ON CONFLICT (rate_date, currency) DO UPDATE
    SET multiplier = EXCLUDED.multiplier,
        value = EXCLUDED.value,
        ingested_at = now()
"""

def load_rates(rates: list[dict]) -> int:
    if not rates:
        return 0

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.executemany(UPSERT_SQL, rates)
            return cursor.rowcount

if __name__ == "__main__":
    from pathlib import Path

    from fx_pipeline.parse import parse_rates

    xml_text = Path("data/sample.xml").read_text(encoding="utf-8")
    rates = parse_rates(xml_text)
    inserted = load_rates(rates)
    print(f"Inserted {inserted} rows")