
import unittest
import json
import sys
import importlib
from typing import Dict, Any, List

# Global storage for test results
TEST_RESULTS_STORAGE = []

class EnhancedTestResult(unittest.TestResult):
    """Custom test result that captures Expected/Actual/Notes."""
    
    def __init__(self, stream=None, descriptions=None, verbosity=None):
        super().__init__()
        global TEST_RESULTS_STORAGE
        TEST_RESULTS_STORAGE = []
    
    def startTest(self, test):
        super().startTest(test)
        test._current_test_data = {
            "name": test._testMethodName,
            "description": test._testMethodDoc or self._method_name_to_description(test._testMethodName),
            "class_name": test.__class__.__name__,
            "expected": None,
            "actual": None,
            "input": None,  # NEW: Field for input data
            "message": None,  # Educational message for students
            "status": "RUNNING"
        }
    
    def _method_name_to_description(self, method_name: str) -> str:
        """Convert test_method_name to 'Test Method Name'."""
        if method_name.startswith('test_'):
            name = method_name[5:]  # Remove 'test_' prefix
        elif method_name.startswith('test'):
            name = method_name[4:]  # Remove 'test' prefix
        else:
            name = method_name
        
        # Convert snake_case or camelCase to spaced words
        result = []
        for i, char in enumerate(name):
            if char == '_':
                result.append(' ')
            elif char.isupper() and i > 0 and name[i-1].islower():
                result.append(' ')
                result.append(char.lower())
            else:
                result.append(char.lower() if i > 0 else char.upper())
        
        return ''.join(result)
    
    def addSuccess(self, test):
        super().addSuccess(test)
        if hasattr(test, '_current_test_data'):
            test._current_test_data["status"] = "PASSED"
            # Keep custom message if set, otherwise use default success message
            if not test._current_test_data["message"]:
                test._current_test_data["message"] = "Great job! This test passed successfully."
            TEST_RESULTS_STORAGE.append(test._current_test_data.copy())
    
    def addError(self, test, err):
        super().addError(test, err)
        if hasattr(test, '_current_test_data'):
            test._current_test_data["status"] = "ERROR"
            error_msg = str(err[1]).strip() if err and len(err) > 1 else "Unknown error"
            # Keep custom message if set, otherwise provide educational error message
            if not test._current_test_data["message"]:
                test._current_test_data["message"] = f"Your code encountered an unexpected error: {error_msg}. Check your syntax and logic."
            TEST_RESULTS_STORAGE.append(test._current_test_data.copy())
    
    def addFailure(self, test, err):
        super().addFailure(test, err)
        if hasattr(test, '_current_test_data'):
            test._current_test_data["status"] = "FAILED"
            failure_msg = str(err[1]).strip() if err and len(err) > 1 else "Test failed"
            # Keep custom message if set, otherwise provide educational failure message
            if not test._current_test_data["message"]:
                test._current_test_data["message"] = f"This test didn't pass. {failure_msg}. Review the expected vs actual values to understand what went wrong."
            TEST_RESULTS_STORAGE.append(test._current_test_data.copy())


