[![Documentation Status](https://readthedocs.org/projects/iex-parser/badge/?version=latest)](https://iex-parser.readthedocs.io/?badge=latest)

# IEX Data Download and Parsing

The IEX exchange offers two types of historical data: DEEP and TOPS, both provided as PCAP files capturing network activity. This package provides a convenient API for extracting data from DEEP files. These files contain various types of messages, such as trade reports, bid submissions, security messages etc. Currently, our package supports parsing two specific types of messages:

* **Trade reports** - Detailed records of executed trades.
* **Price level updates** - Information about changes in the bid and ask price levels.

### Key benefits:

* **High-performance parsing**: Significantly faster than the available Python parsers
* **Multi-timestamp support**: Provides three timestamps for each event:
	+ **Event timestamp** (from the matching engine)
	+ **Packet send timestamp**
	+ **Packet capture timestamp**

## Requirements

This requires Linux OS or Windows WSL terminal to run. It also requires additional softwares that are listed at [requirements](https://iex-parser.readthedocs.io/usage.html).

## How to use

1. Install this package using pip.
### UPDATE AFTER MIGRATION!!!
```
pip install -i https://test.pypi.org/simple/ iex-parser
```
1. Create a `symbols.txt` file to filter the desired symbols
```
AAPL
MSFT

```
3. Run the following python script
```
from iex_parser import parse_date

download_folder = ...

parsed_folder = ...

parse_date("2023-10-30",download_folder,parsed_folder,"symbols.txt")
```

## Output
The output CSV file contains parsed trade reports and price level updates.