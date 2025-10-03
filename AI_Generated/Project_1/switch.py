"""
Switch Module - Operation Type Detection and Routing

This module determines the type of mathematical operation requested
and routes it to the appropriate calculation engine.
"""

import re
from typing import Dict, Any, Optional
from modules.derivative_engine import DerivativeEngine
from modules.integral_engine import IntegralEngine  
from modules.basic_math import BasicMathOperations


class CalculusRouter:
    """Routes mathematical expressions to appropriate calculation engines."""

    def __init__(self):
        """Initialize all calculation engines."""
        self.derivative_engine = DerivativeEngine()
        self.integral_engine = IntegralEngine()
        self.basic_math = BasicMathOperations()

        # Define operation patterns
        self.patterns = {
            'derivative': [
                r'd/dx\[.*?\]',           # d/dx[expression]
                r'derivative\(.*?\)',     # derivative(expression)
                r'diff\(.*?\)',          # diff(expression)
                r"d\(.*?\)/dx",          # d(expression)/dx
                r"\'\(.*?\)",           # '(expression) - prime notation
            ],
            'integral': [
                r'∫.*?dx',                 # ∫expression dx
                r'integral\(.*?\)',       # integral(expression)
                r'int\(.*?\)',           # int(expression)
                r'definite\(.*?\)',      # definite(expression, a, b)
                r'∫.*?\|.*?',             # ∫expression|limits
            ],
            'basic_math': [
                r'^[\d\+\-\*/\^\(\)\s\.eπ]+$',  # Basic arithmetic
                r'sqrt\(.*?\)',          # Square root
                r'sin\(.*?\)',           # Sine
                r'cos\(.*?\)',           # Cosine
                r'tan\(.*?\)',           # Tangent
                r'ln\(.*?\)',            # Natural log
                r'log\(.*?\)',           # Logarithm
                r'exp\(.*?\)',           # Exponential
            ]
        }

    def determine_operation(self, expression: str) -> str:
        """
        Determine the type of operation based on the expression.

        Args:
            expression (str): The mathematical expression

        Returns:
            str: Operation type ('derivative', 'integral', or 'basic_math')
        """
        expression = expression.lower().strip()

        # Check for derivative patterns
        for pattern in self.patterns['derivative']:
            if re.search(pattern, expression):
                return 'derivative'

        # Check for integral patterns  
        for pattern in self.patterns['integral']:
            if re.search(pattern, expression):
                return 'integral'

        # Check if it contains variables (likely calculus)
        if re.search(r'[a-z]', expression) and 'x' in expression:
            # If it contains x and mathematical functions, might be calculus
            if any(func in expression for func in ['sin', 'cos', 'tan', 'ln', 'log', 'exp']):
                # Default to basic math unless explicitly marked for calculus
                return 'basic_math'

        # Default to basic math
        return 'basic_math'

    def route_calculation(self, expression: str, operation_type: str, formulas: Dict) -> Any:
        """
        Route the calculation to the appropriate engine.

        Args:
            expression (str): The mathematical expression
            operation_type (str): Type of operation
            formulas (Dict): Loaded formulas and rules

        Returns:
            Calculation result
        """
        try:
            if operation_type == 'derivative':
                return self._handle_derivative(expression, formulas)
            elif operation_type == 'integral':
                return self._handle_integral(expression, formulas)
            else:  # basic_math
                return self._handle_basic_math(expression)

        except Exception as e:
            return f"Calculation error: {str(e)}"

    def _handle_derivative(self, expression: str, formulas: Dict) -> str:
        """Handle derivative calculations."""
        # Extract the function to differentiate
        func_to_diff = self._extract_function_from_derivative(expression)

        if not func_to_diff:
            return "Could not extract function from derivative expression"

        # Calculate derivative
        result = self.derivative_engine.calculate_derivative(func_to_diff, formulas)
        return result

    def _handle_integral(self, expression: str, formulas: Dict) -> str:
        """Handle integral calculations."""
        # Extract the function to integrate
        func_to_integrate = self._extract_function_from_integral(expression)

        if not func_to_integrate:
            return "Could not extract function from integral expression"

        # Calculate integral
        result = self.integral_engine.calculate_integral(func_to_integrate, formulas)
        return result

    def _handle_basic_math(self, expression: str) -> str:
        """Handle basic mathematical calculations."""
        result = self.basic_math.evaluate_expression(expression)
        return str(result)

    def _extract_function_from_derivative(self, expression: str) -> Optional[str]:
        """Extract the function to differentiate from derivative notation."""
        patterns = [
            r'd/dx\[(.*?)\]',         # d/dx[function]
            r'derivative\((.*?)\)',    # derivative(function)
            r'diff\((.*?)(?:,.*?)?\)', # diff(function) or diff(function, var)
            r"d\((.*?)\)/dx",         # d(function)/dx
        ]

        for pattern in patterns:
            match = re.search(pattern, expression)
            if match:
                return match.group(1).strip()

        # If no pattern matched, assume the whole expression is the function
        if 'x' in expression:
            return expression

        return None

    def _extract_function_from_integral(self, expression: str) -> Optional[str]:
        """Extract the function to integrate from integral notation."""
        patterns = [
            r'∫(.*?)dx',               # ∫function dx
            r'integral\((.*?)\)',     # integral(function)
            r'int\((.*?)\)',         # int(function)
            r'definite\((.*?),.*?,.*?\)', # definite(function, a, b)
        ]

        for pattern in patterns:
            match = re.search(pattern, expression)
            if match:
                return match.group(1).strip()

        # If no pattern matched, assume the whole expression is the function
        if 'x' in expression:
            return expression

        return None

    def get_operation_info(self, operation_type: str) -> Dict[str, str]:
        """Get information about a specific operation type."""
        info = {
            'derivative': {
                'name': 'Derivative Calculation',
                'description': 'Finds the rate of change of a function',
                'examples': ['d/dx[x^2]', 'derivative(sin(x))', 'diff(ln(x))']
            },
            'integral': {
                'name': 'Integral Calculation', 
                'description': 'Finds the antiderivative or area under curve',
                'examples': ['∫x^2 dx', 'integral(cos(x))', 'definite(x, 0, 1)']
            },
            'basic_math': {
                'name': 'Basic Mathematics',
                'description': 'Evaluates arithmetic and elementary functions',
                'examples': ['2 + 3 * 4', 'sqrt(16)', 'sin(pi/2)']
            }
        }

        return info.get(operation_type, {
            'name': 'Unknown Operation',
            'description': 'Operation type not recognized',
            'examples': []
        })


# Example usage and testing
if __name__ == "__main__":
    router = CalculusRouter()

    test_expressions = [
        "d/dx[x^2 + 3x + 1]",
        "∫2x dx", 
        "2 + 3 * 4",
        "derivative(sin(x))",
        "integral(cos(x))",
        "sqrt(16) + 2^3"
    ]

    print("🧪 Testing Operation Router")
    print("-" * 40)

    for expr in test_expressions:
        op_type = router.determine_operation(expr)
        info = router.get_operation_info(op_type)
        print(f"Expression: {expr}")
        print(f"Type: {op_type} - {info['name']}")
        print(f"Description: {info['description']}")
        print()
