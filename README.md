[![Documentation Status](https://readthedocs.org/projects/iex-parser/badge/?version=latest)](https://iex-parser.readthedocs.io/?badge=latest)

# IEX Data Download and Parsing

This repository contains various C++ and Python files needed to download and parse IEX (Investors Exchange) data. The C++ parsers are designed to efficiently extract data from DEEP pcap files provided by the Investors Exchange (IEX). Currently, it supports the parsing of:

* **Trade reports**
* **Price level updates**

### Key benefits:

* **High-performance parsing**: Significantly faster than Python parsers
* **Multi-timestamp support**: Provides three timestamps for each event:
	+ **Event timestamp** (from the matching engine)
	+ **Packet send timestamp**
	+ **Packet capture timestamp**



## Output
The output CSV file contains parsed trade reports and price level updates.

## Requirements

This requires Linux OS or Windows WSL terminal to run.

## How to use

1. Install this package using pip.
```
pip install -i https://test.pypi.org/simple/ iex-parser
```
2. Create a `symbols.txt` file to filter the desired symbols
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