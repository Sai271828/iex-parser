# IEX Data Download and Parsing

This repository contains various C++ and Python files needed to download and parse IEX (Investors Exchange) data. Some of the code and logic was taken from [David Lariviere](https://gitlab.engr.illinois.edu/shared_code/iexdownloaderparser)

**IEX Parser**
=============================

The file `iex_parser.cpp` is a  C++ parser designed to efficiently extract data from DEEP pcap files provided by the Investors Exchange (IEX). Currently, it supports the parsing of:

* **Trade reports**
* **Price level updates**

### Key benefits:

* **High-performance parsing**: Significantly faster than Python parsers
* **Multi-timestamp support**: Provides three timestamps for each event:
	+ **Event timestamp** (from the matching engine)
	+ **Packet send timestamp**
	+ **Packet capture timestamp**


### Compilation
To compile the program, ensure you have a C++ compiler installed (e.g., g++). Execute the following command:

```bash
g++ /vagrant/utils/logger.cpp /vagrant/parsers/IEX/src/decode_messages.cpp /vagrant/parsers/IEX/src/iex_parser.cpp -o /vagrant/parsers/IEX/src/iex_parser.out
```
This is dependent on the `logger.cpp` file. If you do not wish to use logger, simply remove all the logging line and compile just the parser.
### How to Use
To utilize the parser, furnish the input pcap file and the output CSV file as command-line arguments:

```bash
gunzip -d -c input.pcap.gz | tcpdump -r - -w - -s 0 | /vagrant/parsers/IEX/src/iex_parser.out /dev/stdin output_folder symbol
```

- input.pcap.gz: The path to the pcap.gz file containing IEX market data.
- output_folder: The path to the folder to save parsed csv files
- symbol:
            `ALL` for parsing all symbols or
            For select symbols, a path to a .txt file with each line a new symbol

### Output
The output CSV file contains parsed trade reports and price level updates. These are stored in CSV files based on the first letter of the symbol. This is done primarily to maintain manageably sized individual parsed CSV files.

**Download and Parse**
======================

The `download_and_parse.py` script automates the downloading of IEX DEEPs (Depth of Book) data for a specified range of dates and symbols, parses the downloaded pcap files, and cleans the data for further analysis. The download portion relies on the `download_dates` function, which is part of the `download_iex_pcaps.py` file.

### How to use

```bash
python3 download_and_parse.py --start-date YYYY-MM-DD --end-date YYYY-MM-DD --download-dir /path/to/download/directory --symbol {symbol}
```

- --start-date: The start date for the data download range.
- --end-date: The end date for the data download range.
- --download-dir: Directory where the downloaded pcap files will be stored.
- --symbol: `ALL` for all symbols or a path to a .txt file with each line a new symbol

The `download_dates` function from `download_iex_pcaps` is **used to download pcap files**. 
To simply use this function run the following line in your python file:
```python
download_dates(download_dir, current_date_str, current_date_str, 'DEEP')
```
**After parsing**, original pcap files are **removed** to conserve space. 