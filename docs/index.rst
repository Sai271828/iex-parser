.. include:: ../README.rst

Contents
========

.. toctree::

   Home <self>
   usage
   functions
   unsupported_os


IEX Parser Documentation
===================================

This package contains various Python functions needed to download and parse IEX (Investors Exchange) data. The parser, using C++ beckend, is designed to efficiently extract data from DEEP pcap files provided by the Investors Exchange (IEX). Currently, it supports the parsing of:

* **Trade reports**
* **Price level updates**

Key benefits:
-----------------------------------

* **High-performance parsing**: Significantly faster than Python parsers
* **Multi-timestamp support**: Provides three timestamps for each event:
	+ **Event timestamp** (from the matching engine)
	+ **Packet send timestamp**
	+ **Packet capture timestamp**

Check out the :doc:`usage` section for further information, including :ref:`installation` of this project.

.. note::

   This project is under active development.

