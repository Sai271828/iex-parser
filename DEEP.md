```
Copyright © 2025 Investors’ Exchange LLC. All rights reserved. This document may not be modified, reproduced, or redistributed without the written permission of IEX Group, Inc.
```
# INVESTORS EXCHANGE

# DEEP+ SPECIFICATION

Version 1.

Updated: January 14, 202 5


## Table of Contents

- OVERVIEW
- TRANSPORT PROTOCOL OPTIONS
- ARCHITECTURE
- DATA TYPES
- NETWORK DETAILS
- ADMINISTRATIVE MESSAGE FORMATS
   - System Event Message – S (0x53)
   - Security Directory Message – D (0x44)
   - Trading Status Message – H (0x48)
   - Retail Liquidity Indicator Message – I (0x49) .....................................................................................................................................
   - Operational Halt Status Message – O (0x4f) ......................................................................................................................................
   - Short Sale Price Test Status Message – P (0x50)
   - Security Event Message – E (0x45) .......................................................................................................................................................
- TRADING MESSAGE FORMATS.............................................................................................................................................
   - Add Order Message – a (0x61)...............................................................................................................................................................
   - Order Modify Message – M (0x4D)
   - Order Delete Message – R (0x52)
   - Order Executed Message – L (0x4C)
   - Trade Message – T (0x54)......................................................................................................................................................................
   - Trade Break Message – B (0x42) ...........................................................................................................................................................
   - Clear Book Message – C (0x43)
- APPENDIX A: FLAGS
- APPENDIX B: BITWISE REPRESENTATION
- APPENDIX C: STATE DIAGRAMS
- REVISION HISTORY


## OVERVIEW

Participants of Investors Exchange (“IEX” or the “Exchange”) may use DEEP+ to receive real-time, order-by-order depth

of book quotations and last sale information direct from IEX. DEEP+ also supports several security-related

administrative messages and provides event controls, such as start of day and end of day, to participants.

The depth of book quotations received via DEEP+ provide an order-by-order view of resting displayed orders a. Non-

displayed orders and non-displayed portions of reserve orders are not represented in DEEP+. DEEP+ also provides last

trade price and size information. Trades resulting from either displayed or non-displayed orders matching on IEX will be

reported. Routed executions are not reported.

Subscribers with bandwidth concerns may consume depth of book aggregated market data via the IEX DEEP protocol,

or top of book market data via the IEX TOPS protocol.

DEEP+ provides short sale restriction status, trading status, operational halt status, and security event information via

security-related administrative messages. Lastly, DEEP+ provides event information about the market and data feed via

administrative messages.

DEEP+ cannot be used to enter orders. For order entry, refer to the IEX FIX Specification.

IEX also offers a DEEP+ SNAP service, which is intended to augment the DEEP+ gap-fill service by adding a separate

snapshot protocol. Please refer to IEX DEEP+ SNAP Specification.

For ordering information, contact IEX Market Operations at 646.343.2310 or marketops@iextrading.com or simply

submit a completed IEX Data Subscriber Agreement and Forms. Please see the IEX Connectivity Manual for additional

information.


## TRANSPORT PROTOCOL OPTIONS

For direct data feed subscribers, IEX provides DEEP+ using the IEX Transport Protocol (IEX-TP) on UDP multicast for

sequenced delivery. Additionally, IEX provides retransmission of DEEP+ data (i.e., gap fills) using IEX-TP on TCP or UDP

unicast. See the IEX Transport Specification for details on sequenced delivery and requesting delivery of missed data.

Protocol Identification on IEX-TP

- Message Protocol ID: 0x
- Channel ID: 1

## ARCHITECTURE

DEEP+ is made up of a series of sequenced messages. Each message is variable in length based on the message type.

IEX reserves the right to add message types and grow the length of any messages without notice. Subscribers should

develop their decoders to deal with unknown message types and messages that grow beyond the expected length.

Messages will only be grown to add additional data to the end of a message or to add additional flag values at the end

of a flags field. The messages that make up the data feed are delivered using a lower-level protocol that takes care of

sequencing and delivery guarantees. Note that a Message Length field is provided with every message as part of

## framing defined in IEX-TP.


## DATA TYPES

- String: Fixed-length ASCII byte sequence, left justified and space filled on the right
- Long: 8 bytes, signed integer
- Price: 8 bytes, signed integer containing a fixed-point number with 4 digits to the right of an implied decimal
    point
- Integer: 4 bytes, unsigned integer
- Byte: 1 byte, unsigned integer
- Timestamp: 8 bytes, signed integer containing a counter of nanoseconds since POSIX (Epoch) time UTC
- Event Time: 4 bytes, unsigned integer containing a counter of seconds since POSIX (Epoch) time UTC

All binary fields are in **little endian** format.

Note that each byte is represented by two hexadecimal digits in the examples within this specification.

### Timestamp Relationships

Timestamps establish a total ordering of a _happened-before_ relationship within the IEX Trading System. If Message A

has a lower Timestamp than Message B, then the event causing Message A happened before (i.e., preceded) the event

causing Message B. Messages with the same Timestamp (regardless of Message Type or Symbol) were caused by the

same event and may be interpreted to have happened simultaneously and atomically within the IEX Trading System.

For a given <Message Type, Symbol> pairing, the subsequence of messages matching this <Message Type, Symbol>

pairing on the data feed will have a progression of Timestamps which either remain equal (due to simultaneity) or

increase (due to precedence) — within this subsequence Timestamps will never decrease.

No progression of Timestamps between messages having different Symbols may be expected. No progression of

