Package Functions
=================


Download historical data from IEX
-----------------

The following functions are available for downloading historical data from IEX.


.. autofunction:: iex_cppparser.download.download_hist_file

**Example Usage:**

.. code-block:: python

    from iex_cppparser.download import download_hist_file

    success = download_hist_file("20231010", "/path/to/download")
    if success:
        print("File downloaded or already exists.")
    else:
        print("File download failed.")

Parse historical data from IEX
------------------



.. autofunction:: iex_cppparser.parse_file



**Example Usage:**

.. code-block:: python

    from iex_cppparser import parse_file

    parse_file("data_feeds_20231010_20231010_IEXTP1_DEEP1.0.pcap.gz", "/path/to/parsed", "symbols.txt", split=True)



.. autofunction:: iex_cppparser.parse_date



**Example Usage:**

.. code-block:: python

    from iex_cppparser import parse_date

    parse_date("2023-10-10", "/path/to/download", "/path/to/parsed", "symbols.txt", download=True, split=False)


.. autofunction:: iex_cppparser.parse_dates




**Example Usage:**

.. code-block:: python

    from iex_cppparser import parse_dates

    parse_dates("2023-10-10", "2023-10-12", "/path/to/download", "/path/to/parsed", "symbols.txt", download=False, split=True)
