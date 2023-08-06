## Installation

```
pip install polygon_protection
```

## Get Started
```python
from polygon_protection import PolygonProtection

# A dictionary defining the set of currency pairs we will be pulling data for
# WARNING: portfolio class can never be found
# it is a self created class which is not published
currency_pairs = [["AUD", "USD", [], portfolio("AUD", "USD")],
                  ["GBP", "EUR", [], portfolio("GBP", "EUR")],
                  ["USD", "CAD", [], portfolio("USD", "CAD")],
                  ["USD", "JPY", [], portfolio("USD", "JPY")],
                  ["USD", "MXN", [], portfolio("USD", "MXN")],
                  ["EUR", "USD", [], portfolio("EUR", "USD")],
                  ["USD", "CNY", [], portfolio("USD", "CNY")],
                  ["USD", "CZK", [], portfolio("USD", "CZK")],
                  ["USD", "PLN", [], portfolio("USD", "PLN")],
                  ["USD", "INR", [], portfolio("USD", "INR")]]

# Run the main data collection loop
PolygonProtection.main(currency_pairs=currency_pairs)
```