class EnhancedTestCase(unittest.TestCase):
    """
    Base test case that provides Enhanced Expected/Actual/Notes functionality.
    
    Users should extend this class instead of unittest.TestCase.
    """
    
    def setUp(self):
        """Called before each test method."""
        super().setUp()
        if hasattr(self, '_current_test_data'):
            self._current_test_data["expected"] = None
            self._current_test_data["actual"] = None
            self._current_test_data["input"] = None
            self._current_test_data["message"] = None
    
    def set_expected_actual(self, expected, actual, message=None):
        """Set expected and actual values for the current test."""
        if hasattr(self, '_current_test_data'):
            self._current_test_data["expected"] = str(expected)
            self._current_test_data["actual"] = str(actual)
            if message:
                self._current_test_data["message"] = message
    
    def set_input(self, input_value):
        """Set the input value(s) used for this test."""
        if hasattr(self, '_current_test_data'):
            # Handle various input formats
            if isinstance(input_value, list):
                # Use newlines to match how stdin actually works
                self._current_test_data["input"] = "\\n".join(str(x) for x in input_value)
            elif isinstance(input_value, dict):
                self._current_test_data["input"] = json.dumps(input_value)
            else:
                self._current_test_data["input"] = str(input_value)
    
    def set_message(self, message):
        """Set an educational message for students about this test."""
        if hasattr(self, '_current_test_data'):
            self._current_test_data["message"] = message
    
    def set_description_and_message(self, description, message):
        """Set both description and educational message for this test."""
        if hasattr(self, '_current_test_data'):
            self._current_test_data["description"] = description
            self._current_test_data["message"] = message
    
    # Enhanced assertion methods that capture Expected/Actual
    
    def assertEqualAndCapture(self, actual, expected, message=None):
        """Assert equality and capture Expected/Actual values."""
        self.set_expected_actual(expected, actual, message)
        self.assertEqual(actual, expected)
    
    
    def assertInAndCapture(self, member, container, message=None):
        """Assert membership and capture Expected/Actual values."""
        self.set_expected_actual(f"'{member}' in container", str(member in container), message)
        self.assertIn(member, container)
    
    def assertNotInAndCapture(self, member, container, message=None):
        """Assert non-membership and capture Expected/Actual values."""
        self.set_expected_actual(f"'{member}' not in container", str(member not in container), message)
        self.assertNotIn(member, container)
    
    def assertContainsAndCapture(self, text, substring, message=None):
        """Assert string contains substring and capture Expected/Actual values."""
        contains = substring in text if text else False
        self.set_expected_actual(f"text containing '{substring}'", f"'{text}'", message)
        self.assertIn(substring, text)
    
    def assertGreaterAndCapture(self, a, b, message=None):
        """Assert greater than and capture Expected/Actual values."""
        self.set_expected_actual(f"value > {b}", str(a), message)
        self.assertGreater(a, b)
    
    def assertLessAndCapture(self, a, b, message=None):
        """Assert less than and capture Expected/Actual values."""
        self.set_expected_actual(f"value < {b}", str(a), message)
        self.assertLess(a, b)
    
    def assertGreaterEqualAndCapture(self, a, b, message=None):
        """Assert greater than or equal and capture Expected/Actual values."""
        self.set_expected_actual(f"value >= {b}", str(a), message)
        self.assertGreaterEqual(a, b)
    
    def assertLessEqualAndCapture(self, a, b, message=None):
        """Assert less than or equal and capture Expected/Actual values."""
        self.set_expected_actual(f"value <= {b}", str(a), message)
        self.assertLessEqual(a, b)
    
    def assertIsInstanceAndCapture(self, obj, cls, message=None):
        """Assert is instance and capture Expected/Actual values."""
        self.set_expected_actual(f"instance of {cls.__name__}", type(obj).__name__, message)
        self.assertIsInstance(obj, cls)
    
    def assertIsNoneAndCapture(self, obj, message=None):
        """Assert is None and capture Expected/Actual values."""
        self.set_expected_actual("None", str(obj), message)
        self.assertIsNone(obj)
    
    def assertCallAndCapture(self, callable_func, expected, message=None):
        """
        Call a function and assert the result equals expected, automatically capturing errors.
        
        Args:
            callable_func: A function/lambda to call (e.g., lambda: main.add(10, 5))
            expected: The expected result
            message: Optional educational message for students
        """
        try:
            actual = callable_func()
            self.set_expected_actual(expected, actual, message)
            # Don't use assertEqual here - it throws AssertionError which gets caught
            # Just let the test framework handle the comparison
            if actual != expected:
                self.fail(f"Expected {expected}, but got {actual}")
        except AssertionError:
            # Re-raise assertion errors from our own comparison
            raise
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.set_expected_actual(expected, error_msg, message)
            self.fail(f"Function call failed: {str(e)}")

    def assertSafeCallAndCapture(self, callable_or_value, expected, message=None):
        """
        SONNET-PROOF version: Safely handle both lambda functions and direct values.
        
        This method is designed to be foolproof when AI generates test code:
        - If callable_or_value is a callable (lambda), it calls it safely
        - If callable_or_value is already a value, it uses it directly
        - If callable_or_value is an exception/error, it handles it gracefully
        - Handles all error cases gracefully with clear messaging
        
        Args:
            callable_or_value: Either a lambda function OR a direct value OR an error
            expected: The expected result
            message: Optional educational message for students
        """
        actual = None
        error_occurred = False
        
        try:
            # Check if it's callable (lambda/function)
            if callable(callable_or_value):
                try:
                    actual = callable_or_value()
                except Exception as e:
                    error_occurred = True
                    actual = f"Runtime error: {str(e)}"
            else:
                # It's a direct value - this handles the case where AI forgot to use lambda
                # or where the function call failed before reaching the assertion
                actual = callable_or_value
                
        except Exception as e:
            # Catch any other unexpected errors (shouldn't happen but just in case)
            error_occurred = True
            actual = f"Unexpected error: {str(e)}"
        
        # Always set the expected/actual values for reporting
        self.set_expected_actual(expected, actual, message)
        
        # Handle the comparison
        if error_occurred:
            self.fail(f"Test execution failed: {actual}")
        elif actual != expected:
            self.fail(f"Expected {expected}, but got {actual}")
        # If we get here, the test passed!

    def safe_test_wrapper(self, test_func, expected, message=None):
        """
        Ultra-safe wrapper for test functions that might have errors anywhere.
        
        This catches ANY error that occurs during test execution, even before 
        reaching the assertion, and reports it properly.
        
        Usage:
            def test_something(self):
                self.safe_test_wrapper(
                    lambda: main.add(10, 5),  # or any code that might fail
                    15,
                    "Your add function should work"
                )
        """
        try:
            if callable(test_func):
                actual = test_func()
            else:
                actual = test_func
            
            self.set_expected_actual(expected, actual, message)
            
            if actual != expected:
                self.fail(f"Expected {expected}, but got {actual}")
                
        except Exception as e:
            # Catch ANY error and report it properly
            error_msg = f"Error: {str(e)}"
            self.set_expected_actual(expected, error_msg, message)
            self.fail(f"Test failed with error: {str(e)}")


