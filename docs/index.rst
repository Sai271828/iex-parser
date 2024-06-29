
Contents
========

.. toctree::
   :maxdepth: 1

   Home <self>
   usage
   functions
   unsupported_os
   iex_format


IEX Parser Documentation
===================================

The IEX exchange offers two types of historical data: DEEP and TOPS, both provided as PCAP files capturing network activity (see :doc:`iex_format` for more details). This package provides a convenient API for extracting data from DEEP files . These files contain various types of messages, such as trade reports, bid submissions, security messages, etc. Currently, our package supports parsing two specific types of messages:

* **Trade reports** - Detailed records of executed trades.
* **Price level updates** - Information about changes in the bid and ask price levels.

Key benefits:
=============

* **High-performance parsing**: Significantly faster than other available Python parsers.
* **Multi-timestamp support**: Provides three timestamps for each event.

      * **Event timestamp**: Indicates when the event happened in the matching engine.
      * **Packet send timestamp**: Indicates when the packet was sent.
      * **Packet capture timestamp**: Indicates when the packet was captured.
      These timestamps provide insights into the time delay between event occurrence time and the data reception time, enabling more accurate backtesting.
* **Easy-to-use API**: Provides a simple interface for extracting data from DEEP files.
* **OneTick compatibility**: The output format is compatible with OneTick, a popular time-series database for financial data.
For detailed information on the essential software requirements, consult the :doc:`usage` section. To find instructions for installation, refer to :ref:`installation`.


Acknowledgement
===============

This project extends the work of the authors done as part of IE 421 course at `University of Illinois Urbana-Champaign <https://illinois.edu/>`_. The previous project repository can be found at `this link <https://gitlab.engr.illinois.edu/ie421_high_frequency_trading_spring_2024/ie421_hft_spring_2024_group_03/group_03_project>`_ (a private UIUC repository at the time of this writing).

Citing this Work
================

To cite this work in academic papers or publications, you can use the following BibTeX format::

    @misc{bavisettyvasu,
      author       = {Bavisetty, Venkata Sai Narayana and Vasu, Karthik},
      title        = {IEX C++ Parser},
      year         = {2024},
      publisher    = {GitHub},
      journal      = {GitHub Repository},
      howpublished = {\url{[Repository URL](https://github.com/Sai271828/iex-parser)}}
    }

.. note::

   This project is under active development.

