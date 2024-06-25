.. _requirements:




Requirements
------------

The compiled binaries in this package can only be run on a Linux machine or a Windows machine with the Windows Subsystem for Linux (WSL) installed. Look at :ref:`unsupported_os` for more information on compiling the binaries for other operating systems.

.. _installation:

Installation
------------

To use the IEX Parser, first install it using pip:

   
   `Will need to be edited to point to the correct location of the package!!!`

.. code-block:: console

   $ pip install -i https://test.pypi.org/simple/ iex-parser   

.. _usage:

Usage
----------------

Create a `symbols.txt` file to filter the desired symbols

.. code-block:: bash

   AAPL
   MSFT


Run the following python script

>>> from iex_parser import parse_date
>>> download_folder = ...
>>> parsed_folder = ...
>>> parse_date("2023-10-30",download_folder,parsed_folder,"symbols.txt",download=True)

Output
----------------

The parsed data will be saved in the `parsed_folder` directory. The parsed data will be saved in the following format:

.. csv-table:: TRD file
   :header: Packet Capture Time,Send Time,Message ID,Raw Timestamp,Tick Type,Symbol,Size,Price,Trade ID,Sale Condition
   1696248274476274944,1696248274476249406,60091,1696248274475865577,T,MSFT,10,316.350000,2275739,EXTENDED_HOURS|ODD_LOT
   1696248522899780096,1696248522899762796,70817,1696248522899669709,T,AAPL,20,171.410000,2683260,EXTENDED_HOURS|ODD_LOT
