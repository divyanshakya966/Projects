"""
Unit Tests for Utils Module

Tests utility functions including mathematical operations,
expression parsing, validation, and helper functions.
"""

import unittest
import sys
import os
import math

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import CalculatorUtils


class TestCalculatorUtils(unittest.TestCase):
    """Comprehensive tests for CalculatorUtils class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.utils = CalculatorUtils()

    def test_constants(self):
        """Test mathematical constants are correctly defined."""
        self.assertAlmostEqual(self.utils.constants['pi'], math.pi, places=10)
        self.assertAlmostEqual(self.utils.constants['e'], math.e, places=10)
        self.assertAlmostEqual(self.utils.constants['phi'], (1 + math.sqrt(5)) / 2, places=10)
        self.assertEqual(self.utils.constants['inf'], float('inf'))

    def test_function_mappings(self):
        """Test mathematical function mappings."""
        # Test trigonometric functions
        self.assertEqual(self.utils.functions['sin'](0), 0)
        self.assertEqual(self.utils.functions['cos'](0), 1)
        self.assertAlmostEqual(self.utils.functions['sin'](math.pi/2), 1, places=10)

        # Test logarithmic functions
        self.assertAlmostEqual(self.utils.functions['ln'](math.e), 1, places=10)
        self.assertEqual(self.utils.functions['log'](100), 2)

        # Test other functions
        self.assertEqual(self.utils.functions['sqrt'](16), 4)
        self.assertEqual(self.utils.functions['abs'](-5), 5)

    def test_clean_expression(self):
        """Test expression cleaning and normalization."""
        test_cases = [
            # Basic cleaning
            ("  x + 2  ", "x + 2"),
            ("2×3", "2*3"),
            ("10÷2", "10/2"),
            ("x²", "x^2"),
            ("x³", "x^3"),
            ("√x", "sqrt(x)"),
            ("π", "pi"),

            # Implicit multiplication
            ("2x", "2*x"),
            ("3(x+1)", "3*(x+1)"),
            ("x(y+z)", "x*(y+z)"),
            ("(a+b)(c+d)", "(a+b)*(c+d)"),
        ]

        for original, expected in test_cases:
            with self.subTest(original=original):
                result = self.utils.clean_expression(original)
                self.assertEqual(result, expected)

    def test_validate_expression(self):
        """Test expression validation."""
        # Valid expressions
        valid_cases = [
            "x + 2",
            "sin(x) + cos(x)",
            "2 * pi * r",
            "(x + 1) / (x - 1)",
            "e^x",
            "ln(x)",
        ]

        for expr in valid_cases:
            with self.subTest(expr=expr):
                is_valid, error = self.utils.validate_expression(expr)
                self.assertTrue(is_valid, f"'{expr}' should be valid, but got: {error}")

        # Invalid expressions
        invalid_cases = [
            ("", "Empty expression"),
            ("2 + + 3", "consecutive operators"),
            ("((x + 1)", "unbalanced parentheses"),
            (")x + 1(", "unbalanced parentheses"),
        ]

        for expr, error_type in invalid_cases:
            with self.subTest(expr=expr):
                is_valid, error = self.utils.validate_expression(expr)
                self.assertFalse(is_valid, f"'{expr}' should be invalid")

    def test_balanced_parentheses(self):
        """Test parentheses balance checking."""
        balanced_cases = [
            "()",
            "(x + 1)",
            "((x + 1) * (x - 1))",
            "sin(pi/2) + cos(0)",
            "",  # Empty string is balanced
        ]

        unbalanced_cases = [
            "(",
            ")",
            "(()",
            "())",
            "(x + 1))",
            "sin(x + cos(y)",
        ]

        for expr in balanced_cases:
            with self.subTest(expr=expr):
                is_balanced = self.utils._check_balanced_parentheses(expr)
                self.assertTrue(is_balanced, f"'{expr}' should be balanced")

        for expr in unbalanced_cases:
            with self.subTest(expr=expr):
                is_balanced = self.utils._check_balanced_parentheses(expr)
                self.assertFalse(is_balanced, f"'{expr}' should be unbalanced")

    def test_parse_function_call(self):
        """Test function call parsing."""
        test_cases = [
            ("sin(x)", ("sin", ["x"])),
            ("log(10)", ("log", ["10"])),
            ("pow(2, 3)", ("pow", ["2", "3"])),
            ("max(1, 2, 3)", ("max", ["1", "2", "3"])),
            ("func(a, b+c, d)", ("func", ["a", "b+c", "d"])),
        ]

        for expr, expected in test_cases:
            with self.subTest(expr=expr):
                result = self.utils.parse_function_call(expr)
                self.assertEqual(result, expected)

    def test_substitute_constants(self):
        """Test constant substitution."""
        test_cases = [
            ("pi", str(math.pi)),
            ("e", str(math.e)),
            ("2 * pi", f"2 * {math.pi}"),
            ("sin(pi/2)", f"sin({math.pi}/2)"),
            ("e^2", f"{math.e}^2"),
        ]

        for original, expected in test_cases:
            with self.subTest(original=original):
                result = self.utils.substitute_constants(original)
                self.assertEqual(result, expected)

    def test_format_result(self):
        """Test result formatting."""
        test_cases = [
            # Integer-like floats
            (5.0, "5"),
            (10.0, "10"),

            # Regular decimals
            (3.14159, "3.14159"),
            (2.5, "2.5"),

            # Scientific notation (large numbers)
            (1e6, "1.000000e+06"),
            (2.5e8, "2.500000e+08"),

            # Scientific notation (small numbers) 
            (1e-5, "1.000000e-05"),
            (3.7e-8, "3.700000e-08"),

            # Complex numbers
            (complex(1, 2), "1 + 2i"),
            (complex(3, -4), "3 - 4i"),
            (complex(5, 0), "5"),  # Real part only
        ]

        for value, expected in test_cases:
            with self.subTest(value=value):
                result = self.utils.format_result(value)
                if "e+" in str(expected) or "e-" in str(expected):
                    # For scientific notation, check format pattern
                    self.assertRegex(result, r'\d\.\d+e[+-]\d+')
                else:
                    self.assertEqual(result, expected)

    def test_safe_eval(self):
        """Test safe expression evaluation."""
        test_cases = [
            ("2 + 3", 5),
            ("2 * 3.5", 7.0),
            ("pi", math.pi),
            ("e", math.e),
            ("sin(0)", 0),
            ("cos(pi)", -1),
            ("sqrt(16)", 4),
            ("2^3", 8),  # Should be converted to **
            ("ln(e)", 1),
        ]

        for expr, expected in test_cases:
            with self.subTest(expr=expr):
                result = self.utils.safe_eval(expr)
                if isinstance(expected, float):
                    self.assertAlmostEqual(result, expected, places=5)
                else:
                    self.assertEqual(result, expected)

    def test_safe_eval_with_variables(self):
        """Test safe evaluation with variables."""
        variables = {'x': 2, 'y': 3}

        test_cases = [
            ("x + y", 5),
            ("x * y", 6),
            ("x^y", 8),
            ("sin(x) + cos(y)", math.sin(2) + math.cos(3)),
        ]

        for expr, expected in test_cases:
            with self.subTest(expr=expr):
                result = self.utils.safe_eval(expr, variables)
                if isinstance(expected, float):
                    self.assertAlmostEqual(result, expected, places=5)
                else:
                    self.assertEqual(result, expected)

    def test_derivative_at_point(self):
        """Test numerical derivative calculation."""
        test_cases = [
            ("x^2", "x", 3, 6),  # d/dx[x²] at x=3 should be 6
            ("2*x + 1", "x", 5, 2),  # d/dx[2x+1] at any x should be 2
            ("sin(x)", "x", 0, 1),  # d/dx[sin(x)] at x=0 should be 1
        ]

        for func, var, point, expected in test_cases:
            with self.subTest(func=func, point=point):
                result = self.utils.derivative_at_point(func, var, point)
                self.assertAlmostEqual(result, expected, places=3)

    def test_integral_simpson(self):
        """Test Simpson's rule integration."""
        # Test integral of x^2 from 0 to 1 (should be 1/3)
        result = self.utils.integral_simpson("x^2", "x", 0, 1, 1000)
        self.assertAlmostEqual(result, 1/3, places=3)

        # Test integral of sin(x) from 0 to pi (should be 2)
        result = self.utils.integral_simpson("sin(x)", "x", 0, math.pi, 1000)
        self.assertAlmostEqual(result, 2, places=2)

    def test_get_function_info(self):
        """Test function information retrieval."""
        known_functions = ['sin', 'cos', 'ln', 'sqrt']

        for func in known_functions:
            with self.subTest(func=func):
                info = self.utils.get_function_info(func)
                self.assertIn('description', info)
                self.assertIn('domain', info)
                self.assertIn('range', info)
                self.assertNotEqual(info['description'], 'Unknown function')

        # Test unknown function
        info = self.utils.get_function_info('unknown_func')
        self.assertEqual(info['description'], 'Unknown function')


if __name__ == "__main__":
    # Run the tests
    unittest.main(verbosity=2)
