import shutil
import pytest

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