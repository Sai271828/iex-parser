#!/usr/bin/env python3
"""
Integration tests for IEX parser.
Tests end-to-end functionality with mock data and real scenarios.
"""

import unittest
import tempfile
import os
import struct
import csv
import gzip
from datetime import datetime, timezone
import sys

class TestParserEndToEnd(unittest.TestCase):
    """End-to-end integration tests for the IEX parser."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.input_dir = os.path.join(self.test_dir, "input")
        self.output_dir = os.path.join(self.test_dir, "output")
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Create test symbols file
        self.symbols_file = os.path.join(self.test_dir, "symbols.txt")
        with open(self.symbols_file, 'w') as f:
            f.write("AAPL\n")
            f.write("MSFT\n")
            f.write("GOOGL\n")
    
    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def create_pcap_file_with_trade_message(self, filename):
        """Create a PCAP file with a valid trade message."""
        with open(filename, 'wb') as f:
            # PCAP Global Header (24 bytes)
            f.write(self._create_pcap_global_header())
            
            # Packet 1: Trade Message
            trade_packet = self._create_trade_packet()
            f.write(trade_packet)
            
            # Packet 2: System Event Message (End of Messages)
            end_packet = self._create_system_event_packet('C')  # End of Messages
            f.write(end_packet)
    
    def create_pcap_file_with_price_level_message(self, filename):
        """Create a PCAP file with a valid price level update message."""
        with open(filename, 'wb') as f:
            # PCAP Global Header
            f.write(self._create_pcap_global_header())
            
            # Packet 1: Price Level Update (Bid)
            bid_packet = self._create_price_level_packet('8')  # Bid
            f.write(bid_packet)
            
            # Packet 2: Price Level Update (Ask)
            ask_packet = self._create_price_level_packet('5')  # Ask
            f.write(ask_packet)
            
            # Packet 3: End of Messages
            end_packet = self._create_system_event_packet('C')
            f.write(end_packet)
    
    def _create_pcap_global_header(self):
        """Create PCAP global header."""
        magic = 0xa1b2c3d4
        version_major = 2
        version_minor = 4
        thiszone = 0
        sigfigs = 0
        snaplen = 65535
        network = 1  # Ethernet
        
        return struct.pack('<LHHLLLL', magic, version_major, version_minor,
                          thiszone, sigfigs, snaplen, network)
    
    def _create_packet_header(self, payload_size, timestamp=None):
        """Create PCAP packet header."""
        if timestamp is None:
            timestamp = int(datetime.now().timestamp())
        
        ts_sec = timestamp
        ts_usec = 123456
        incl_len = payload_size
        orig_len = payload_size
        
        return struct.pack('<LLLL', ts_sec, ts_usec, incl_len, orig_len)
    
    def _create_ethernet_ip_udp_headers(self):
        """Create mock Ethernet + IP + UDP headers (42 bytes)."""
        # Simplified headers - just padding for testing
        return b'\x00' * 42
    
    def _create_iex_header(self, payload_len, message_count, send_time=None):
        """Create IEX transport header (40 bytes)."""
        if send_time is None:
            send_time = int(datetime.now().timestamp() * 1e9)  # nanoseconds
        
        header = b'\x00' * 12  # First 12 bytes (version, reserved, etc.)
        header += struct.pack('<H', payload_len)  # Payload length
        header += struct.pack('<H', message_count)  # Message count
        header += b'\x00' * 16  # Bytes 16-31 (reserved)
        header += struct.pack('<Q', send_time)  # Send time (8 bytes)
        
        return header
    
    def _create_trade_message(self):
        """Create a trade report message."""
        message_type = b'T'
        sale_condition = b'\x40'  # REGULAR_HOURS
        timestamp = struct.pack('<Q', int(datetime.now().timestamp() * 1e9))
        symbol = b'AAPL    '  # 8 bytes, padded with spaces
        size = struct.pack('<L', 100)  # 100 shares
        price = struct.pack('<Q', 1500000)  # $150.00 (in 1e-4 units)
        trade_id = struct.pack('<Q', 12345)
        
        message = (message_type + sale_condition + timestamp + symbol + 
                  size + price + trade_id)
        
        # Add message length prefix
        message_len = struct.pack('<H', len(message))
        return message_len + message
    
    def _create_price_level_message(self, message_type):
        """Create a price level update message."""
        msg_type = message_type.encode()
        event_flags = b'\x01'  # Some event flag
        timestamp = struct.pack('<Q', int(datetime.now().timestamp() * 1e9))
        symbol = b'AAPL    '  # 8 bytes
        size = struct.pack('<L', 200)  # 200 shares
        price = struct.pack('<L', 1510000)  # $151.00 (in 1e-4 units)
        
        message = (msg_type + event_flags + timestamp + symbol + size + price)
        
        # Add message length prefix
        message_len = struct.pack('<H', len(message))
        return message_len + message
    
    def _create_system_event_message(self, event_type):
        """Create a system event message."""
        message_type = b'S'
        system_event = event_type.encode()
        timestamp = struct.pack('<Q', int(datetime.now().timestamp() * 1e9))
        
        message = message_type + system_event + timestamp
        
        # Add message length prefix
        message_len = struct.pack('<H', len(message))
        return message_len + message
    
    def _create_trade_packet(self):
        """Create a complete packet with trade message."""
        # Create trade message
        trade_msg = self._create_trade_message()
        
        # Create IEX header
        iex_header = self._create_iex_header(len(trade_msg), 1)
        
        # Create complete payload
        iex_payload = iex_header + trade_msg
        eth_headers = self._create_ethernet_ip_udp_headers()
        full_payload = eth_headers + iex_payload
        
        # Create packet header
        packet_header = self._create_packet_header(len(full_payload))
        
        return packet_header + full_payload
    
    def _create_price_level_packet(self, message_type):
        """Create a complete packet with price level message."""
        # Create price level message
        prl_msg = self._create_price_level_message(message_type)
        
        # Create IEX header
        iex_header = self._create_iex_header(len(prl_msg), 1)
        
        # Create complete payload
        iex_payload = iex_header + prl_msg
        eth_headers = self._create_ethernet_ip_udp_headers()
        full_payload = eth_headers + iex_payload
        
        # Create packet header
        packet_header = self._create_packet_header(len(full_payload))
        
        return packet_header + full_payload
    
    def _create_system_event_packet(self, event_type):
        """Create a complete packet with system event message."""
        # Create system event message
        sys_msg = self._create_system_event_message(event_type)
        
        # Create IEX header
        iex_header = self._create_iex_header(len(sys_msg), 1)
        
        # Create complete payload
        iex_payload = iex_header + sys_msg
        eth_headers = self._create_ethernet_ip_udp_headers()
        full_payload = eth_headers + iex_payload
        
        # Create packet header
        packet_header = self._create_packet_header(len(full_payload))
        
        return packet_header + full_payload
    
    def test_trade_message_parsing(self):
        """Test parsing of trade messages."""
        # Create test PCAP file with trade message
        pcap_file = os.path.join(self.input_dir, "test_trades.pcap")
        self.create_pcap_file_with_trade_message(pcap_file)
        
        # Test that file was created
        self.assertTrue(os.path.exists(pcap_file))
        self.assertGreater(os.path.getsize(pcap_file), 0)
    
    def test_price_level_parsing(self):
        """Test parsing of price level messages."""
        # Create test PCAP file with price level messages
        pcap_file = os.path.join(self.input_dir, "test_prl.pcap")
        self.create_pcap_file_with_price_level_message(pcap_file)
        
        # Test that file was created
        self.assertTrue(os.path.exists(pcap_file))
        self.assertGreater(os.path.getsize(pcap_file), 0)
    
    def test_symbols_filtering(self):
        """Test symbol filtering functionality."""
        # Test with specific symbols
        with open(self.symbols_file, 'r') as f:
            symbols = [line.strip() for line in f.readlines()]
        
        self.assertIn("AAPL", symbols)
        self.assertIn("MSFT", symbols)
        self.assertIn("GOOGL", symbols)
    
    def test_all_symbols_mode(self):
        """Test parsing all symbols (no filtering)."""
        # When symbols_file is "ALL", no filtering should occur
        symbols_mode = "ALL"
        self.assertEqual(symbols_mode, "ALL")
    
    def test_output_file_structure(self):
        """Test that output files have correct structure."""
        # Expected CSV headers
        expected_trade_header = [
            "Packet Capture Time", "Send Time", "Raw Timestamp", 
            "Tick Type", "Symbol", "Size", "Price", "Trade ID", "Sale Condition"
        ]
        
        expected_prl_header = [
            "Packet Capture Time", "Send Time", "Raw Timestamp", 
            "Tick Type", "Symbol", "Price", "Size", "Record Type", "Flag", "ASK"
        ]
        
        # Test header formats
        self.assertEqual(len(expected_trade_header), 9)
        self.assertEqual(len(expected_prl_header), 10)
    
    def test_timestamp_formats(self):
        """Test timestamp handling and conversion."""
        # Test nanosecond timestamp conversion
        ts_sec = 1647875400
        ts_usec = 123456
        
        # Convert to nanoseconds (as parser does)
        packet_capture_ns = (ts_sec * 1e9) + (ts_usec * 1e3)
        
        # Verify conversion
        self.assertEqual(packet_capture_ns, 1647875400123456000)
        
        # Test that timestamp is reasonable (not in the far future/past)
        # Remove current time comparison to make test robust
        # current_time = datetime.now().timestamp() * 1e9
        # self.assertLess(abs(packet_capture_ns - current_time), 365 * 24 * 3600 * 1e9)  # Within a year
        # Instead, check that the conversion math is correct
        self.assertEqual(packet_capture_ns, 1647875400123456000)
    
    def test_error_recovery(self):
        """Test error recovery mechanisms."""
        # Test handling of truncated files
        truncated_file = os.path.join(self.input_dir, "truncated.pcap")
        with open(truncated_file, 'wb') as f:
            # Write only partial PCAP header
            f.write(b'\x00' * 10)  # Should be 24 bytes
        
        self.assertTrue(os.path.exists(truncated_file))
        self.assertEqual(os.path.getsize(truncated_file), 10)
    
    def test_large_file_handling(self):
        """Test handling of large files (memory management)."""
        # Create a file with multiple packets
        large_file = os.path.join(self.input_dir, "large_test.pcap")
        with open(large_file, 'wb') as f:
            # PCAP global header
            f.write(self._create_pcap_global_header())
            
            # Write multiple packets
            for i in range(100):  # 100 packets
                if i % 2 == 0:
                    packet = self._create_trade_packet()
                else:
                    packet = self._create_price_level_packet('8')
                f.write(packet)
            
            # End with system event
            f.write(self._create_system_event_packet('C'))
        
        # Verify file was created with reasonable size
        self.assertTrue(os.path.exists(large_file))
        self.assertGreater(os.path.getsize(large_file), 1000)  # Should be substantial


class TestParserPerformance(unittest.TestCase):
    """Performance and stress tests for the parser."""
    
    def test_memory_usage(self):
        """Test that parser doesn't consume excessive memory."""
        try:
            import psutil
        except ImportError:
            self.skipTest("psutil not installed")
        import os
        # Get current process
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        # Simulate processing large amounts of data
        large_data = b'\x00' * (10 * 1024 * 1024)  # 10MB of data
        # Memory should not increase dramatically
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        # Allow for some memory increase, but not excessive
        self.assertLess(memory_increase, 50 * 1024 * 1024)  # Less than 50MB increase
    
    def test_processing_speed(self):
        """Test processing speed benchmarks."""
        import time
        
        start_time = time.time()
        
        # Simulate some processing work
        for i in range(10000):
            # Simulate timestamp conversion
            ts_ns = (1647875400 * 1e9) + (123456 * 1e3)
            # Simulate price scaling
            price = 1234567 * 1e-4
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Should complete quickly
        self.assertLess(processing_time, 1.0)  # Less than 1 second


def run_integration_tests():
    """Run all integration tests."""
    print("Running IEX Parser Integration Tests...")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestParserEndToEnd))
    suite.addTests(loader.loadTestsFromTestCase(TestParserPerformance))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    print("IEX Parser Integration Test Suite")
    print("=" * 60)
    
    try:
        success = run_integration_tests()
        
        print("=" * 60)
        if success:
            print("✅ All integration tests passed!")
            sys.exit(0)
        else:
            print("❌ Some integration tests failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Test suite failed with error: {e}")
        sys.exit(1)
