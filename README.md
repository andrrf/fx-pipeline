# fx-pipeline

ELT pipeline for Romanian National Bank (BNR) exchange rates.

## Data notes (work in progress)

- Source: https://curs.bnr.ro/nbrfxrates.xml (daily), yearly archives at /files/xml/years/
- CAUTION: the XML namespace differs between the daily file (https://www.bnr.ro/xsd)
  and the yearly archives (http://www.bnr.ro/xsd)
- Coverage: 2020-2026, 55,674 rows, 1,668 banking days
- The set of quoted currencies changes over time:
  - HRK last quoted 2022-12-30 (Croatia joined the euro area)
  - BGN last quoted 2025-12-31 (Bulgaria joined the euro area)
  - 7 currencies added on 2024-09-23 (HKD, IDR, ILS, ISK, MYR, PHP, SGD)
- multiplier=100 applies to HUF, IDR, ISK, JPY, KRW