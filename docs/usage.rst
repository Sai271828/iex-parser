Usage
=====

.. _requirements:

Requirements
------------

The compiled binaries in this package can only be run on a Linux machine or a Windows machine with the Windows Subsystem for Linux (WSL) installed.

.. _installation:

Installation
------------

To use the IEX Parser, first install it using pip:

.. code-block:: console

   $ pip install -i https://test.pypi.org/simple/ iex-parser

.. _download_and_parse:

Downloading and Parsing data
----------------

Create a `symbols.txt` file to filter the desired symbols
.. code-block:: console
   AAPL
   MSFT

Run the following python script

>>> from iex_parser import parse_date

>>> download_folder = ...
>>> parsed_folder = ...

>>> parse_date("2023-10-30",download_folder,parsed_folder,"symbols.txt",download=True)