def safe_test(expected, message=None, input_value=None):
    """
    SONNET-PROOF DECORATOR: Equality test (==)
    
    Usage:
        @safe_test(15, "Should return 15", input_value=[10, 5])
        def test_add_basic(self):
            return main.add(10, 5)
    """
    def decorator(test_method):
        def wrapper(self):
            # Set input if provided
            if input_value is not None:
                self.set_input(input_value)
            
            try:
                actual = test_method(self)
                self.set_expected_actual(expected, actual, message)
                if actual != expected:
                    raise AssertionError(f"Expected {expected}, but got {actual}")
            except AssertionError:
                # Re-raise assertion errors (these are test failures, not runtime errors)
                raise
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                self.set_expected_actual(expected, error_msg, message)
                raise AssertionError(f"Test failed with error: {str(e)}")
        return wrapper
    return decorator




def safe_contains(expected_substring, message=None, input_value=None):
    """
    SONNET-PROOF DECORATOR: Contains test (uses assertIn underneath)
    
    Usage:
        @safe_contains("Hello", "Should contain Hello", input_value="World")
        def test_greeting(self):
            return main.get_greeting("World")
    """
    def decorator(test_method):
        def wrapper(self):
            # Set input if provided
            if input_value is not None:
                self.set_input(input_value)
            
            try:
                actual = test_method(self)
                self.set_expected_actual(f"contains '{expected_substring}'", actual, message)
                if expected_substring not in str(actual):
                    self.fail(f"Expected '{actual}' to contain '{expected_substring}'")
            except AssertionError:
                # Re-raise assertion errors (these are test failures, not runtime errors)
                raise
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                self.set_expected_actual(f"contains '{expected_substring}'", error_msg, message)
                self.fail(f"Test failed with error: {str(e)}")
        return wrapper
    return decorator


