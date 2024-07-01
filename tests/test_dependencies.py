import shutil
import pytest
from iex_cppparser import parse_file
import os
import filecmp

dir = os.path.dirname(os.path.abspath(__file__))



def test_gunzip_installed():
    """
    Ensure that gunzip is installed on the system.
    """
    try:
        if shutil.which("gunzip") is None:
            pytest.fail("gunzip is not installed on the system.")
    except (AttributeError, TypeError):
        pytest.fail("gunzip is not installed on the system.")

def test_tcpdump_installed():
    """
    Ensure that tcpdump is installed on the system.
    """
    try:
        if shutil.which("tcpdump") is None:
            pytest.fail("tcpdump is not installed on the system.")
    except (AttributeError, TypeError):
        pytest.fail("tcpdump is not installed on the system.")

def test_parsing_selected_symbols():
    if not os.path.exists(os.path.join(dir, "parsed_folder")):
        os.mkdir(os.path.join(dir, "parsed_folder"))
    test_file = os.path.join(dir, "test.pcap.gz")
    parsed_folder = os.path.join(dir, "parsed_folder")
    symbol = os.path.join(dir, "symbols.txt")
    try:
        parse_file(test_file, parsed_folder, symbol)
    except Exception as e:
        pytest.fail(f"Failed to parse selected symbols: {e}")
    
    expected_files = ["test_trd.csv", "test_prl.csv"]

    for file in expected_files:
        expected_file = os.path.join(dir, "expected_output", file)
        parsed_file = os.path.join(parsed_folder, file)

        # Compare the parsed file with the expected file
        if not filecmp.cmp(expected_file, parsed_file):
            pytest.fail(f"Output file {file} does not match the expected file.")
    
    shutil.rmtree(parsed_folder)
