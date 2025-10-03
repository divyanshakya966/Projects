"""
Basic Math Module - Elementary Mathematical Operations

This module handles basic arithmetic, algebraic operations, 
trigonometric functions, logarithms, and other elementary mathematics.
"""

import math
import re
from typing import Union, Dict, Any, List
from decimal import Decimal, getcontext
import cmath

# Set precision for decimal operations
getcontext().prec = 28


class BasicMathOperations:
    """Class for handling basic mathematical operations and evaluations."""

    def __init__(self):
        """Initialize mathematical constants and function mappings."""
        self.constants = {
            'pi': math.pi,
            'π': math.pi,
            'e': math.e,
            'phi': (1 + math.sqrt(5)) / 2,  # Golden ratio
            'gamma': 0.5772156649015329,    # Euler-Mascheroni constant
            'inf': float('inf'),
            'nan': float('nan'),
        }

        self.functions = {
            # Trigonometric functions
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'asin': math.asin,
            'acos': math.acos,
            'atan': math.atan,
            'atan2': math.atan2,

            # Hyperbolic functions
            'sinh': math.sinh,
            'cosh': math.cosh,
            'tanh': math.tanh,
            'asinh': math.asinh,
            'acosh': math.acosh,
            'atanh': math.atanh,

            # Exponential and logarithmic
            'exp': math.exp,
            'ln': math.log,
            'log': math.log10,
            'log2': math.log2,
            'pow': pow,

            # Power and root functions
            'sqrt': math.sqrt,
            'cbrt': lambda x: x ** (1/3),
            'abs': abs,
            'sign': lambda x: 1 if x > 0 else -1 if x < 0 else 0,

            # Rounding functions
            'floor': math.floor,
            'ceil': math.ceil,
            'round': round,
            'trunc': math.trunc,

            # Other functions
            'factorial': math.factorial,
            'gcd': math.gcd,
            'lcm': lambda a, b: abs(a * b) // math.gcd(a, b),
            'max': max,
            'min': min,
        }

        # Operator precedence
        self.operators = {
            '+': (1, lambda x, y: x + y),
            '-': (1, lambda x, y: x - y),
            '*': (2, lambda x, y: x * y),
            '/': (2, lambda x, y: x / y),
            '//': (2, lambda x, y: x // y),
            '%': (2, lambda x, y: x % y),
            '^': (3, lambda x, y: x ** y),
            '**': (3, lambda x, y: x ** y),
        }

    def evaluate_expression(self, expression: str, variables: Dict[str, float] = None) -> Union[float, int, complex]:
        """
        Evaluate a mathematical expression safely.

        Args:
            expression (str): Mathematical expression to evaluate
            variables (Dict, optional): Variable values

        Returns:
            Union[float, int, complex]: Result of evaluation
        """
        if variables is None:
            variables = {}

        try:
            # Clean and prepare expression
            expr = self._preprocess_expression(expression)

            # Create safe evaluation namespace
            safe_dict = self._create_safe_namespace(variables)

            # Evaluate the expression
            result = eval(expr, safe_dict)

            # Format result appropriately
            return self._format_result(result)

        except Exception as e:
            raise ValueError(f"Cannot evaluate expression '{expression}': {str(e)}")

    def _preprocess_expression(self, expr: str) -> str:
        """Preprocess expression for safe evaluation."""
        # Remove extra whitespace
        expr = re.sub(r'\s+', '', expr)

        # Replace mathematical symbols
        replacements = {
            '×': '*',
            '÷': '/',
            '²': '**2',
            '³': '**3',
            '√': 'sqrt',
            'π': 'pi',
            '∞': 'inf',
        }

        for old, new in replacements.items():
            expr = expr.replace(old, new)

        # Handle implicit multiplication
        expr = self._add_implicit_multiplication(expr)

        # Replace ^ with ** for Python exponentiation
        expr = expr.replace('^', '**')

        return expr

    def _add_implicit_multiplication(self, expr: str) -> str:
        """Add explicit multiplication signs where implicit."""
        # Number followed by variable or function
        expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)

        # Number followed by opening parenthesis
        expr = re.sub(r'(\d)\(', r'\1*(', expr)

        # Closing parenthesis followed by number or variable
        expr = re.sub(r'\)([a-zA-Z0-9])', r')*\1', expr)

        # Variable followed by opening parenthesis (function call)
        # This should be handled carefully to not break function calls

        return expr

    def _create_safe_namespace(self, variables: Dict[str, float]) -> Dict[str, Any]:
        """Create a safe namespace for expression evaluation."""
        safe_dict = {
            '__builtins__': {},  # Remove all builtins for security
            **self.constants,
            **self.functions,
            **variables,
        }

        return safe_dict

    def _format_result(self, result: Union[float, int, complex]) -> Union[float, int, complex]:
        """Format the result appropriately."""
        if isinstance(result, complex):
            # Handle complex numbers
            if abs(result.imag) < 1e-10:  # Effectively real
                return result.real
            return result

        if isinstance(result, float):
            # Check if it's effectively an integer
            if result.is_integer():
                return int(result)
            return result

        return result

    def solve_quadratic(self, a: float, b: float, c: float) -> List[Union[float, complex]]:
        """
        Solve quadratic equation ax² + bx + c = 0.

        Args:
            a, b, c: Coefficients of the quadratic equation

        Returns:
            List of solutions (real or complex)
        """
        if a == 0:
            if b == 0:
                if c == 0:
                    return ["Infinite solutions"]
                else:
                    return ["No solution"]
            else:
                return [-c / b]  # Linear equation

        # Calculate discriminant
        discriminant = b**2 - 4*a*c

        if discriminant >= 0:
            # Real solutions
            sqrt_disc = math.sqrt(discriminant)
            x1 = (-b + sqrt_disc) / (2*a)
            x2 = (-b - sqrt_disc) / (2*a)
            return [x1, x2]
        else:
            # Complex solutions
            sqrt_disc = cmath.sqrt(discriminant)
            x1 = (-b + sqrt_disc) / (2*a)
            x2 = (-b - sqrt_disc) / (2*a)
            return [x1, x2]

    def calculate_statistics(self, numbers: List[float]) -> Dict[str, float]:
        """Calculate basic statistics for a list of numbers."""
        if not numbers:
            raise ValueError("Cannot calculate statistics for empty list")

        n = len(numbers)
        sorted_nums = sorted(numbers)

        # Basic statistics
        mean = sum(numbers) / n

        # Median
        if n % 2 == 0:
            median = (sorted_nums[n//2 - 1] + sorted_nums[n//2]) / 2
        else:
            median = sorted_nums[n//2]

        # Mode (most frequent value)
        frequency = {}
        for num in numbers:
            frequency[num] = frequency.get(num, 0) + 1
        mode = max(frequency, key=frequency.get)

        # Range
        range_val = max(numbers) - min(numbers)

        # Variance and standard deviation
        variance = sum((x - mean) ** 2 for x in numbers) / n
        std_dev = math.sqrt(variance)

        return {
            'count': n,
            'mean': mean,
            'median': median,
            'mode': mode,
            'range': range_val,
            'min': min(numbers),
            'max': max(numbers),
            'variance': variance,
            'std_dev': std_dev,
            'sum': sum(numbers),
        }

    def convert_units(self, value: float, from_unit: str, to_unit: str, unit_type: str) -> float:
        """
        Convert between different units.

        Args:
            value: Value to convert
            from_unit: Source unit
            to_unit: Target unit
            unit_type: Type of unit (length, weight, temperature, etc.)

        Returns:
            Converted value
        """
        conversions = {
            'length': {
                'mm': 0.001,
                'cm': 0.01,
                'm': 1.0,
                'km': 1000.0,
                'in': 0.0254,
                'ft': 0.3048,
                'yd': 0.9144,
                'mi': 1609.34,
            },
            'weight': {
                'mg': 0.001,
                'g': 1.0,
                'kg': 1000.0,
                'oz': 28.3495,
                'lb': 453.592,
            },
            'area': {
                'mm²': 1e-6,
                'cm²': 1e-4,
                'm²': 1.0,
                'km²': 1e6,
                'in²': 6.4516e-4,
                'ft²': 0.092903,
            },
            'volume': {
                'ml': 0.001,
                'l': 1.0,
                'gal': 3.78541,
                'qt': 0.946353,
                'pt': 0.473176,
                'cup': 0.236588,
            }
        }

        if unit_type not in conversions:
            raise ValueError(f"Unknown unit type: {unit_type}")

        unit_dict = conversions[unit_type]

        if from_unit not in unit_dict or to_unit not in unit_dict:
            raise ValueError(f"Unknown unit for {unit_type}")

        # Convert to base unit, then to target unit
        base_value = value * unit_dict[from_unit]
        result = base_value / unit_dict[to_unit]

        return result

    def calculate_compound_interest(self, principal: float, rate: float, 
                                 time: float, compounds_per_year: int = 1) -> Dict[str, float]:
        """
        Calculate compound interest.

        Args:
            principal: Initial amount
            rate: Annual interest rate (as decimal, e.g., 0.05 for 5%)
            time: Time in years
            compounds_per_year: Number of times interest compounds per year

        Returns:
            Dictionary with calculation results
        """
        amount = principal * (1 + rate / compounds_per_year) ** (compounds_per_year * time)
        interest = amount - principal

        return {
            'principal': principal,
            'rate': rate * 100,  # Convert to percentage
            'time': time,
            'compounds_per_year': compounds_per_year,
            'final_amount': amount,
            'interest_earned': interest,
        }

    def get_function_help(self, function_name: str) -> Dict[str, str]:
        """Get help information for a mathematical function."""
        help_info = {
            'sin': {'description': 'Sine function', 'syntax': 'sin(x)', 'example': 'sin(pi/2) = 1'},
            'cos': {'description': 'Cosine function', 'syntax': 'cos(x)', 'example': 'cos(0) = 1'},
            'tan': {'description': 'Tangent function', 'syntax': 'tan(x)', 'example': 'tan(pi/4) = 1'},
            'ln': {'description': 'Natural logarithm', 'syntax': 'ln(x)', 'example': 'ln(e) = 1'},
            'log': {'description': 'Common logarithm (base 10)', 'syntax': 'log(x)', 'example': 'log(100) = 2'},
            'sqrt': {'description': 'Square root', 'syntax': 'sqrt(x)', 'example': 'sqrt(16) = 4'},
            'exp': {'description': 'Exponential function (e^x)', 'syntax': 'exp(x)', 'example': 'exp(1) = e'},
        }

        return help_info.get(function_name, {
            'description': 'Function not found',
            'syntax': 'Unknown',
            'example': 'None'
        })


# Example usage and testing
if __name__ == "__main__":
    math_ops = BasicMathOperations()

    test_expressions = [
        "2 + 3 * 4",
        "sqrt(16) + 2^3",
        "sin(pi/2) + cos(0)",
        "ln(e) + log(100)",
        "2 * pi * 5",  # Circumference
    ]

    print("🧪 Testing Basic Math Operations")
    print("-" * 40)

    for expr in test_expressions:
        try:
            result = math_ops.evaluate_expression(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"{expr} -> Error: {e}")
        print()

    # Test quadratic solver
    print("\nQuadratic Equation: x² - 5x + 6 = 0")
    solutions = math_ops.solve_quadratic(1, -5, 6)
    print(f"Solutions: {solutions}")