Timestamps between messages having the same Symbol but different Message Type may be expected, except in the

following circumstance:

- The receipt of a Security Event Message for a given security implies that all preceding Price Level Update
    Messages for the same security have been transmitted.


## NETWORK DETAILS

### Multicast Addresses

```
SITE XC Type Group Port Source IP Subnet
```
```
IEX POP
```
```
(Equinix NY5)
```
```
Primary (A) 233.215.21.8 10378 23.226.155.128/
```
```
Secondary (B) 233.215.21.138 10378 23.226.155.192/
```
```
Disaster Recovery
```
```
(Equinix CH4)
```
```
Tertiary (C)
233.215.21.
```
```
10378 23.226.155. 176 /
```
```
IEX Testing Facility (“ITF”)
(Equinix NY5)
```
```
ITF (I)
233.215.21.
```
```
32001 23.226.155.8/
```
### Unicast Gap Fill Details

Gap Fill Server Configuration

- Supported Retransmission Protocol(s): TCP and UDP
- Maximum UDP Retransmission Response: 1,000 messages per Retransmission Request
- Maximum TCP Retransmission Response: N/A (there is no limit to the retransmission response via TCP)
- Supported Request Type(s): Sequenced Messages

UDP Gap Fill Server Addresses

```
SITE XC Type Server Port
```
```
IEX POP
```
```
(Equinix NY5)
```
```
Primary (A) 23.226.155. 170 11378
```
```
Secondary (B) 23.226.155. 234 11378
```
```
Disaster Recovery
(Equinix CH4)
```
```
Tertiary (C) 23.226.155.251 11378
```
```
IEX Testing Facility
(Equinix NY5)
```
```
ITF (I) 23.226.155.20 33001
```

TCP Gap Fill Server Addresses

```
SITE XC Type Server Port
```
```
IEX POP
```
```
(Equinix NY5)
```
```
Primary (A) 23.226.155. 171 11378
```
```
Secondary (B) 23.226.155. 235 11 378
```
```
Disaster Recovery
(Equinix CH4)
```
```
Tertiary (C) 23.226.155.252 11378
```
```
IEX Testing Facility
(Equinix NY5)
```
```
ITF (I) 23.226.155.21 33001
```
### PIM RP Configuration Examples

```
SITE XC Type PIM RP Statement Sample*
```
```
IEX POP
(Equinix NY5)
```
```
Primary (A) ip pim rp-address x.x.x.x 233.215 .21.0/
```
```
Secondary (B) ip pim rp-address y.y.y.y 233.215 .21.128/
```
```
Disaster Recovery
```
```
(Equinix CH4)
```
```
Tertiary (C) ip pim rp-address z.z.z.z 233.215.21.64/
```
```
IEX Testing Facility
(Equinix NY5)
```
```
ITF (I) ip pim rp-address i.i.i.i 233.215.21.240/
```
* x.x.x.x, y.y.y.y, z.z.z.z, and i.i.i.i in above samples refer to respective IEX-side BGP Peer IPs.

Please note that this is only one of several ways to configure multicast. Additionally, RP IPs are not advertised at this

time.

IEX statically subscribes and floods individual data feed multicast groups to applicable direct data feed subscribers on

### cross-connects designated A, B, C, or I.

### Network Prefixes A dvertised

```
SITE XC Type Market Data Unicast Prefixes Advertised
```
```
IEX POP
```
```
(Equinix NY5)
```
```
Primary (A)
```
```
23.226.155.128/28 (Multicast Sources)
```
```
23.226.155.160/28 (Gap Fill Servers)
```
```
Secondary (B)
```
```
23.226.155.192/28 (Multicast Sources)
```
```
23.226.155.224/28 (Gap Fill Servers)
```
```
Disaster Recovery
(Equinix CH4)
```
```
Tertiary (C)
```
```
23.226.155.176/28 (Multicast Sources)
23.226.155.240/28 (Gap Fill Servers)
```
```
IEX Testing Facility
(Equinix NY5)
```
```
ITF (I)
```
```
23.226.155.8/29 (Multicast Source)
23.226.155.16/29 (Gap Fill Servers)
```

## ADMINISTRATIVE MESSAGE FORMATS

### System Event Message – S (0x53)

The System Event Message is used to indicate events that apply to the market or the data feed.

There will be a single message disseminated per channel for each System Event type within a given trading session.

```
Field Name Offset Length Type Description/Notes
```
```
Message Type 0 1 Byte ‘S’ (0x53) – System Event
```
```
System Event 1 1 Byte
```
```
System event identifier
```
- ‘O’ (0x4f): _Start of Messages_ – Outside of
    heartbeat messages on the lower level
    protocol, the start of day message is the first
    message sent in any trading session.
- ‘S’ (0x53): _Start of System Hours_ – This
    message indicates that IEX is open and
    ready to start accepting orders.
- ‘R’ (0x52): _Start of Regular Market Hours_ –
    This message indicates that DAY and GTX
    orders, as well as market orders and pegged
    orders, are available for execution on IEX.
- ‘M’ (0x4d): _End of Regular Market Hours_ –
    This message indicates that DAY orders,
    market orders, and pegged orders are no
    longer accepted by IEX.
- ‘E’ (0x45): _End of System Hours_ – This
    message indicates that IEX is now closed
    and will not accept any new orders during
    this trading session. It is still possible to
    receive messages after the end of day.
- ‘C’ (0x43): _End of Messages_ – This is always
    the last message sent in any trading session.

```
Timestamp 2 8 Timestamp Time stamp of the system event
```
Total Message Data length is 10 bytes. See Appendix B for the bitwise representation.

