Package Functions
=================

The package provides the following functions for downloading and parsing historical DEEP data from IEX. The parse functions run a built C++ parser to extract data from the PCAP files. For a detailed explanation of the data format, refer to the :ref:`usage` section.

Download historical data from IEX
-----------------

The package provides a function to download historical data from IEX. The function downloads the data for a specific date and saves it to the specified directory. If the file already exists, the function skips the download.


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


The package offers several functions for parsing historical data from IEX. The `parse_file` function allows for parsing any IEX DEEP file. If you need to download and parse data, you can use the `parse_date` or `parse_dates` functions. Additionally, these functions support splitting the parsed data into separate files based on the symbols present in the data.

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
