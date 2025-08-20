#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Runner Script
Runs all tests and provides a comprehensive test report.
"""

import unittest
import sys
import os
import time
from io import StringIO

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def run_test_suite():
    """Run all test suites and return results."""
    # Create test loader
    loader = unittest.TestLoader()
    
    # Discover all test files
    test_dir = os.path.dirname(__file__)
    suite = loader.discover(test_dir, pattern='test_*.py')
    
    # Create test runner
    runner = unittest.TextTestRunner(verbosity=2, stream=StringIO())
    
    # Run tests
    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()
    
    return result, end_time - start_time


def run_individual_test_files():
    """Run individual test files and return detailed results."""
    test_files = [
        'test_basic_functionality.py',
        'test_core_modules.py',
        'test_api_endpoints.py',
        'test_configuration.py',
        'test_integration.py'
    ]
    
    results = {}
    total_time = 0
    
    for test_file in test_files:
        test_path = os.path.join(os.path.dirname(__file__), test_file)
        if os.path.exists(test_path):
            print(f"\n{'='*60}")
            print(f"Running {test_file}")
            print(f"{'='*60}")
            
            # Load and run the test file
            loader = unittest.TestLoader()
            suite = loader.discover(os.path.dirname(__file__), pattern=test_file)
            
            runner = unittest.TextTestRunner(verbosity=2)
            start_time = time.time()
            result = runner.run(suite)
            end_time = time.time()
            
            results[test_file] = {
                'tests_run': result.testsRun,
                'failures': len(result.failures),
                'errors': len(result.errors),
                'skipped': len(result.skipped) if hasattr(result, 'skipped') else 0,
                'time': end_time - start_time
            }
            
            total_time += end_time - start_time
        else:
            print(f"Warning: Test file {test_file} not found")
    
    return results, total_time


def print_test_summary(result, execution_time, detailed_results=None):
    """Print a comprehensive test summary."""
    print("\n" + "="*80)
    print("TEST EXECUTION SUMMARY")
    print("="*80)
    
    # Overall results
    print(f"Total Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Execution Time: {execution_time:.2f} seconds")
    
    # Calculate success rate
    total_issues = len(result.failures) + len(result.errors)
    success_rate = ((result.testsRun - total_issues) / result.testsRun * 100) if result.testsRun > 0 else 0
    print(f"Success Rate: {success_rate:.1f}%")
    
    # Print failures
    if result.failures:
        print(f"\n{'='*40}")
        print("FAILURES")
        print(f"{'='*40}")
        for test, traceback in result.failures:
            print(f"❌ {test}")
            print(f"   {traceback.split('AssertionError:')[-1].strip()}")
    
    # Print errors
    if result.errors:
        print(f"\n{'='*40}")
        print("ERRORS")
        print(f"{'='*40}")
        for test, traceback in result.errors:
            print(f"💥 {test}")
            print(f"   {traceback.split('Exception:')[-1].strip()}")
    
    # Print detailed results if available
    if detailed_results:
        print(f"\n{'='*40}")
        print("DETAILED RESULTS BY TEST FILE")
        print(f"{'='*40}")
        
        for test_file, stats in detailed_results.items():
            status = "✅ PASS" if stats['failures'] == 0 and stats['errors'] == 0 else "❌ FAIL"
            print(f"{status} {test_file}")
            print(f"   Tests: {stats['tests_run']}, Failures: {stats['failures']}, "
                  f"Errors: {stats['errors']}, Time: {stats['time']:.2f}s")
    
    # Final status
    print(f"\n{'='*40}")
    if total_issues == 0:
        print("🎉 ALL TESTS PASSED!")
        print("✅ The application is working correctly.")
    else:
        print(f"⚠️  {total_issues} TEST(S) FAILED")
        print("❌ Please review the failures and errors above.")
    print(f"{'='*40}")


def run_quick_tests():
    """Run a subset of quick tests for development."""
    print("Running Quick Tests...")
    
    # Import and run basic functionality tests
    from test_basic_functionality import TestBasicFunctionality
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestBasicFunctionality)
    
    runner = unittest.TextTestRunner(verbosity=2)
    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()
    
    print_test_summary(result, end_time - start_time)
    
    return result


def main():
    """Main test runner function."""
    print("🧪 Text Processing Application Test Suite")
    print("="*60)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--quick':
            print("Running quick tests only...")
            result = run_quick_tests()
            return 0 if len(result.failures) + len(result.errors) == 0 else 1
        elif sys.argv[1] == '--help':
            print("Usage:")
            print("  python run_all_tests.py          # Run all tests")
            print("  python run_all_tests.py --quick  # Run quick tests only")
            print("  python run_all_tests.py --help   # Show this help")
            return 0
    
    print("Running comprehensive test suite...")
    
    # Run all tests
    result, execution_time = run_test_suite()
    
    # Run individual test files for detailed results
    detailed_results, _ = run_individual_test_files()
    
    # Print summary
    print_test_summary(result, execution_time, detailed_results)
    
    # Return appropriate exit code
    return 0 if len(result.failures) + len(result.errors) == 0 else 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code) 