Example

Message Type 53 // S = System Event

System Event 45 // End of System Hours

Timestamp 00 a0 99 97 e9 3d b6 14 // 2017-04-17 17:00:00.


### Security Directory Message – D (0x44)

IEX disseminates a full pre-market spin of Security Directory Messages for all IEX-listed securities. After the pre-market

spin, IEX will use the Security Directory Message to relay changes for an individual security.

```
Field Name Offset Length Type Description/Notes
```
```
Message Type 0 1 Byte ‘D’ (0x44) – Security Directory
```
```
Flags 1 1 Byte See Appendix A for flag values
```
```
Timestamp 2 8 Timestamp Time stamp of the security information
```
```
Symbol 10 8 String
```
```
Security identifier represented in Nasdaq
Integrated symbology
```
```
Round Lot Size 18 4 Integer Number of shares that represent a round lot
```
```
Adjusted POC Price 22 8 Price
```
```
Corporate action adjusted previous official closing
price
```
```
LULD Tier 30 1 Byte
```
```
Indicates which Limit Up-Limit Down price band
calculation parameter is to be used
```
- 0 (0x0): Not applicable
- 1 (0x1): Tier 1 NMS Stock
- 2 (0x2): Tier 2 NMS Stock

Total Message Data length is 31 bytes. See Appendix B for the bitwise representation.

Example

Message Type 44 // D = Security Directory

Flags 80 // Test security, not an ETP,
not a When Issued security
Timestamp 00 20 89 7b 5a 1f b6 14 // 2017-04-17 07:40:00.

Symbol 5a 49 45 58 54 20 20 20 // ZIEXT

Round Lot Size 64 00 00 00 // 100 shares

Adjusted POC Price 24 1d 0f 00 00 00 00 00 // $99.

LULD Tier 01 // Tier 1 NMS Stock


### Trading Status Message – H (0x48)

The Trading Status Message is used to indicate the current trading status of a security. For securities eligible for

trading, IEX abides by any regulatory trading halts and trading pauses instituted by the primary or listing market, as

applicable.

IEX disseminates a full pre-market spin of Trading Status Messages indicating the trading status of all securities. In the

spin, IEX will send out a Trading Status Message with “T” (Trading) for all securities that are eligible for trading at the

start of the Pre-Market Session. If a security is absent from the dissemination, firms should assume that the security is

being treated as operationally halted in the IEX Trading System.

After the pre-market spin, IEX will use the Trading Status Message to relay changes in trading status for an individual

security. Messages will be sent when a security is:

- Halted
- Paused*
- Released into an Order Acceptance Period*
- Released for trading

* The paused and released into an Order Acceptance Period status will be disseminated for IEX-listed securities only.

Trading pauses on non-IEX-listed securities will be treated simply as a halt.

```
Field Name Offset Length Type Description/Notes
```
```
Message Type 0 1 Byte ‘H’ (0x48) –Trading Status
```
```
Trading Status 1 1 Byte
```
```
Trading status identifier
Trading Status will be set to “H” (Trading Halt)
when a non-IEX-listed security is paused by the
listing exchange.
```
- ‘H’ (0x48): Trading halted across all US
    equity marketsr‘O’ (0x4f): Trading halt
    released into an Order Acceptance Period
    on IEX (IEX-listed securities only)
- ‘P’ (0x50): Trading paused and Order
    Acceptance Period on IEX (IEX-listed
    securities only)
- ‘T’ (0x54): Trading on IEX

```
Timestamp 2 8 Timestamp Time stamp of the trading status
```
```
Symbol 10 8 String
```
```
Security identifier represented in Nasdaq
Integrated symbology
```
```
Reason 18 4 String
```
```
Reason for the trading status change
IEX populates the Reason field for IEX-listed
securities when the Trading Status is “H” (Trading
Halt) or “O” (Order Acceptance Period). For non-
IEX-listed securities, the Reason field will be set to
“NA” (Reason Not Available) when the Trading
Status is “H” (Trading Halt). The Reason will be
```

```
blank when the Trading Status is “P” (Trading
Pause and Order Acceptance Period) or “T”
(Trading).
```
- Trading Halt Reasons
    o T1: Halt News Pending
    o IPO1: IPO Not Yet Trading
    o IPOD: IPO Deferred
    o MCB3: Market-Wide Circuit Breaker
       Level 3 – Breached
    o NA: Reason Not Available
- Order Acceptance Period Reasons
    o T2: Halt News Dissemination
    o IPO2: IPO Order Acceptance Period
    o IPO3: IPO Pre-Launch Period
    o MCB1: Market-Wide Circuit Breaker
       Level 1 – Breached
    o MCB2: Market-Wide Circuit Breaker
       Level 2 – Breached

Total Message Data length is 22 bytes. See Appendix B for the bitwise representation.

Example

Message Type 48 // H = Trading Status

Trading Status 48 // H = Trading Halted

Timestamp ac 63 c0 20 96 86 6d 14 // 2016-08-23 15:30:32.

Symbol 5a 49 45 58 54 20 20 20 // ZIEXT

Reason 54 31 20 20 // T1 = Halt News Pending

State Diagram

See Appendix C for a state diagram illustrating the potential Trading Status and Reason transitions.


### Retail Liquidity Indicator Message – I (0x49) .....................................................................................................................................

DEEP+ broadcasts a real-time Retail Liquidity Indicator Message each time there is an update to IEX's eligible retail

