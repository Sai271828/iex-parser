Package Functions
=================


Download historical data from IEX
-----------------

The following functions are available for downloading historical data from IEX.


.. autofunction:: iex_cppparser.download.download_hist_file

**Example Usage:**

.. code-block:: python

    from iex_cppparser.download import download_hist_file

    success = download_hist_file("20230625", "/path/to/download")
    if success:
        print("File downloaded or already exists.")
    else:
        print("File download failed.")

Parse historical data from IEX
------------------



.. autofunction:: iex_cppparser.parse_file

**Input Parameters:**

- `file_path (str)`: The path to the file to be parsed.
- `parsed_folder (str)`: The path to the folder where the parsed output should be saved.
- `symbol (str)`: Path to a txt file with symbols to parse. Must have one symbol per line. If "ALL", all symbols are parsed.
- `split (bool)`: Whether to split the output files. One file per letter of the alphabet is generated. Default is False.

**Returns:**

- `None`

**Example Usage:**

.. code-block:: python

    from iex_cppparser import parse_file

    parse_file("data_feeds_20230625.pcap.gz", "/path/to/parsed", "symbols.txt", split=True)



.. autofunction:: iex_cppparser.parse_date

**Input Parameters:**

- `date_str (str)`: The date string to be parsed. Format YYYY-MM-DD.
- `download_dir (str)`: The directory where the files are downloaded.
- `parsed_folder (str)`: The directory where the parsed output should be saved.
- `symbol (str)`: Path to a txt file with symbols to parse. Must have one symbol per line. If "ALL", all symbols are parsed.
- `download (bool)`: Whether to download the files. Default is True.
- `split (bool)`: Whether to split the output files. One file per letter of the alphabet is generated. Default is False.

**Returns:**

- `None`

**Example Usage:**

.. code-block:: python

    from iex_cppparser import parse_date

    parse_date("2023-06-25", "/path/to/download", "/path/to/parsed", "symbols.txt", download=True, split=False)


.. autofunction:: iex_cppparser.parse_dates

**Input Parameters:**

- `start_date (str)`: The start date string in the format YYYY-MM-DD.
- `end_date (str)`: The end date string in the format YYYY-MM-DD.
- `download_dir (str)`: The directory where the files are downloaded.
- `parsed_folder (str)`: The directory where the parsed output should be saved.
- `symbol (str)`: Path to a txt file with symbols to parse. Must have one symbol per line. If "ALL", all symbols are parsed.
- `download (bool)`: Whether to download the files. Default is False.
- `split (bool)`: Whether to split the output files. One file per letter of the alphabet is generated. Default is False.

**Returns:**

- `None`

**Example Usage:**

.. code-block:: python

    from iex_cppparser import parse_dates

    parse_dates("2023-06-25", "2023-06-30", "/path/to/download", "/path/to/parsed", "symbols.txt", download=False, split=True)
