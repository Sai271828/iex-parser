.. _requirements:

Requirements
------------

This package contains compiled binaries that can only be run on a Linux machine or a Windows machine with the Windows Subsystem for Linux (WSL) installed. Look at :ref:`unsupported_os` for more information on compiling the binaries for other operating systems.

.. _installation:

Installation
------------

To use the IEX Parser, first install it using pip:

 

.. code-block:: console

   $ pip install iex-cppparser

.. _usage:

Usage
----------------

Create a `symbols.txt` file to filter the desired symbols

.. code-block:: bash

   AAPL
   MSFT


Compile the cpp files by running the following python script

>>> from iex_cppparser import compile_cpp
>>> compile_cpp.compile()

Run the following python script

>>> from iex_cppparser import parse_date
>>> download_folder = ...
>>> parsed_folder = ...
>>> parse_date("2023-10-30",download_folder,parsed_folder,"symbols.txt",download=True)

Output
================


The parsed data will be saved in the `parsed_folder` directory. Currently, two types of data are being parsed: trade reports and price levels. The schemas are as follows

+ Trade report schema


   .. csv-table:: Trade Report Schema
      :header: "Column Name", "Description"
      :widths: 20, 80

      "Packet Capture Time", "The time when the packet was captured in Nanoseconds since epoch."
      "Send Time", "The time when the message was sent in Nanoseconds since epoch."
      "Exchange Timestamp", "The exchange timestamp of the message in Nanoseconds since epoch."
      "Tick Type", "The type of tick (e.g., trade, quote)."
      "Symbol", "The stock symbol (e.g., MSFT, AAPL)."
      "Size", "The size of the trade."
      "Price", "The price of the trade."
      "Trade ID", "The unique identifier for the trade."
      "Sale Condition", "Additional conditions of the sale (e.g., EXTENDED_HOURS, ODD_LOT)."



   Example trades output file

   .. csv-table::

      Packet Capture Time,Send Time,Exchange Timestamp,Tick Type,Symbol,Size,Price,Trade ID,Sale Condition
      1696248433848282112,1696248433848263608,1696248433848175696,T,MSFT,20,316.250000,2546905,EXTENDED_HOURS|ODD_LOT
      1696248522899780096,1696248522899762796,1696248522899669709,T,AAPL,20,171.410000,2683260,EXTENDED_HOURS|ODD_LOT


+ Price Level Update schema
   .. csv-table:: Price Level Update Schema
      :header: "Column Name", "Description"
      :widths: 20, 80

      "Packet Capture Time", "The time when the packet was captured in nanoseconds since epoch."
      "Send Time", "The time when the message was sent in nanoseconds since epoch."
      "Buy_Ask Flag", "The flag indicating whether the price level is a buy or ask price. 1 for Ask"
      "Exchange Timestamp", "The exchange timestamp of the message in nanoseconds since epoch."
      "Tick Type", "The type of tick (e.g., trade, quote)."
      "Symbol", "The stock symbol (e.g., MSFT, AAPL)."
      "Price", "The price of the trade."
      "Size", "The size of the trade."
      "Record Type", "The type of record."
      "Event Flag", "The flag indicating special conditions or states."

   Example Price Level output file

   .. csv-table::

      Packet Capture Time,Send Time, Buy_Ask Flag,Exchange Timestamp,Tick Type,Symbol,Price,Size,Record Type,Event Flag
      1696248000327041024,1696248000326948634,1,1696248000184809932,PRL,MSFT,348.000000,20,R,1
      1696249295813316096,1696249295813302703,1,1696249295813269151,PRL,AAPL,171.130000,243,R,1