liquidity interest during the trading day. Prior to the start of trading, IEX publishes a "no interest indicator" (Retail

Liquidity Indicator is set to '0x20') for all symbols in the IEX Trading System.

```
Field Name Offset Length Type Description/Notes
```
```
Message Type 0 1 Byte 'I' (0x49) - Retail Liquidity Indicator Message
```
```
Retail Liquidity Indicator 1 1 Byte
```
```
Retail Liquidity Indicator identifier
```
- [space] (0x20) - Retail indicator not
    applicable
- 'A' (0x41) - Buy interest for Retail
- 'B' (0x42) - Sell interest for Retail
- 'C' (0x43) - Buy and sell interest for Retail

```
Timestamp 2 8 Timestamp
```
```
Time stamp of the Retail Liquidity Indicator
Message
```
```
Symbol 10 8 String
```
```
Security identifier represented in Nasdaq
Integrated symbology
```
Total Message Data length is 18 bytes. See Appendix B for the bitwise representation.

Example

Message Type 49 // I = Retail Liquidity Indicator Message

Retail Liquidity Indicator 41 // A = Buy Interest for Retail

Timestamp ac 63 c0 20 96 86 6d 14 // 2016-08-23 15:30:32.

Symbol 5a 49 45 58 54 20 20 20 // ZIEXT


### Operational Halt Status Message – O (0x4f) ......................................................................................................................................

The Exchange may suspend trading of one or more securities on IEX for operational reasons and indicates such

operational halt using the Operational Halt Status Message.

IEX disseminates a full pre-market spin of Operational Halt Status Messages indicating the operational halt status of all

securities. In the spin, IEX will send out an Operational Halt Message with “N” (Not operationally halted on IEX) for all

securities that are eligible for trading at the start of the Pre-Market Session. If a security is absent from the

dissemination, firms should assume that the security is being treated as operationally halted in the IEX Trading System

at the start of the Pre-Market Session.

After the pre-market spin, IEX will use the Operational Halt Status Message to relay changes in operational halt status

for an individual security.

```
Field Name Offset Length Type Description/Notes
```
```
Message Type 0 1 Byte ‘O’ (0x4f) – Operational Halt Status
```
```
Operational Halt Status 1 1 Byte
```
```
Operational halt status identifier
```
- ‘O’ (0x4f): IEX specific operational trading
    halt
- ‘N’ (0x4e): Not operationally halted on IEX

```
Timestamp 2 8 Timestamp Time stamp of the operational halt status
```
```
Symbol 10 8 String
```
```
Security identifier represented in Nasdaq
Integrated symbology
```
Total Message Data length is 18 bytes. See Appendix B for the bitwise representation.

Example

Message Type 4f // O = Operational Halt Status

Operational Halt Status 4f // O = Operationally halted on IEX

Timestamp ac 63 c0 20 96 86 6d 14 // 2016-08-23 15:30:32.

Symbol 5a 49 45 58 54 20 20 20 // ZIEXT


### Short Sale Price Test Status Message – P (0x50)

In association with Rule 201 of Regulation SHO, the Short Sale Price Test Message is used to indicate when a short sale

price test restriction is in effect for a security.

IEX disseminates a full pre-market spin of Short Sale Price Test Status Messages indicating the Rule 201 status of all

securities. After the pre-market spin, IEX will use the Short Sale Price Test Status Message in the event of an intraday

status change.

The IEX Trading System will process orders based on the latest short sale price test restriction status.

```
Field Name Offset Length Type Description/Notes
```
```
Message Type 0 1 Byte ‘P’ (0x50) – Short Sale Price Test Status
```
```
Short Sale Price Test Status 1 1 Byte
```
```
Reg. SHO short sale price test restriction status
```
- 0 (0x0): Short Sale Price Test Not in Effect
- 1 (0x1): Short Sale Price Test in Effect

```
Timestamp 2 8 Timestamp Time stamp of the short sale price test status
```
```
Symbol 10 8 String
```
```
Security identifier represented in Nasdaq
Integrated symbology
```
```
Detail 18 1 Byte
```
```
Detail of the Reg. SHO short sale price test
restriction status
```
```
IEX populates the Detail field for IEX-listed
securities; this field will be set to “N” (Detail Not
Available) for non-IEX-listed securities.
```
- [space] (0x20): No price test in place
- ‘A’ (0x41): Short sale price test restriction in
    effect due to an intraday price drop in the
    security (i.e., Activated)
- ‘C’ (0x43): Short sale price test restriction
    remains in effect from prior day (i.e.,
    Continued)
- ‘D’ (0x44): Short sale price test restriction
    deactivated (i.e., Deactivated)
- ‘N’ (0x4e): Detail Not Available

Total Message Data length is 19 bytes. See Appendix B for the bitwise representation.

Example

Message Type 50 // P = Short Sale Price Test Status

Short Sale Price Test Status 01 // Short Sale Price Test in Effect

Timestamp ac 63 c0 20 96 86 6d 14 // 2016-08-23 15:30:32.

Symbol 5a 49 45 58 54 20 20 20 // ZIEXT

Detail 41 // A = Short Sale Price Test Activated

State Diagram

See Appendix C for a state diagram illustrating the potential Short Sale Price Test Status and Detail transitions.


### Security Event Message – E (0x45) .......................................................................................................................................................

The Security Event Message is used to indicate events that apply to a security. A Security Event Message will be sent

whenever such event occurs for a security.

```
Field Name Offset Length Type Description/Notes
```
```
Message Type 0 1 Byte ‘E’ (0x45) – Security Event
```
```
Security Event 1 1 Byte
```
```
Security event identifier
```
- ‘O’ (0x4f): _Opening Process Complete_ – This
    message indicates that the Opening Process
    is complete in this security and any orders
    queued during the Pre-Market Session are
    now available for execution on the IEX Order
    Book for the subject security.
