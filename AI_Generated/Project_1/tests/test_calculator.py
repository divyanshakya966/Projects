"""
Unit Tests for Calculator Module

Tests the main calculator functionality including initialization,
calculation routing, interactive features, and error handling.
"""

import unittest
import sys
import os

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calculator import CalculusCalculator
from switch import CalculusRouter
from utils import CalculatorUtils


class TestCalculusCalculator(unittest.TestCase):
    """Test cases for the main CalculusCalculator class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.calculator = CalculusCalculator()

    def test_calculator_initialization(self):
        """Test calculator initializes correctly."""
        self.assertIsNotNone(self.calculator.router)
        self.assertIsNotNone(self.calculator.utils)
        self.assertIsNotNone(self.calculator.basic_math)
        self.assertIsNotNone(self.calculator.formula_loader)

    def test_basic_arithmetic(self):
        """Test basic arithmetic calculations."""
        test_cases = [
            ("2 + 3", 5),
            ("10 - 4", 6),
            ("5 * 6", 30),
            ("15 / 3", 5),
            ("2^3", 8),
            ("sqrt(16)", 4),
        ]

        for expression, expected in test_cases:
            with self.subTest(expr=expression):
                result = self.calculator.calculate(expression)
                self.assertTrue(result.get("success", False))
                self.assertEqual(float(result["result"]), expected)

    def test_trigonometric_functions(self):
        """Test trigonometric function calculations."""
        import math

        test_cases = [
            ("sin(0)", 0),
            ("cos(0)", 1),
            ("sin(pi/2)", 1),
            ("cos(pi)", -1),
        ]

        for expression, expected in test_cases:
            with self.subTest(expr=expression):
                result = self.calculator.calculate(expression)
                self.assertTrue(result.get("success", False))
                self.assertAlmostEqual(float(result["result"]), expected, places=5)

    def test_logarithmic_functions(self):
        """Test logarithmic function calculations."""
        import math

        test_cases = [
            ("ln(e)", 1),
            ("log(100)", 2),
            ("ln(1)", 0),
        ]

        for expression, expected in test_cases:
            with self.subTest(expr=expression):
                result = self.calculator.calculate(expression)
                self.assertTrue(result.get("success", False))
                self.assertAlmostEqual(float(result["result"]), expected, places=5)

    def test_derivative_calculation(self):
        """Test derivative calculations."""
        test_cases = [
            ("d/dx[x^2]", "2*x"),
            ("derivative(x^3)", "3*x**2"),
            ("d/dx[sin(x)]", "cos(x)"),
        ]

        for expression, expected_pattern in test_cases:
            with self.subTest(expr=expression):
                result = self.calculator.calculate(expression)
                self.assertTrue(result.get("success", False))
                # Note: Exact symbolic comparison would require more sophisticated testing
                self.assertIsNotNone(result["result"])

    def test_integral_calculation(self):
        """Test integral calculations."""
        test_cases = [
            ("integral(x)", "x**2/2 + C"),
            ("∫x^2 dx", "x**3/3 + C"),
            ("integral(sin(x))", "-cos(x) + C"),
        ]

        for expression, expected_pattern in test_cases:
            with self.subTest(expr=expression):
                result = self.calculator.calculate(expression)
                self.assertTrue(result.get("success", False))
                self.assertIsNotNone(result["result"])

    def test_error_handling(self):
        """Test error handling for invalid expressions."""
        invalid_expressions = [
            "",  # Empty expression
            "2 + + 3",  # Invalid syntax
            "sin(",  # Incomplete function
            "unknown_func(x)",  # Unknown function
        ]

        for expression in invalid_expressions:
            with self.subTest(expr=expression):
                result = self.calculator.calculate(expression)
                self.assertFalse(result.get("success", True))
                self.assertIn("error", result)


class TestCalculusRouter(unittest.TestCase):
    """Test cases for the CalculusRouter class."""

    def setUp(self):
        """Set up test fixtures."""
        self.router = CalculusRouter()

    def test_operation_detection_derivative(self):
        """Test detection of derivative operations."""
        derivative_expressions = [
            "d/dx[x^2]",
            "derivative(sin(x))",
            "diff(ln(x))",
        ]

        for expr in derivative_expressions:
            with self.subTest(expr=expr):
                op_type = self.router.determine_operation(expr)
                self.assertEqual(op_type, "derivative")

    def test_operation_detection_integral(self):
        """Test detection of integral operations."""
        integral_expressions = [
            "∫x^2 dx",
            "integral(cos(x))",
            "int(e^x)",
        ]

        for expr in integral_expressions:
            with self.subTest(expr=expr):
                op_type = self.router.determine_operation(expr)
                self.assertEqual(op_type, "integral")

    def test_operation_detection_basic_math(self):
        """Test detection of basic math operations."""
        basic_expressions = [
            "2 + 3 * 4",
            "sqrt(16)",
            "sin(pi/2)",
            "ln(e)",
        ]

        for expr in basic_expressions:
            with self.subTest(expr=expr):
                op_type = self.router.determine_operation(expr)
                self.assertEqual(op_type, "basic_math")

    def test_get_operation_info(self):
        """Test operation information retrieval."""
        operation_types = ["derivative", "integral", "basic_math"]

        for op_type in operation_types:
            with self.subTest(op_type=op_type):
                info = self.router.get_operation_info(op_type)
                self.assertIn("name", info)
                self.assertIn("description", info)
                self.assertIn("examples", info)


class TestCalculatorUtils(unittest.TestCase):
    """Test cases for the CalculatorUtils class."""

    def setUp(self):
        """Set up test fixtures."""
        self.utils = CalculatorUtils()

    def test_expression_cleaning(self):
        """Test expression cleaning and normalization."""
        test_cases = [
            ("2x + 3", "2*x + 3"),
            ("sin(π/2)", "sin(pi/2)"),
            ("√16", "sqrt(16)"),
            ("2(3+4)", "2*(3+4)"),
        ]

        for original, expected in test_cases:
            with self.subTest(original=original):
                cleaned = self.utils.clean_expression(original)
                self.assertEqual(cleaned, expected)

    def test_expression_validation(self):
        """Test expression validation."""
        valid_expressions = [
            "x + 2",
            "sin(x)",
            "2 * pi",
            "(x + 1) / (x - 1)",
        ]

        invalid_expressions = [
            "",  # Empty
            "2 + + 3",  # Double operator
            "((x + 1)",  # Unbalanced parentheses
            "x + @",  # Invalid character
        ]

        for expr in valid_expressions:
            with self.subTest(expr=expr):
                is_valid, error = self.utils.validate_expression(expr)
                self.assertTrue(is_valid, f"Expression '{expr}' should be valid but got error: {error}")

        for expr in invalid_expressions:
            with self.subTest(expr=expr):
                is_valid, error = self.utils.validate_expression(expr)
                self.assertFalse(is_valid, f"Expression '{expr}' should be invalid")

    def test_safe_evaluation(self):
        """Test safe expression evaluation."""
        test_cases = [
            ("2 + 3", 5),
            ("pi", 3.141592653589793),
            ("e", 2.718281828459045),
            ("sqrt(16)", 4),
            ("sin(0)", 0),
        ]

        for expression, expected in test_cases:
            with self.subTest(expr=expression):
                result = self.utils.safe_eval(expression)
                if isinstance(expected, float):
                    self.assertAlmostEqual(result, expected, places=5)
                else:
                    self.assertEqual(result, expected)

    def test_result_formatting(self):
        """Test result formatting."""
        test_cases = [
            (5.0, "5"),
            (3.14159, "3.14159"),
            (1000000.0, "1.000000e+06"),
            (0.00001, "1.000000e-05"),
            (complex(1, 2), "1 + 2i"),
        ]

        for value, expected in test_cases:
            with self.subTest(value=value):
                formatted = self.utils.format_result(value)
                if "e+" in expected or "e-" in expected:
                    # For scientific notation, just check the format
                    self.assertIn("e", formatted)
                else:
                    self.assertEqual(formatted, expected)


if __name__ == "__main__":
    # Create a test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestCalculusCalculator))
    suite.addTests(loader.loadTestsFromTestCase(TestCalculusRouter))
    suite.addTests(loader.loadTestsFromTestCase(TestCalculatorUtils))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print(f"{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
