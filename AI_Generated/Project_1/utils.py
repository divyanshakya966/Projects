"""
Utils Module - Mathematical Utilities and Helper Functions

This module provides utility functions for expression parsing, validation,
mathematical operations, and result formatting.
"""

import re
import math
from typing import Union, Dict, List, Optional, Tuple
from decimal import Decimal, getcontext

# Set high precision for decimal calculations
getcontext().prec = 28


class CalculatorUtils:
    """Utility class containing helper functions for mathematical operations."""

    def __init__(self):
        """Initialize mathematical constants and patterns."""
        self.constants = {
            'pi': math.pi,
            'π': math.pi,
            'e': math.e,
            'inf': float('inf'),
            '∞': float('inf'),
            'phi': (1 + math.sqrt(5)) / 2,  # Golden ratio
        }

        # Mathematical function mappings
        self.functions = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'asin': math.asin,
            'acos': math.acos,
            'atan': math.atan,
            'sinh': math.sinh,
            'cosh': math.cosh,
            'tanh': math.tanh,
            'ln': math.log,
            'log': math.log10,
            'log2': math.log2,
            'exp': math.exp,
            'sqrt': math.sqrt,
            'abs': abs,
            'floor': math.floor,
            'ceil': math.ceil,
            'round': round,
        }

    def clean_expression(self, expression: str) -> str:
        """
        Clean and normalize a mathematical expression.

        Args:
            expression (str): Raw mathematical expression

        Returns:
            str: Cleaned and normalized expression
        """
        if not isinstance(expression, str):
            return ""

        # Remove extra whitespace
        expression = re.sub(r'\s+', ' ', expression.strip())

        # Replace common mathematical symbols
        replacements = {
            '×': '*',
            '÷': '/',
            '²': '^2',
            '³': '^3',
            '√': 'sqrt',
            'π': 'pi',
            '∞': 'inf',
        }

        for old, new in replacements.items():
            expression = expression.replace(old, new)

        # Handle implicit multiplication (2x -> 2*x, 2(3) -> 2*(3))
        expression = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expression)
        expression = re.sub(r'(\d)\(', r'\1*(', expression)
        expression = re.sub(r'\)([a-zA-Z])', r')*\1', expression)
        expression = re.sub(r'\)(\d)', r')*\1', expression)

        return expression

    def validate_expression(self, expression: str) -> Tuple[bool, str]:
        """
        Validate if a mathematical expression is properly formatted.

        Args:
            expression (str): Mathematical expression to validate

        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not expression:
            return False, "Empty expression"

        # Check balanced parentheses
        if not self._check_balanced_parentheses(expression):
            return False, "Unbalanced parentheses"

        # Check for invalid characters
        valid_chars = r'[a-zA-Z0-9+\-*/^().\s∫πe]'
        if re.search(r'[^' + valid_chars[1:-1] + ']', expression):
            invalid_chars = re.findall(r'[^' + valid_chars[1:-1] + ']', expression)
            return False, f"Invalid characters: {', '.join(set(invalid_chars))}"

        # Check for consecutive operators
        if re.search(r'[+\-*/^]{2,}', expression):
            return False, "Consecutive operators not allowed"

        return True, ""

    def _check_balanced_parentheses(self, expression: str) -> bool:
        """Check if parentheses are balanced in the expression."""
        count = 0
        for char in expression:
            if char == '(':
                count += 1
            elif char == ')':
                count -= 1
                if count < 0:
                    return False
        return count == 0

    def parse_function_call(self, expression: str) -> Optional[Tuple[str, List[str]]]:
        """
        Parse a function call and extract function name and arguments.

        Args:
            expression (str): Function call expression

        Returns:
            Optional[Tuple[str, List[str]]]: (function_name, arguments) or None
        """
        pattern = r'(\w+)\((.*?)\)'
        match = re.search(pattern, expression)

        if not match:
            return None

        func_name = match.group(1)
        args_str = match.group(2)

        # Split arguments by comma, considering nested parentheses
        args = self._split_arguments(args_str)

        return func_name, args

    def _split_arguments(self, args_str: str) -> List[str]:
        """Split function arguments considering nested parentheses."""
        if not args_str.strip():
            return []

        args = []
        current_arg = ""
        paren_count = 0

        for char in args_str:
            if char == ',' and paren_count == 0:
                args.append(current_arg.strip())
                current_arg = ""
            else:
                current_arg += char
                if char == '(':
                    paren_count += 1
                elif char == ')':
                    paren_count -= 1

        if current_arg.strip():
            args.append(current_arg.strip())

        return args

    def substitute_constants(self, expression: str) -> str:
        """Substitute mathematical constants with their values."""
        for const, value in self.constants.items():
            # Use word boundaries to avoid partial replacements
            pattern = r'\b' + re.escape(const) + r'\b'
            expression = re.sub(pattern, str(value), expression)

        return expression

    def format_result(self, result: Union[float, int, complex], precision: int = 6) -> str:
        """
        Format calculation result for display.

        Args:
            result: Numerical result
            precision: Number of decimal places

        Returns:
            str: Formatted result string
        """
        if isinstance(result, complex):
            if result.imag == 0:
                result = result.real
            else:
                real_part = self._format_number(result.real, precision)
                imag_part = self._format_number(abs(result.imag), precision)
                sign = "+" if result.imag >= 0 else "-"
                return f"{real_part} {sign} {imag_part}i"

        return self._format_number(result, precision)

    def _format_number(self, num: Union[float, int], precision: int) -> str:
        """Format a single number with appropriate precision."""
        if isinstance(num, int) or num.is_integer():
            return str(int(num))

        # Use scientific notation for very large or very small numbers
        if abs(num) >= 1e6 or (abs(num) < 1e-4 and num != 0):
            return f"{num:.{precision}e}"

        # Regular decimal formatting
        formatted = f"{num:.{precision}f}"
        # Remove trailing zeros
        formatted = formatted.rstrip('0').rstrip('.')

        return formatted

    def safe_eval(self, expression: str, variables: Optional[Dict[str, float]] = None) -> Union[float, int, complex]:
        """
        Safely evaluate a mathematical expression.

        Args:
            expression (str): Mathematical expression
            variables (Dict, optional): Variable values

        Returns:
            Numerical result

        Raises:
            ValueError: If expression cannot be evaluated
        """
        if variables is None:
            variables = {}

        # Create safe namespace
        safe_dict = {
            '__builtins__': {},
            **self.constants,
            **self.functions,
            **variables
        }

        # Replace ^ with ** for Python exponentiation
        expression = re.sub(r'\^', '**', expression)

        try:
            # Validate before evaluation
            is_valid, error_msg = self.validate_expression(expression)
            if not is_valid:
                raise ValueError(f"Invalid expression: {error_msg}")

            result = eval(expression, safe_dict)
            return result

        except Exception as e:
            raise ValueError(f"Evaluation error: {str(e)}")

    def derivative_at_point(self, func_str: str, variable: str, point: float, h: float = 1e-8) -> float:
        """
        Calculate numerical derivative at a specific point using finite differences.

        Args:
            func_str (str): Function expression
            variable (str): Variable to differentiate with respect to
            point (float): Point to evaluate derivative at
            h (float): Small increment for finite difference

        Returns:
            float: Derivative value at the point
        """
        try:
            # Evaluate f(x+h)
            vars_plus = {variable: point + h}
            f_plus = self.safe_eval(func_str, vars_plus)

            # Evaluate f(x-h)
            vars_minus = {variable: point - h}
            f_minus = self.safe_eval(func_str, vars_minus)

            # Central difference formula
            derivative = (f_plus - f_minus) / (2 * h)

            return derivative

        except Exception as e:
            raise ValueError(f"Could not calculate derivative: {str(e)}")

    def integral_simpson(self, func_str: str, variable: str, a: float, b: float, n: int = 1000) -> float:
        """
        Calculate definite integral using Simpson's rule.

        Args:
            func_str (str): Function expression
            variable (str): Variable to integrate with respect to
            a (float): Lower bound
            b (float): Upper bound
            n (int): Number of intervals (must be even)

        Returns:
            float: Approximate integral value
        """
        if n % 2 != 0:
            n += 1  # Make n even

        h = (b - a) / n

        try:
            # Calculate sum using Simpson's rule
            integral_sum = 0

            # First and last terms
            integral_sum += self.safe_eval(func_str, {variable: a})
            integral_sum += self.safe_eval(func_str, {variable: b})

            # Middle terms
            for i in range(1, n):
                x = a + i * h
                coeff = 4 if i % 2 == 1 else 2
                integral_sum += coeff * self.safe_eval(func_str, {variable: x})

            return (h / 3) * integral_sum

        except Exception as e:
            raise ValueError(f"Could not calculate integral: {str(e)}")

    def get_function_info(self, func_name: str) -> Dict[str, str]:
        """Get information about a mathematical function."""
        function_info = {
            'sin': {'description': 'Sine function', 'domain': 'All real numbers', 'range': '[-1, 1]'},
            'cos': {'description': 'Cosine function', 'domain': 'All real numbers', 'range': '[-1, 1]'},
            'tan': {'description': 'Tangent function', 'domain': 'x ≠ π/2 + nπ', 'range': 'All real numbers'},
            'ln': {'description': 'Natural logarithm', 'domain': 'x > 0', 'range': 'All real numbers'},
            'log': {'description': 'Common logarithm (base 10)', 'domain': 'x > 0', 'range': 'All real numbers'},
            'exp': {'description': 'Exponential function (e^x)', 'domain': 'All real numbers', 'range': 'y > 0'},
            'sqrt': {'description': 'Square root function', 'domain': 'x ≥ 0', 'range': 'y ≥ 0'},
        }

        return function_info.get(func_name, {
            'description': 'Unknown function',
            'domain': 'Unknown',
            'range': 'Unknown'
        })


# Example usage and testing
if __name__ == "__main__":
    utils = CalculatorUtils()

    # Test expression cleaning
    test_expressions = [
        "2x + 3",
        "sin(π/2)",
        "2(3 + 4)",
        "√16 + 2³"
    ]

    print("🧪 Testing Calculator Utils")
    print("-" * 40)

    for expr in test_expressions:
        cleaned = utils.clean_expression(expr)
        valid, error = utils.validate_expression(cleaned)
        print(f"Original: {expr}")
        print(f"Cleaned:  {cleaned}")
        print(f"Valid:    {valid} {'✅' if valid else '❌ ' + error}")
        print()