- ‘C’ (0x43): _Closing Process Complete_ – For
    non-IEX-listed securities, this message
    indicates that IEX has completed canceling
    orders from the IEX Order Book for the
    subject security that are not eligible for the
    Post-Market Session. For IEX-listed
    securities, this message indicates that the
    closing process (e.g., Closing Auction) has
    completed for this security and IEX has
    completed canceling orders from the IEX
    Order Book for the subject security that are
    not eligible for the Post-Market Session.

```
Timestamp 2 8 Timestamp Time stamp of the security event
```
```
Symbol 10 8 String
```
```
Security identifier represented in Nasdaq
Integrated symbology
```
Total Message Data length is 18 bytes. See Appendix B for the bitwise representation.

Example

Message Type 45 // E = Security Event

Security Event 4f // O = Opening Process Complete

Timestamp 00 f0 30 2a 5b 25 b6 14 // 2017-04-17 09:30:00.

Symbol 5a 49 45 58 54 20 20 20 // ZIEXT


## TRADING MESSAGE FORMATS.............................................................................................................................................

### Add Order Message – a (0x61)...............................................................................................................................................................

A displayed order that has been added to the IEX Book.

The Order ID of this message is used as the identifier to calculate the order’s state in subsequent messages.

```
Field Name Offset Length Type Description/Notes
```
```
Message Type 0 1 Byte ‘a ’ (0x61) – Add Order
```
```
Side 1 1 Byte
```
```
Side of order:
```
- ‘8’ (0x38) – Buy
- ‘5’ (0x35) – Sell

```
Timestamp 2 8 Timestamp Time stamp of the new order
```
```
Symbol 10 8 String
```
```
Security identifier represented in Nasdaq
Integrated symbology
```
```
Order ID 18 8 Long Order ID of new order
```
```
Size 26 4 Integer Quoted size
```
```
Price 30 8 Price Booking price on the IEX Order Book
```
Total Message Data length is 38 bytes. See Appendix B for the bitwise representation.

Example

Message Type 61 // a = Add Order

Side 38 // Buy Order

Timestamp b2 8f a5 a0 ab 86 6d 14 // 2016-08-23 15:32:04.

Symbol 5a 49 45 58 54 20 20 20 // ZIEXT

Order ID 96 8f 06 00 00 00 00 00 // 429974

Size 64 00 00 00 // 100 shares

### Price 24 1d 0f 00 00 00 00 00 // $99.


### Order Modify Message – M (0x4D)

A displayed order that had its Price, Size, or Priority component changed as a result of user or system action.

The Order ID will reference the Order ID in the Add Order Message.

```
Field Name Offset Length Type Description/Notes
```
```
Message Type 0 1 Byte ‘M ’ (0x4D) – Order Modify
```
```
Modify Flags 1 1 Byte
```
```
Bit 0 – Priority
```
- 0 = Reset Priority
- 1 = Maintain Priority

```
Bits 1 – 7 Reserved
```
```
Timestamp 2 8 Timestamp Time stamp of the modified order
```
```
Symbol 10 8 String
```
```
Security identifier represented in Nasdaq
Integrated symbology
```
```
Order ID Reference 18 8 Long Order ID of the referenced order
```
```
Size 26 4 Integer New total quoted size
```
```
Price 30 8 Price Booking price on the IEX Order Book
```
Total Message Data length is 38 bytes. See Appendix B for the bitwise representation.

Example

Message Type 4D // M = Order Modify

Modify Flags 00 // Reset priority

Timestamp b2 8f a5 a0 ab 86 6d 14 // 2016-08-23 15:32:04.

Symbol 5a 49 45 58 54 20 20 20 // ZIEXT

Order ID Reference 96 8f 06 00 00 00 00 00 // 429974

Size 64 00 00 00 // 100 shares

### Price 24 1d 0f 00 00 00 00 00 // $99.


### Order Delete Message – R (0x52)

A displayed order that was removed from the IEX Book. This is caused by a member request or due to an internal
system action.

The Order ID will no longer be used in future messages to track state, unless a new Add Order Message contains the
same Order ID.

```
Field Name Offset Length Type Description/Notes
```
```
Message Type 0 1 Byte ‘R ’ (0x52) – Order Delete
```
```
Reserved 1 1 Byte Reserved for future use
```
```
Timestamp 2 8 Timestamp Time stamp of the deleted order
```
```
Symbol 10 8 String
```
```
Security identifier represented in Nasdaq
Integrated symbology
```
```
Order ID Reference 18 8 Long Order ID of the referenced order
```
Total Message Data length is 26 bytes. See Appendix B for the bitwise representation.

Example

Message Type 52 // R = Order Delete

Reserved 00 // Reserved for future use

Timestamp b2 8f a5 a0 ab 86 6d 14 // 2016-08-23 15:32:04.

Symbol 5a 49 45 58 54 20 20 20 // ZIEXT

Order ID Reference 96 8f 06 00 00 00 00 00 // 429974


### Order Executed Message – L (0x4C)

A displayed order that was executed against.

If the quantity executed reduces the remaining quantity of the order to 0, the order should be removed from the book.
Otherwise, the remaining order quantity after the execution remains on the order book with the same time-priority.

The executed price given by this message may differ from the original displayed price of the order, due to system price
improvement or price sliding.

