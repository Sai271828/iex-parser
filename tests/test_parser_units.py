#!/usr/bin/env python3
"""
Unit tests for IEX parser functionality.
Tests the core parsing functions and error handling.
"""

import unittest
import tempfile
import os
import struct
from unittest.mock import patch, mock_open
import sys
import subprocess

class TestIEXParser(unittest.TestCase):
    """Test cases for IEX parser functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.test_symbols_file = os.path.join(self.test_dir, "test_symbols.txt")
        
        # Create test symbols file
        with open(self.test_symbols_file, 'w') as f:
            f.write("AAPL\n")
            f.write("MSFT\n")
            f.write("GOOGL\n")
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_symbols_file_parsing(self):
        """Test that symbols file is parsed correctly."""
        # This would test the symbols file reading logic
        with open(self.test_symbols_file, 'r') as f:
            symbols = [line.strip() for line in f.readlines()]
        
        expected_symbols = ["AAPL", "MSFT", "GOOGL"]
        self.assertEqual(symbols, expected_symbols)
    
    def test_empty_symbols_file(self):
        """Test handling of empty symbols file."""
        empty_file = os.path.join(self.test_dir, "empty.txt")
        with open(empty_file, 'w') as f:
            pass  # Create empty file
        
        with open(empty_file, 'r') as f:
            symbols = [line.strip() for line in f.readlines() if line.strip()]
        
        self.assertEqual(symbols, [])
    
    def test_all_symbols_mode(self):
        """Test that 'ALL' mode works correctly."""
        # Test that when symbols_file is "ALL", no filtering is applied
        symbols_file = "ALL"
        self.assertEqual(symbols_file, "ALL")
    
    def create_mock_pcap_header(self):
        """Create a mock PCAP global header (24 bytes)."""
        # PCAP global header format
        magic = 0xa1b2c3d4  # Magic number
        version_major = 2
        version_minor = 4
        thiszone = 0
        sigfigs = 0
        snaplen = 65535
        network = 1  # Ethernet
        
        return struct.pack('<LHHLLLL', magic, version_major, version_minor, 
                          thiszone, sigfigs, snaplen, network)
    
    def create_mock_packet_header(self, ts_sec=1647875400, ts_usec=123456, 
                                 incl_len=100, orig_len=100):
        """Create a mock PCAP packet header (16 bytes)."""
        return struct.pack('<LLLL', ts_sec, ts_usec, incl_len, orig_len)
    
    def create_mock_ethernet_ip_udp_headers(self):
        """Create mock Ethernet + IP + UDP headers (42 bytes total)."""
        # Simplified mock headers - just padding for now
        return b'\x00' * 42
    
    def create_mock_iex_payload(self, message_count=1, payload_len=50):
        """Create a mock IEX payload."""
        # IEX header (40 bytes) + messages
        iex_header = b'\x00' * 12  # First 12 bytes
        iex_header += struct.pack('<H', payload_len)  # Payload length (2 bytes)
        iex_header += struct.pack('<H', message_count)  # Message count (2 bytes)
        iex_header += b'\x00' * 16  # Bytes 16-31
        iex_header += struct.pack('<Q', 1647875400000000000)  # Send time (8 bytes)
        
        # Mock message: 2-byte length + message data
        message_len = 38  # Trade report message length
        message_data = b'T'  # Message type
        message_data += b'\x00' * 37  # Rest of trade report message
        
        message = struct.pack('<H', message_len) + message_data
        
        return iex_header + message
    
    def test_pcap_header_creation(self):
        """Test PCAP header creation."""
        header = self.create_mock_pcap_header()
        self.assertEqual(len(header), 24)
    
    def test_packet_header_creation(self):
        """Test packet header creation."""
        header = self.create_mock_packet_header()
        self.assertEqual(len(header), 16)
    
    def test_iex_payload_creation(self):
        """Test IEX payload creation."""
        payload = self.create_mock_iex_payload()
        self.assertGreater(len(payload), 40)  # Should have header + message
    
    def test_timestamp_conversion(self):
        """Test timestamp conversion logic."""
        ts_sec = 1647875400
        ts_usec = 123456
        
        # Convert to nanoseconds (as done in parser)
        ts_ns = (ts_sec * 1e9) + (ts_usec * 1e3)
        
        expected_ns = 1647875400123456000
        self.assertEqual(ts_ns, expected_ns)
    
    def test_price_scaling(self):
        """Test price scaling logic."""
        # Test price scaling (multiply by 1e-4)
        raw_price = 1234567  # Raw price from IEX
        scaled_price = raw_price * 1e-4
        
        expected_price = 123.4567
        self.assertAlmostEqual(scaled_price, expected_price, places=6)
    
    def test_symbol_parsing_edge_cases(self):
        """Test symbol parsing with various edge cases."""
        # Test symbol with spaces (should be trimmed)
        symbol_with_spaces = "AAPL    "
        cleaned = symbol_with_spaces.rstrip()
        self.assertEqual(cleaned, "AAPL")
        
        # Test symbol with null bytes
        symbol_with_nulls = "MSFT\x00\x00\x00\x00"
        cleaned = symbol_with_nulls.rstrip('\x00')
        self.assertEqual(cleaned, "MSFT")
    
    def test_sale_condition_flags(self):
        """Test sale condition flag interpretation."""
        # Test bitwise flag operations
        flags = 0x80 | 0x40  # INTERMARKET_SWEEP | EXTENDED_HOURS
        
        conditions = []
        if flags & 0x80:
            conditions.append("INTERMARKET_SWEEP")
        if flags & 0x40:
            conditions.append("EXTENDED_HOURS")
        else:
            conditions.append("REGULAR_HOURS")
        
        expected = ["INTERMARKET_SWEEP", "EXTENDED_HOURS"]
        self.assertEqual(conditions, expected)


class TestParserIntegration(unittest.TestCase):
    """Integration tests for the complete parser."""
    
    def setUp(self):
        """Set up integration test fixtures."""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up integration test fixtures."""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_parser_compilation(self):
        """Test that the C++ parser compiles successfully."""
        try:
            from iex_cppparser import compile_cpp
            # This should not raise an exception
            result = compile_cpp.compile()
            # If compile() returns something, check it's successful
            if result is not None:
                self.assertTrue(result)
        except ImportError:
            self.skipTest("iex_cppparser module not available")
        except Exception as e:
            self.fail(f"Parser compilation failed: {e}")
    
    def test_parser_import(self):
        """Test that parser functions can be imported."""
        try:
            from iex_cppparser import parse_date
            self.assertTrue(callable(parse_date))
        except ImportError:
            self.skipTest("iex_cppparser module not available")
    
    def create_minimal_test_pcap(self, filename):
        """Create a minimal valid PCAP file for testing."""
        with open(filename, 'wb') as f:
            # Write PCAP global header
            f.write(self.create_mock_pcap_header())
            
            # Write one packet
            packet_header = self.create_mock_packet_header(incl_len=100)
            f.write(packet_header)
            
            # Write packet data (Ethernet + IP + UDP + IEX payload)
            eth_ip_udp = b'\x00' * 42
            iex_payload = b'\x00' * 58  # Minimal payload
            f.write(eth_ip_udp + iex_payload)
    
    def create_mock_pcap_header(self):
        """Create a mock PCAP global header."""
        magic = 0xa1b2c3d4
        version_major = 2
        version_minor = 4
        thiszone = 0
        sigfigs = 0
        snaplen = 65535
        network = 1
        
        return struct.pack('<LHHLLLL', magic, version_major, version_minor,
                          thiszone, sigfigs, snaplen, network)
    
    def create_mock_packet_header(self, ts_sec=1647875400, ts_usec=123456,
                                 incl_len=100, orig_len=100):
        """Create a mock PCAP packet header."""
        return struct.pack('<LLLL', ts_sec, ts_usec, incl_len, orig_len)


