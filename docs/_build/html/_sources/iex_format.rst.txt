IEX-PCAP file format
====================

Every PCAP file begins with a global PCAP header. 
For IEX, the magic number is ``d4 c3 b2 a1`` and the link type is ethernet ``01 00 00 00`` (see `PCAP FILE SPECIFICATIONS`_).

Following the global header, each PCAP packet has a packet header.

- **PCAP Packet Header**:
  - **Timestamp Seconds** (4 bytes): Seconds from the UNIX epoch.\
  - **Timestamp Microseconds** (4 bytes): Additional microseconds.\
  - **Captured Length** (4 bytes): Packet length captured.\
  - **Original Length** (4 bytes): Packet length sent, usually the same as Captured length.\

The packet payload structure is as follows:

- Starts with an **Ethernet frame** (14 bytes), followed by an **IPv4 frame** (20 bytes), and ends with a **UDP frame** (8 bytes).
- The payload then includes an **IEX packet header** (40 bytes) followed by the **message length** (2 bytes), and ends with the actual **IEX message**.

Below we summarize the above in a diagram.

**Global PCAP header (24 bytes)**

**PCAP packet header (16 bytes)**

**Packet payload**

- Ethernet frame (14 bytes)
- IPv4 frame (20 bytes)
- UDP frame (8 bytes)
- IEX packet
  - IEX Header (40 bytes)
  - IEX message 1 len (2 bytes)
  - IEX message 1
  - IEX message 2 len (2 bytes)
  - IEX message 2

Example PCAP file
-------------------------------------------------------------

For this example we will read the first 500 bytes from IEX DEEP File for 14 Sep 2023.
1. **Global PCAP Header (24 bytes)**:
   - ``d4 c3 b2 a1 | 02 00 | 04 00 | 00 00 00 00 | 00 00 00 00``
   - ``ff ff 00 00 | 01 00 00 00``

2. **PCAP Packet Header**:
   - ``8d ed 02 65 | 70 e5 03 00``
   - ``52 00 00 00 | 52 00 00 00``
     - Indicates packet length is 82 bytes (52 in Hex).

3. **PCAP Packet payload**:

    - **Ethernet Frame**:
      - ``01 00 5e 57 15 04 b8 59``
      - ``9f f9 2d 53 08 00``

    - **IPv4 Frame**:
      - ``45 00 00 44 00 00 00 00 40 11``
      - ``c8 67 17 e2 9b 84 e9 d7 15 04``

    - **UDP Frame**:
      - ``28 8a 28 8a 00 30 d4 ee``

    - **IEX Packet**:

      - **IEX Header (40 bytes)**:
        - ``01 00 04 80 01 00 00 00 00 00 9e 4c 00 00``
        - ``00 00 00 00 00 00 00 00 00 00 01 00 00 00 00 00``
        - ``00 00 54 e0 71 c4 36 c0 84 17``
      - **No IEX Message** (Length is 0 for this packet).

7. **Second PCAP Packet**:
   - ``8e ed 02 65 1f 08 04 00 52 00 00 00 52 00 00 00``
   - ... (Details similar to above, with no IEX message).

8. **Third PCAP Packet**:
   - (Details similar to above, IEX message is non trivial so we skip to that part).
   - **IEX Header (40 bytes)**:
      - ``01 00 04 80 01 00 00 00 00 00 9e 4c 85 05 43 00 00 00 00 00 00 00``
      - ``00 00 01 00 00 00 00 00 00 00 ae 85 ec 09 37 c0 84 17``
      - Number of messages (2 bytes) is at offset 14 (see `IEX TP SPECIFICATIONS`_).
   - **IEX Message len (2 bytes)**:
      - ``0a 00`` - So message is only 10 bytes
  
   - **IEX message 1**:
      - ``53 4f 1e 46 ec 09 37 c0 84 17``
      - This is the system event message (see `IEX DEEP SPECIFICATIONS`_).
   and so on.


.. _PCAP FILE SPECIFICATIONS: https://datatracker.ietf.org/doc/html/draft-ietf-opsawg-pcap
.. _IEX TP SPECIFICATIONS: https://assets-global.website-files.com/635ad1b3d188c10deb1ebcba/63bd4d3604199d7af121cfd3_IEX_Transport_Specification.pdf
.. _IEX DEEP SPECIFICATIONS: https://assets-global.website-files.com/635ad1b3d188c10deb1ebcba/63bd4a1cb0d2bef3cbf36bcc_IEX%20DEEP%20Specification%20v1.08.pdf
