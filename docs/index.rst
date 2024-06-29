
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



Check out the :doc:`usage` section for further information, including :ref:`installation` of this project.

.. note::

   This project is under active development.

