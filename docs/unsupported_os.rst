
.. _unsupported_os:

Unsupported OS
==============

To compile the program, ensure you have a C++ compiler installed (e.g., g++) and cd into the cpp directory after cloning the project repository. Execute the following commands:

.. code-block:: bash

    g++ -O2 logger.cpp decode_messages.cpp iex_parser_threaded.cpp -o iex_parser_threaded.out -pthread
    g++ -O2 logger.cpp decode_messages.cpp iex_parser.cpp -o iex_parser.out
    g++ -O2 logger.cpp decode_messages.cpp iex_parser_split.cpp -o iex_parser_split.out

This is dependent on the `logger.cpp` file. If you do not wish to use logger, simply remove all the logging line and compile just the parser.

How to Use
----------

To utilize the parser, furnish the input pcap file and the output CSV file as command-line arguments:

.. code-block:: bash
    
    gunzip -d -c input.pcap.gz | tcpdump -r - -w - -s 0 | iex_parser.out /dev/stdin output_folder symbol


- input.pcap.gz: The path to the pcap.gz file containing IEX market data.
- output_folder: The path to the folder to save parsed csv files
- symbol:
    - `ALL` for parsing all symbols or
    - For select symbols, a path to a .txt file with each line a new symbol
