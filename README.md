[![Documentation Status](https://readthedocs.org/projects/iex-parser/badge/?version=latest)](https://iex-parser.readthedocs.io/?badge=latest)
[![Downloads](https://static.pepy.tech/badge/iex-cppparser)](https://pepy.tech/project/iex-cppparser)
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
  
These timestamps provide insights into the time delay between event occurrence time and the data reception time, enabling more accurate backtesting. For a more detailed explanation of Market data see [market data format](https://iex-parser.readthedocs.io/iex_format.html).
* **Easy-to-use API**: Provides a simple interface for extracting data from DEEP files.
* **OneTick compatibility**: The output format is compatible with OneTick, a popular time-series database for financial data.
## Requirements

This requires Linux OS or Windows WSL terminal to run. It also requires additional softwares that are listed at [requirements](https://iex-parser.readthedocs.io/usage.html).

## How to use

1. Install this package using pip.

```
pip install iex-cppparser
```
1. Create a `symbols.txt` file to filter the desired symbols
```
AAPL
MSFT

```
3. Run the following python script
```
from iex_cppparser import parse_date

download_folder = ...

parsed_folder = ...

parse_date("2023-10-30",download_folder,parsed_folder,"symbols.txt")
```

For an extensive list of parsing and downloading functions see [documentation](https://iex-parser.readthedocs.io/functions.html).

## Output
The output CSV file contains parsed trade reports and price level updates.

## Acknowledgement

This project extends the work of the authors done as part of  IE 421 course at [University of Illinois Urbana-Champaign](https://illinois.edu/). The previous project repository can be found at [this link](https://gitlab.engr.illinois.edu/ie421_high_frequency_trading_spring_2024/ie421_hft_spring_2024_group_03/group_03_project) (a private UIUC repository at the time of this writing).


## Citing this Work

To cite this work in academic papers or publications, you can use the following BibTeX format:

```bibtex
@misc{bavisettyvasu,
  author       = {Bavisetty, Venkata Sai Narayana and Vasu, Karthik},
  title        = {IEX C++ Parser},
  year         = {2024},
  publisher    = {GitHub},
  journal      = {GitHub Repository},
  howpublished = {\url{[Repository URL](https://github.com/Sai271828/iex-parser)}}
}
```