def safe_greater_equal(expected_min, message=None, input_value=None):
    """
    SONNET-PROOF DECORATOR: Greater than or equal test (>=)
    
    Usage:
        @safe_greater_equal(10, "Should be >= 10", input_value=5)
        def test_result(self):
            return main.get_number()
    """
    def decorator(test_method):
        def wrapper(self):
            # Set input if provided
            if input_value is not None:
                self.set_input(input_value)
            
            try:
                actual = test_method(self)
                self.set_expected_actual(f">= {expected_min}", actual, message)
                if not (actual >= expected_min):
                    self.fail(f"Expected {actual} to be >= {expected_min}")
            except AssertionError:
                raise
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                self.set_expected_actual(f">= {expected_min}", error_msg, message)
                self.fail(f"Test failed with error: {str(e)}")
        return wrapper
    return decorator


def safe_less_equal(expected_max, message=None, input_value=None):
    """
    SONNET-PROOF DECORATOR: Less than or equal test (<=)
    
    Usage:
        @safe_less_equal(100, "Should be <= 100", input_value=50)
        def test_result(self):
            return main.get_number()
    """
    def decorator(test_method):
        def wrapper(self):
            # Set input if provided
            if input_value is not None:
                self.set_input(input_value)
            
            try:
                actual = test_method(self)
                self.set_expected_actual(f"<= {expected_max}", actual, message)
                if not (actual <= expected_max):
                    self.fail(f"Expected {actual} to be <= {expected_max}")
            except AssertionError:
                raise
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                self.set_expected_actual(f"<= {expected_max}", error_msg, message)
                self.fail(f"Test failed with error: {str(e)}")
        return wrapper
    return decorator


def safe_instance(expected_type, message=None, input_value=None):
    """
    SONNET-PROOF DECORATOR: Instance type test
    
    Usage:
        @safe_instance(int, "Should return an integer", input_value=42)
        def test_result(self):
            return main.get_number()
    """
    def decorator(test_method):
        def wrapper(self):
            # Set input if provided
            if input_value is not None:
                self.set_input(input_value)
            
            try:
                actual = test_method(self)
                self.set_expected_actual(f"instance of {expected_type.__name__}", type(actual).__name__, message)
                if not isinstance(actual, expected_type):
                    self.fail(f"Expected {actual} to be instance of {expected_type.__name__}, got {type(actual).__name__}")
            except AssertionError:
                raise
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                self.set_expected_actual(f"instance of {expected_type.__name__}", error_msg, message)
                self.fail(f"Test failed with error: {str(e)}")
        return wrapper
    return decorator


def safe_none(message=None, input_value=None):
    """
    SONNET-PROOF DECORATOR: None test
    
    Usage:
        @safe_none("Should return None", input_value=None)
        def test_result(self):
            return main.get_nothing()
    """
    def decorator(test_method):
        def wrapper(self):
            # Set input if provided
            if input_value is not None:
                self.set_input(input_value)
            
            try:
                actual = test_method(self)
                self.set_expected_actual("None", str(actual), message)
                if actual is not None:
                    self.fail(f"Expected None, but got {actual}")
            except AssertionError:
                raise
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                self.set_expected_actual("None", error_msg, message)
                self.fail(f"Test failed with error: {str(e)}")
        return wrapper
    return decorator


def safe_greater(expected_min, message=None, input_value=None):
    """
    SONNET-PROOF DECORATOR: Greater than test (>)
    
    Usage:
        @safe_greater(10, "Should be greater than 10", input_value=15)
        def test_large_result(self):
            return main.calculate_large_number()
    """
    def decorator(test_method):
        def wrapper(self):
            # Set input if provided
            if input_value is not None:
                self.set_input(input_value)
            
            try:
                actual = test_method(self)
                self.set_expected_actual(f"> {expected_min}", actual, message)
                if not (actual > expected_min):
                    self.fail(f"Expected {actual} to be greater than {expected_min}")
            except AssertionError:
                raise
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                self.set_expected_actual(f"> {expected_min}", error_msg, message)
                self.fail(f"Test failed with error: {str(e)}")
        return wrapper
    return decorator