```
Field Name Offset Length Type Description/Notes
```
```
Message Type 0 1 Byte ‘L ’ (0x4C) – Order Executed
```
```
Sale Condition Flags 1 1 Byte See Appendix A for flag values
```
```
Timestamp 2 8 Timestamp Time stamp of the trade
```
```
Symbol 10 8 String
```
```
Security identifier represented in Nasdaq
Integrated symbology
```
```
Order ID Reference 18 8 Long Order ID of the referenced order
```
```
Size 26 4 Integer Trade volume
```
```
Price 30 8 Price Trade price
```
```
Trade ID 38 8 Long IEX Generated Identifier
```
Total Message Data length is 46 bytes. See Appendix B for the bitwise representation.

Example

Message Type 4C // L = Order Executed

Sale Condition Flags 00 // Non-ISO, Regular Market session, Round or
Mixed Lot, Trade is subject to Rule 611,
execution during continuous trading

Timestamp b2 8f a5 a0 ab 86 6d 14 // 2016-08-23 15:32:04.

Symbol 5a 49 45 58 54 20 20 20 // ZIEXT

Order ID Reference 96 8f 06 00 00 00 00 00 // 429974

Size 64 00 00 00 // 100 shares

### Price 24 1d 0f 00 00 00 00 00 // $99.

Trade ID 96 8f 02 00 00 00 00 00 // 167830


### Trade Message – T (0x54)......................................................................................................................................................................

A non-displayed order on the book that executed against another non-displayed order on the book.

This message does not modify the quantity of a displayed order on the book but does impact the cumulative executed
volume on IEX. For users interested in only knowing book state, this message can be ignored.

```
Field Name Offset Length Type Description/Notes
```
```
Message Type 0 1 Byte ‘T ’ (0x 54 ) – Trade
```
```
Sale Condition Flags 1 1 Byte See Appendix A for flag values
```
```
Timestamp 2 8 Timestamp Time stamp of the trade
```
```
Symbol 10 8 String
```
```
Security identifier represented in Nasdaq
Integrated symbology
```
```
Size 18 4 Integer Trade volume
```
```
Price 22 8 Price Trade price
```
```
Trade ID 30 8 Long IEX Generated Identifier
```
Total Message Data length is 38 bytes. See Appendix B for the bitwise representation.

Example

Message Type 54 // T = Trade

Sale Condition Flags 00 // Non-ISO, Regular Market session, Round or
Mixed Lot, Trade is subject to Rule 611,
execution during continuous trading

Timestamp b2 8f a5 a0 ab 86 6d 14 // 2016-08-23 15:32:04.

Symbol 5a 49 45 58 54 20 20 20 // ZIEXT

Size 64 00 00 00 // 100 shares

Price 24 1d 0f 00 00 00 00 00 // $99.

Trade ID 96 8f 02 00 00 00 00 00 // 167830


### Trade Break Message – B (0x42) ...........................................................................................................................................................

Trade Break Messages are sent when an execution on IEX is broken on that same trading day. Trade breaks are rare and

only affect applications that rely upon IEX execution based data.

```
Field Name Offset Length Type Description/Notes
```
```
Message Type 0 1 Byte ‘B’ (0x42) – Trade Break
```
```
Sale Condition Flags 1 1 Byte See Appendix A for flag values
```
```
Timestamp 2 8 Timestamp Time stamp of the trade break
```
```
Symbol 10 8 String
```
```
Security identifier represented in Nasdaq
Integrated symbology
```
```
Size 18 4 Integer Trade break volume
```
```
Price 22 8 Price Trade break price
```
```
Trade ID 30 8 Long
```
```
IEX trade identifier of the trade that was broken.
Trade ID refers to the previously sent Order
Executed or Trade Message.
```
Total Message Data length is 38 bytes. See Appendix B for the bitwise representation.

Example

Message Type 42 // B = Trade Break

Sale Condition Flags 00 // Non-ISO, Regular Market Session, Round or
Mixed Lot, Trade is subject to Rule 611,
execution during continuous trading

Timestamp b2 8f a5 a0 ab 86 6d 14 // 2016-08-23 15:32:04.912754610

Symbol 5a 49 45 58 54 20 20 20 // ZIEXT

Size 64 00 00 00 // 100 shares

Price 24 1d 0f 00 00 00 00 00 // $99.05

Trade ID 96 8f 06 00 00 00 00 00 // 429974


### Clear Book Message – C (0x43)

This message is used to indicate that the IEX Book for a symbol has been cleared of all orders.

```
Field Name Offset Length Type Description/Notes
```
```
Message Type 0 1 Byte ‘C ’ (0x 43 ) – Clear Book
```
```
Reserved 1 1 Byte Reserved for future use
```
```
Timestamp 2 8 Timestamp Time stamp of the clear book state
```
```
Symbol 10 8 String
```
```
Security identifier represented in Nasdaq
Integrated symbology
```
Total Message Data length is 18 bytes. See Appendix B for the bitwise representation.

Example

Message Type 43 // C = Clear Book

Reserved 00 // Reserved for future use

Timestamp b2 8f a5 a0 ab 86 6d 14 // 2016-08-23 15:32:04.912754610

Symbol 5a 49 45 58 54 20 20 20 // ZIEXT


## APPENDIX A: FLAGS

### Security Directory: Flags

Definition

```
Bit Name Description
```
```
7 T: Test Security Flag
```
```
0: Symbol is not a test security
1: Symbol is a test security
```
```
6 W: When Issued Flag
```
```
0: Symbol is not a when issued security
1: Symbol is a when issued security
```
```
5 E: ETP Flag
```
```
0: Symbol is not an ETP (i.e., Exchange Traded Product)
1: Symbol is an ETP
```
Usage

