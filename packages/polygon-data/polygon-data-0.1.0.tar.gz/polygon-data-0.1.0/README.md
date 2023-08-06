# Polygon Data
A library for fetching real-time forex data from polygon.io and store it into sqlite db.
The library has PolygonDataFetch class which has the main function of max code in the fetchData function of library.

It also includes `ts_to_datetime()`, `reset_raw_data_tables()`, `initialize_raw_data_tables()`, `initialize_aggregated_tables()`,
`aggregate_raw_data_tables()` functions which were the dependency for max christs main funtion.


### Installation
```
pip install polygon_data
```

### Dependency
```
polygon-api-client==0.2.11
sqlalchemy
math
datetime
time
```

### Get started
How to fetch data with this lib?

(Note: Make sure you have a directory named `sqlite` at the root level)

```Python
from polygon_data import PolygonDataFetch

# Instantiate a PolygonDataFetch object
polygonDataFetch = PolygonDataFetch()

# A dictionary defining the set of currency pairs we will be pulling data for
currency_pairs = [["AUD","USD",[],portfolio("AUD","USD")],
                  ["GBP","EUR",[],portfolio("GBP","EUR")],
                  ["USD","CAD",[],portfolio("USD","CAD")],
                  ["USD","JPY",[],portfolio("USD","JPY")],
                  ["USD","MXN",[],portfolio("USD","MXN")],
                  ["EUR","USD",[],portfolio("EUR","USD")],
                  ["USD","CNY",[],portfolio("USD","CNY")],
                  ["USD","CZK",[],portfolio("USD","CZK")],
                  ["USD","PLN",[],portfolio("USD","PLN")],
                  ["USD","INR",[],portfolio("USD","INR")]]

# Call the fetchData method and pass currency_pairs dictionary as a parameter
polygonDataFetch.fetchData(currency_pairs = currency_pairs)
```