def safe_less(expected_max, message=None, input_value=None):
    """
    SONNET-PROOF DECORATOR: Less than test (<)
    
    Usage:
        @safe_less(10, "Should be less than 10", input_value=5)
        def test_small_result(self):
            return main.calculate_small_number()
    """
    def decorator(test_method):
        def wrapper(self):
            # Set input if provided
            if input_value is not None:
                self.set_input(input_value)
            
            try:
                actual = test_method(self)
                self.set_expected_actual(f"< {expected_max}", actual, message)
                if not (actual < expected_max):
                    self.fail(f"Expected {actual} to be less than {expected_max}")
            except AssertionError:
                raise
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                self.set_expected_actual(f"< {expected_max}", error_msg, message)
                self.fail(f"Test failed with error: {str(e)}")
        return wrapper
    return decorator

 
def run_test_class(test_class_name: str) -> Dict[str, Any]:
    """
    Run all tests from a specified test class.
    
    Args:
        test_class_name: Name of the test class to run (e.g., 'MainTests')
    
    Returns:
        Dictionary containing test results
    """
    try:
        # Import the test class
        module = importlib.import_module(test_class_name)
        test_class = getattr(module, test_class_name)
        
        # Create test suite
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(test_class)
        
        # Count tests
        test_count = suite.countTestCases()
        print(f"📊 TEST SUMMARY:")
        print(f"   Total: {test_count}")
        print()
        
        # Run tests with enhanced result
        runner = unittest.TextTestRunner(
            resultclass=EnhancedTestResult,
            verbosity=0,
            stream=open('/dev/null', 'w')  # Suppress default output
        )
        
        result = runner.run(suite)
        
        # Print results summary
        passed = len([r for r in TEST_RESULTS_STORAGE if r["status"] == "PASSED"])
        failed = len([r for r in TEST_RESULTS_STORAGE if r["status"] in ["FAILED", "ERROR"]])
        
        print("📈 RESULTS SUMMARY:")
        print(f"   ✅ Passed: {passed}")
        print(f"   ❌ Failed: {failed}")
        print(f"   📊 Total:  {len(TEST_RESULTS_STORAGE)}")
        print()
        
        # Print detailed results
        print_detailed_results()
        
        # Print JSON results
        json_results = print_json_results()
        
        return json_results
        
    except ImportError:
        print(f"❌ Test class not found: {test_class_name}")
        print("Make sure the test file exists and is in the Python path.")
        return {"error": f"Test class '{test_class_name}' not found"}
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return {"error": str(e)}


def print_detailed_results():
    """Print detailed test results in parsing-friendly format."""
    print("Starting Tests")
    
    for result in TEST_RESULTS_STORAGE:
        passed = result["status"] == "PASSED"
        
        # Print "new" separator
        print("new")
        
        # Print all test fields including input, description and educational message
        name = result['name']
        description = result.get('description', 'N/A')
        expected = result['expected'] or 'N/A'
        actual = result['actual'] or 'N/A'
        input_value = result.get('input')
        message = result.get('message', '')
        
        # Enhanced output format with optional Input field
        print(f"Name: {name}", end="")
        
        # Add Input field if it exists
        if input_value:
            print(f" Input: {input_value}", end="")
        
        print(f" Expected: {expected} Actual: {actual}", end="")
        
        if message:
            print(f" Message: {message}", end="")
        
        print(f" Passed: {passed} Description: {description}")
    
    print("Ending Tests")


def print_json_results() -> Dict[str, Any]:
    """Print and return results in JSON format."""
    print("📋 JSON RESULTS:")
    print("=" * 30)
    
    json_output = {
        "framework": "Enhanced Testing Framework for JuiceMind IDE (Python)",
        "total_tests": len(TEST_RESULTS_STORAGE),
        "tests": TEST_RESULTS_STORAGE
    }
    
    print(json.dumps(json_output, indent=2))
    return json_output


def main():
    """Main entry point for the test runner."""
    if len(sys.argv) > 1:
        test_class_name = sys.argv[1]
    else:
        test_class_name = "MainTests"  # Default test class
    
    run_test_class(test_class_name)


if __name__ == "__main__":
    main()