```
T W E Mask Meaning
```
```
X Flags & 0x80 Test security
```
```
X^ Flags & 0x40 When issued security
```
```
X Flags & 0x20 ETP
```
### Order Executed, Trade, & Trade Break: Sale Condition Flags

Definition

```
Bit Name Description
```
```
7 F: Intermarket Sweep Flag
```
```
0: Non-Intermarket Sweep Order
1: Intermarket Sweep Order ("ISO")
```
```
6 T: Extended Hours Flag
```
```
0: Regular Market Session Trade
1: Extended Hours Trade (i.e., Form T sale condition)
```
```
5 I: Odd Lot Flag
```
```
0: Round or Mixed Lot Trade
1: Odd Lot Trade
```
```
4 8: Trade Through Exempt Flag
```
```
0: Trade is subject to Rule 611 (Trade Through) of SEC Reg. NMS
1: Trade is not subject to Rule 611 (Trade Through) of SEC Reg. NMS*
```
```
3 X: Single-price Cross Trade Flag
```
```
0: Execution during continuous trading
1: Trade resulting from a single-price cross
```
* Applied when the taking order was an ISO that traded through a protected quotation, OR the NBBO was crossed at the time of the

trade, OR the trade occurred through a self-helped venue's quotation, OR the trade was a single-price cross.


Usage

```
F T I 8 X Mask Meaning
```
```
X Flags & 0x80 Trade resulted from an ISO
```
```
X Flags & 0x40 Trade occurred before or after the Regular Market Session (i.e., Form T)
```
```
X Flags & 0x20 Trade is less than one round lot
```
```
X Flags & 0x10 Trade is not subject to Trade Through Rule 611 of SEC Reg. NMS*
```
```
X Flags & 0x08 Trade resulted from a single-price cross
```
* Applied when the taking order was an ISO that traded through a protected quotation, OR the NBBO was crossed at the time of the

trade, OR the trade occurred through a self-helped venue's quotation, OR the trade was a single-price cross.

Trade Eligibility Guidelines

- Last Sale Eligible
    o Intermarket Sweep Flag: 0 or 1
    o Extended Hours Flag: 0
    o Odd Lot Flag: 0
    o Trade Through Exempt Flag: 0 or 1
    o Single-price Cross Trade Flag: 0 or 1
- High/Low Price Eligible
    o Intermarket Sweep Flag: 0 or 1
    o Extended Hours Flag: 0
    o Odd Lot Flag: 0
    o Trade Through Exempt Flag: 0 or 1
    o Single-price Cross Trade Flag: 0 or 1
- Volume Eligible
    o Intermarket Sweep Flag: 0 or 1
    o Extended Hours Flag: 0 or 1
    o Odd Lot Flag: 0 or 1
    o Trade Through Exempt Flag: 0 or 1
    o Single-price Cross Trade Flag: 0 or 1


## APPENDIX B: BITWISE REPRESENTATION

### System Event Message in a Single Segment

#### 0 1 2 3

#### 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1

#### +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--------------

| Transport Header | B 0-3
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 4-7
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 8-11
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 12-15
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 16-19
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 20-23
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 24-27
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 28-31
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 32-35
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 36-39
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Message Length | Message Type | System Event | B 40-43
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Timestamp | B 44-47
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Timestamp | B 48-51
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


### Security Directory Message in a Single Segment

#### 0 1 2 3

#### 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1

#### +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--------------

| Transport Header | B 0-3
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 4-7
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 8-11
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 12-15
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 16-19
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 20-23
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 24-27
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 28-31
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 32-35
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 36-39
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Message Length | Message Type |T|W|E| (Flags) | B 40-43
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Timestamp | B 44-47
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Timestamp | B 48-51
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Symbol | B 52-55
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Symbol | B 56-59
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Round Lot Size | B 60-63
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Adjusted POC Price | B 64-67
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Adjusted POC Price | B 68-71
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| LULD Tier | | B 72-75
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--------------


### Trading Status Message in a Single Segment

#### 0 1 2 3

#### 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1

#### +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--------------

| Transport Header | B 0-3
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 4-7
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 8-11
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 12-15
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 16-19
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 20-23
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 24-27
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 28-31
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 32-35
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 36-39
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Message Length | Message Type |Trading Status | B 40-43
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Timestamp | B 44-47
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Timestamp | B 48-51
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Symbol | B 52-55
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Symbol | B 56-59
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Reason | B 60-63
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--------------


### Operational Halt Status Message in a Single Segment

#### 0 1 2 3

#### 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1

#### +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--------------

| Transport Header | B 0-3
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 4-7
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 8-11
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 12-15
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 16-19
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 20-23
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 24-27
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 28-31
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 32-35
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 36-39
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Message Length | Message Type |Op. Halt Status| B 40-43
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Timestamp | B 44-47
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Timestamp | B 48-51
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Symbol | B 52-55
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Symbol | B 56-59
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--------------


### Retail Liquidity Indicator (“RLI”) Message in a Single Segment

#### 0 1 2 3

#### 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1

#### +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--------------

| Transport Header | B 0-3
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 4-7
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 8-11
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 12-15
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 16-19
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 20-23
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 24-27
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 28-31
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 32-35
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 36-39
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Message Length | Message Type | RLI | B 40-43
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Timestamp | B 44-47
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Timestamp | B 48-51
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Symbol | B 52-55
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Symbol | B 56-59
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--------------


### Short Sale Price Test Status Message in a Single Segment