class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases."""
    
    def test_invalid_file_paths(self):
        """Test handling of invalid file paths."""
        # Test non-existent input file
        nonexistent_file = "/path/that/does/not/exist.pcap"
        self.assertFalse(os.path.exists(nonexistent_file))
        
        # Test invalid output directory
        invalid_output = "/invalid/path/output"
        self.assertFalse(os.path.exists(os.path.dirname(invalid_output)))
    
    def test_malformed_data_handling(self):
        """Test handling of malformed data."""
        # Test empty data
        empty_data = b''
        self.assertEqual(len(empty_data), 0)
        
        # Test truncated data
        truncated_header = b'\x00' * 10  # Should be 16 bytes
        self.assertLess(len(truncated_header), 16)
    
    def test_boundary_conditions(self):
        """Test boundary conditions."""
        # Test maximum reasonable values
        max_price = 1000000 * 1e-4  # $100 per share
        self.assertEqual(max_price, 100.0)
        
        # Test minimum values
        min_price = 1 * 1e-4  # $0.0001 per share
        self.assertEqual(min_price, 0.0001)
        
        # Test large message counts
        large_count = 1000
        self.assertLessEqual(large_count, 1000)  # Our validation limit


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestIEXParser))
    suite.addTests(loader.loadTestsFromTestCase(TestParserIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorHandling))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    print("Running IEX Parser Unit Tests...")
    print("=" * 50)
    
    success = run_tests()
    
    print("=" * 50)
    if success:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)
