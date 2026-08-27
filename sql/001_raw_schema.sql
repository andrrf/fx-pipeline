CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.fx_rates (
    rate_date DATE NOT NULL,
    currency CHAR(3) NOT NULL,
    multiplier INTEGER NOT NULL DEFAULT 1,
    value NUMERIC(18, 6) NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT pk_fx_rates PRIMARY KEY (rate_date, currency)
);

COMMENT ON TABLE raw.fx_rates IS 'BNR exchange rates, exactly as in the source XML. No transformations.';
COMMENT ON COLUMN raw.fx_rates.value IS 'Gross value; it is devided by the multiplier only at the staging stage.'; 