#### 0 1 2 3

#### 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1

#### +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--------------

| Transport Header | B 0-3
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 4-7
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 8-11
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 12-15
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 16-19
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 20-23
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 24-27
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 28-31
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 32-35
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 36-39
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Message Length | Message Type |Px. Test Status| B 40-43
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Timestamp | B 44-47
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Timestamp | B 48-51
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Symbol | B 52-55
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Symbol | B 56-59
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Detail | | B 60-63
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--------------


### Security Event Message in a Single Segment

#### 0 1 2 3

#### 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1

#### +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--------------

| Transport Header | B 0-3
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 4-7
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 8-11
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 12-15
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 16-19
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 20-23
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 24-27
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 28-31
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 32-35
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 36-39
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Message Length | Message Type |Security Event | B 40-43
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Timestamp | B 44-47
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Timestamp | B 48-51
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Symbol | B 52-55
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Symbol | B 56-59
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--------------


### Add Order Message in a Single Segment

#### 0 1 2 3

#### 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1

#### +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--------------

| Transport Header | B 0-3
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 4-7
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 8-11
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 12-15
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 16-19
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 20-23
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 24-27
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 28-31
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 32-35
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 36-39
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Message Length | Message Type | Side | B 40-43
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Timestamp | B 44-47
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Timestamp | B 48-51
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Symbol | B 52-55
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Symbol | B 56-59
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Order ID | B 60-63
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Order ID | B 64-67
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Size | B 68-71
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Price | B 72-75
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Price | B 76-79
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--------------


### Order Modify Message in a Single Segment

#### 0 1 2 3

#### 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1

#### +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--------------

| Transport Header | B 0-3
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 4-7
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 8-11
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 12-15
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 16-19
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 20-23
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 24-27
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 28-31
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 32-35
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 36-39
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Message Length | Message Type | Modify Flags | B 40-43
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Timestamp | B 44-47
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Timestamp | B 48-51
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Symbol | B 52-55
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Symbol | B 56-59
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Order ID Reference | B 60-63
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Order ID Reference | B 64-67
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Size | B 68-71
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Price | B 72-75
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Price | B 76-79
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--------------


### Order Delete Message in a Single Segment

#### 0 1 2 3

#### 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1

#### +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--------------

| Transport Header | B 0-3
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 4-7
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 8-11
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 12-15
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 16-19
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 20-23
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 24-27
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 28-31
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 32-35
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 36-39
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Message Length | Message Type | Reserved | B 40-43
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Timestamp | B 44-47
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Timestamp | B 48-51
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Symbol | B 52-55
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Symbol | B 56-59
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Order ID Reference | B 60-63
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Order ID Reference | B 64-67
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--------------


### Order Executed Message in a Single Segment

#### 0 1 2 3

#### 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1

#### +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--------------

| Transport Header | B 0-3
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 4-7
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 8-11
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 12-15
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 16-19
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 20-23
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 24-27
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 28-31
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 32-35
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 36-39
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Message Length | Message Type |F|T|I|8|X| | B 40-43
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Timestamp | B 44-47
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Timestamp | B 48-51
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Symbol | B 52-55
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Symbol | B 56-59
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Order ID Reference | B 60-63
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Order ID Reference | B 64-67
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Size | B 68-71
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Price | B 72-75
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Price | B 76-79
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Trade ID | B 80-83
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Trade ID | B 84-87
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--------------


### Trade Message in a Single Segment

#### 0 1 2 3

#### 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1

#### +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--------------

| Transport Header | B 0-3
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 4-7
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 8-11
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 12-15
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 16-19
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 20-23
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 24-27
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 28-31
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 32-35
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 36-39
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Message Length | Message Type |F|T|I|8|X| | B 40-43
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Timestamp | B 44-47
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Timestamp | B 48-51
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Symbol | B 52-55
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Symbol | B 56-59
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Size | B 60-63
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Price | B 64-67
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Price | B 68-71
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Trade ID | B 72-75
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Trade ID | B 76-79
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--------------


### Trade Break Message in a Single Segment

#### 0 1 2 3

#### 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1

#### +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--------------

| Transport Header | B 0-3
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 4-7
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 8-11
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 12-15
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 16-19
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 20-23
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 24-27
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 28-31
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 32-35
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 36-39
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Message Length | Message Type |F|T|I|8|X| | B 40-43
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Timestamp | B 44-47
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Timestamp | B 48-51
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Symbol | B 52-55
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Symbol | B 56-59
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Size | B 60-63
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Price | B 64-67
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Price | B 68-71
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Trade ID | B 72-75
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Trade ID | B 76-79
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--------------


### Clear Book Message in a Single Segment

#### 0 1 2 3

#### 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1

#### +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--------------

| Transport Header | B 0-3
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 4-7
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 8-11
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 12-15
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 16-19
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 20-23
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 24-27
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 28-31
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 32-35
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Transport Header | B 36-39
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Message Length | Message Type | Reserved | B 40-43
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Timestamp | B 44-47
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Timestamp | B 48-51
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Symbol | B 52-55
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Symbol | B 56-59
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--------------


## APPENDIX C: STATE DIAGRAMS

### Trading Status Messages

Continues on next page.



### Short Sale Price Test Status Messages


## REVISION HISTORY

```
Version Date Change
```
```
1.00 September 3, 2024 Initial document
```
```
1.01 September 30 , 2024 Updated message type byte value for “Add Order” message
```
```
1.02 January 14, 202 5
```
- Clarified description for “Size” field in “Modify Order” message.
- Updated overview to reflect feed launch.


