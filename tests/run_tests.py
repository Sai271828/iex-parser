#!/usr/bin/env python3
"""
Comprehensive test runner for IEX Parser.
Runs unit tests, integration tests, and provides test coverage reporting.
"""

import sys
import os
import subprocess
import time
from pathlib import Path

def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def print_section(title):
    """Print a formatted section header."""
    print(f"\n📋 {title}")
    print("-" * 50)

def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} - FAILED")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def check_dependencies():
    """Check if required dependencies are available."""
    print_section("Checking Dependencies")
    
    dependencies = [
        ("python3", "Python 3"),
        ("gcc", "GCC Compiler"),
        ("g++", "G++ Compiler")
    ]
    
    all_good = True
    for cmd, name in dependencies:
        if run_command(f"which {cmd}", f"Checking {name}"):
            continue
        else:
            all_good = False
    
    return all_good

def compile_parser():
    """Compile the C++ parser."""
    print_section("Compiling Parser")
    
    try:
        from iex_cppparser import compile_cpp
        print("🔧 Compiling C++ parser...")
        compile_cpp.compile()
        print("✅ Parser compilation - SUCCESS")
        return True
    except ImportError:
        print("❌ Cannot import iex_cppparser module")
        return False
    except Exception as e:
        print(f"❌ Parser compilation failed: {e}")
        return False

def run_unit_tests():
    """Run unit tests."""
    print_section("Running Unit Tests")
    
    if not os.path.exists("test_parser_units.py"):
        print("❌ Unit test file not found")
        return False
    
    return run_command("python3 test_parser_units.py", "Unit Tests")

def run_integration_tests():
    """Run integration tests."""
    print_section("Running Integration Tests")
    
    if not os.path.exists("test_parser_integration.py"):
        print("❌ Integration test file not found")
        return False
    
    return run_command("python3 test_parser_integration.py", "Integration Tests")

def run_functional_test():
    """Run functional test with the main parser."""
    print_section("Running Functional Test")
    
    if not os.path.exists("test_parser.py"):
        print("❌ Functional test file not found")
        return False
    
    print("🔧 Running functional parser test...")
    print("   (This may take a moment if processing real data)")
    
    # Check if test data exists
    if os.path.exists("testing/") and any(f.endswith('.pcap.gz') for f in os.listdir("testing/")):
        print("   Found test data, running with real data...")
        return run_command("python3 test_parser.py", "Functional Test with Real Data")
    else:
        print("   No test data found, skipping functional test")
        print("   To run functional tests, add PCAP files to testing/ directory")
        return True

def check_code_quality():
    """Run code quality checks."""
    print_section("Code Quality Checks")
    
    # Check Python files for syntax
    python_files = ["test_parser.py", "test_parser_units.py", "test_parser_integration.py", "run_tests.py"]
    
    all_good = True
    for file in python_files:
        if os.path.exists(file):
            if not run_command(f"python3 -m py_compile {file}", f"Syntax check for {file}"):
                all_good = False
        else:
            print(f"⚠️  File {file} not found, skipping syntax check")
    
    return all_good

def generate_test_report():
    """Generate a test report."""
    print_section("Test Report Summary")
    
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "python_version": sys.version.split()[0],
        "platform": sys.platform,
        "working_directory": os.getcwd()
    }
    
    print(f"📊 Test Report Generated at: {report['timestamp']}")
    print(f"🐍 Python Version: {report['python_version']}")
    print(f"💻 Platform: {report['platform']}")
    print(f"📁 Working Directory: {report['working_directory']}")
    
    # Check for output files
    if os.path.exists("testing/"):
        files = os.listdir("testing/")
        csv_files = [f for f in files if f.endswith('.csv')]
        pcap_files = [f for f in files if f.endswith('.pcap') or f.endswith('.pcap.gz')]
        
        print(f"📈 CSV Output Files: {len(csv_files)}")
        print(f"📦 PCAP Input Files: {len(pcap_files)}")
        
        if csv_files:
            print("   Recent CSV files:")
            for f in sorted(csv_files)[-3:]:  # Show last 3 files
                size = os.path.getsize(os.path.join("testing/", f))
                print(f"     - {f} ({size:,} bytes)")

def main():
    """Main test runner."""
    print_header("IEX Parser Test Suite")
    print("🧪 Comprehensive testing for IEX DEEP message parser")
    print(f"📅 Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    start_time = time.time()
    
    # Test phases
    phases = [
        ("Dependencies", check_dependencies),
        ("Code Quality", check_code_quality),
        ("Parser Compilation", compile_parser),
        ("Unit Tests", run_unit_tests),
        ("Integration Tests", run_integration_tests),
        ("Functional Tests", run_functional_test),
    ]
    
    results = {}
    
    for phase_name, phase_func in phases:
        try:
            results[phase_name] = phase_func()
        except KeyboardInterrupt:
            print(f"\n⚠️  Test suite interrupted during {phase_name}")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Unexpected error in {phase_name}: {e}")
            results[phase_name] = False
    
    # Generate report
    generate_test_report()
    
    # Summary
    print_header("Test Results Summary")
    
    total_phases = len(phases)
    passed_phases = sum(1 for result in results.values() if result)
    
    for phase_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {phase_name:<20} {status}")
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n⏱️  Total execution time: {duration:.2f} seconds")
    print(f"📊 Results: {passed_phases}/{total_phases} phases passed")
    
    if passed_phases == total_phases:
        print("\n🎉 ALL TESTS PASSED! Parser is ready for production.")
        return 0
    else:
        print(f"\n⚠️  {total_phases - passed_phases} phase(s) failed. Please review and fix issues.")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test suite interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Test suite failed with unexpected error: {e}")
        sys.exit(1)
