Financial Markets and Trading
===========================

Introduction
------------

Trading in financial markets involves the buying and selling of financial instruments such as stocks, bonds, commodities, or currencies. This process allows investors and traders to profit from changes in market prices.

Participants
^^^^^^^^^^^^

- **Traders**: Individuals or entities (like institutions or funds) who buy and sell financial instruments.
- **Brokers**: Intermediaries who execute trades on behalf of traders.
- **Exchanges**: Platforms where trading occurs, facilitating the matching of buy and sell orders.

Order Types
^^^^^^^^^^^

Before understanding how trades are executed, it's crucial to know the types of orders traders can place:

- **Market Order**: Executes immediately at the current market price.
- **Limit Order**: Executes only at a specified price or better.
- **Stop Order**: Becomes a market order when a specified price level is reached.
- **Stop-Limit Order**: Becomes a limit order when a specified price level is reached.

Trade Execution Process
^^^^^^^^^^^^^^^^^^^^^^^

1. **Order Placement**: Traders submit orders to buy or sell securities through their brokers. These orders are routed to the relevant exchange where the security is listed.

2. **Matching Orders**: On the exchange, buy orders (bids) are matched with sell orders (asks) based on price and time priority. The exchange's order book displays these orders.

3. **Price Determination**: The current market price is determined by the highest price a buyer is willing to pay (bid) and the lowest price a seller is willing to accept (ask).

4. **Execution**:
   - **Market Orders**: Execute immediately at the best available price.
   - **Limit Orders**: Execute only if the market reaches the specified price or better.
   - **Stop Orders**: Trigger a market order when the stop price is reached.
   - **Stop-Limit Orders**: Trigger a limit order when the stop price is reached, with a specified limit price.

Bids Submission
^^^^^^^^^^^^^^^

Bids refer to buy orders submitted by traders. Here’s how bids are typically submitted:

1. **Selection of Order Type**: Traders choose between market, limit, stop, or stop-limit orders based on their trading strategy and market conditions.

2. **Order Parameters**: Traders specify:
   - Quantity: Number of shares or units to buy.
   - Price: The maximum price they are willing to pay (for limit orders) or the trigger price (for stop orders).
   - Duration: Day order (valid for the current trading day) or good till canceled (remains active until executed or canceled).

3. **Order Transmission**: Orders are transmitted through trading platforms provided by brokers or directly to exchanges.

4. **Order Visibility**: Bids become part of the exchange's order book, where they await matching with appropriate sell orders.




Exchanges and Market Data Dissemination
----------------------------------------

Exchanges
^^^^^^^^^

Exchanges are platforms where financial instruments such as stocks, bonds, commodities, or currencies are traded. They facilitate the matching of buy and sell orders from traders and investors. Exchanges vary in their rules, listing requirements, and trading mechanisms.

Order Handling
^^^^^^^^^^^^^

1. **Order Types**: Traders can place various types of orders including market, limit, stop, and stop-limit orders. These orders are submitted through brokers or directly to the exchange's trading platform.

2. **Order Matching**: Orders are matched based on price and time priority. Buy orders (bids) are matched with sell orders (asks) to execute trades.

3. **Market Mechanics**: Exchanges operate based on centralized order books where buy and sell orders are displayed. The current market price is determined by the best bid and ask prices available.

Market Data Dissemination
^^^^^^^^^^^^^^^^^^^^^^^^^

1. **Real-time Data**: Exchanges disseminate real-time market data including:
   - **Trade Data**: Information about executed trades, including price, volume, and timestamp.
   - **Quote Data**: Bid and ask prices, along with their respective volumes.
   
2. **Historical Data**: Exchanges provide historical market data, allowing traders and analysts to analyze past trends and behavior. This data is crucial for backtesting trading strategies and conducting research.

IEX Market Data
^^^^^^^^^^^^^^^

The Investors Exchange (IEX) provides market data with a focus on transparency and fairness. Historical data from IEX includes:

- **Trade Data**: Detailed records of executed trades, including price, volume, and trade conditions.
- **Quote Data**: Real-time bid and ask prices along with depth-of-book information.
- **Market Metrics**: Additional metrics like market-wide circuit breakers and trading halts.

IEX's market data is accessible through various APIs and data providers, enabling market participants to analyze historical trends and make informed trading decisions.
In the next section, we will explore the various protocols and formats used by IEX to disseminate market data.

IEX Market Data Formats
------------------------

UDP Transmission
^^^^^^^^^^^^^^^^

1. **Data Transmission**: IEX DEEP data is transmitted via UDP (User Datagram Protocol) for low-latency distribution. UDP is preferred for market data to minimize transmission delays and ensure timely updates to market participants.

2. **Packet Structure**: UDP packets contain encoded market data in a structured format. Each packet includes information such as trade prices, volumes, quote updates, and other relevant market metrics.

TCP Capture Format
^^^^^^^^^^^^^^^^^^

1. **Capture Mechanism**: Market participants capture UDP packets containing IEX DEEP data using TCP (Transmission Control Protocol) capture mechanisms. TCP is used for reliable data capture and transmission over networks.

2. **Data Dumping**: Captured UDP packets are decoded and dumped into a more accessible format, such as JSON or CSV, for further analysis and integration into trading systems and analytics platforms.

3. **Data Integrity**: TCP ensures that all UDP packets are captured without loss, providing accurate and complete market data for analysis.

