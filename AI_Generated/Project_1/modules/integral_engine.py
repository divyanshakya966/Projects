"""
Integral Engine - Advanced Integration Calculation Module

This module implements symbolic integration using various techniques
including power rule, substitution, integration by parts, and numerical methods.
"""

import re
import math
from typing import Dict, List, Optional, Union, Tuple


class IntegralEngine:
    """Advanced engine for calculating symbolic and numeric integrals."""

    def __init__(self):
        """Initialize integration rules and patterns."""
        self.basic_integrals = {
            '1': 'x',
            'x': 'x²/2',
            'x^n': 'x^(n+1)/(n+1)',  # Power rule (n ≠ -1)
            '1/x': 'ln|x|',
            'sin(x)': '-cos(x)',
            'cos(x)': 'sin(x)',
            'tan(x)': '-ln|cos(x)|',
            'sec²(x)': 'tan(x)',
            'csc²(x)': '-cot(x)',
            'sec(x)*tan(x)': 'sec(x)',
            'csc(x)*cot(x)': '-csc(x)',
            'e^x': 'e^x',
            '1/sqrt(1-x²)': 'arcsin(x)',
            '1/(1+x²)': 'arctan(x)',
            '1/sqrt(x²-1)': 'ln|x + sqrt(x²-1)|',
        }

        self.substitution_patterns = {
            r'sin\((.+)\)': ('u = {}', 'cos(u) du'),
            r'cos\((.+)\)': ('u = {}', '-sin(u) du'),
            r'e\^\((.+)\)': ('u = {}', 'e^u du'),
            r'1/\((.+)\)': ('u = {}', 'ln|u| du'),
        }

    def calculate_integral(self, expression: str, formulas: Dict = None, 
                         definite: Optional[Tuple[float, float]] = None) -> str:
        """
        Calculate the integral of a mathematical expression.

        Args:
            expression (str): Mathematical expression to integrate
            formulas (Dict, optional): Additional integration formulas
            definite (Tuple, optional): (lower_bound, upper_bound) for definite integral

        Returns:
            str: Integral expression or numerical value
        """
        try:
            # Clean and prepare expression
            expr = self._clean_expression(expression)

            # Calculate indefinite integral
            if definite is None:
                result = self._calculate_indefinite_integral(expr)
                return f"{result} + C"
            else:
                # Calculate definite integral
                a, b = definite
                indefinite = self._calculate_indefinite_integral(expr)

                # Evaluate at bounds
                upper_value = self._evaluate_at_point(indefinite, b)
                lower_value = self._evaluate_at_point(indefinite, a)

                return str(upper_value - lower_value)

        except Exception as e:
            return f"Error calculating integral: {str(e)}"

    def _clean_expression(self, expr: str) -> str:
        """Clean and normalize the expression."""
        # Remove spaces and normalize
        expr = re.sub(r'\s+', '', expr)
        expr = expr.replace('^', '**')
        expr = expr.replace('π', 'pi')

        return expr

    def _calculate_indefinite_integral(self, expr: str) -> str:
        """Calculate indefinite integral using various rules."""

        # Constant multiple rule
        const_match = re.search(r'^(\d+\.?\d*)\*(.+)$', expr)
        if const_match:
            constant = const_match.group(1)
            function = const_match.group(2)
            integral_result = self._calculate_indefinite_integral(function)
            return f"{constant}*({integral_result})"

        # Power rule: x^n
        power_match = re.search(r'^x\*\*(\d+\.?\d*)$', expr)
        if power_match:
            n = float(power_match.group(1))
            if n == -1:
                return 'ln|x|'
            else:
                new_power = n + 1
                return f"x**{new_power}/{new_power}"

        # Simple polynomial terms
        poly_match = re.search(r'^(\d*\.?\d*)\*?x(?:\*\*(\d+\.?\d*))?$', expr)
        if poly_match:
            coeff = float(poly_match.group(1)) if poly_match.group(1) else 1
            power = float(poly_match.group(2)) if poly_match.group(2) else 1

            if power == -1:
                return f"{coeff}*ln|x|" if coeff != 1 else "ln|x|"
            else:
                new_power = power + 1
                new_coeff = coeff / new_power
                if new_power == 1:
                    return f"{new_coeff}*x" if new_coeff != 1 else "x"
                else:
                    return f"{new_coeff}*x**{new_power}"

        # Trigonometric functions
        trig_integrals = {
            'sin(x)': '-cos(x)',
            'cos(x)': 'sin(x)',
            'tan(x)': '-ln|cos(x)|',
            'sec(x)**2': 'tan(x)',
            'csc(x)**2': '-cot(x)',
        }

        for pattern, integral in trig_integrals.items():
            if re.search(pattern.replace('(', '\\(').replace(')', '\\)').replace('**', '\\*\\*'), expr):
                return integral

        # Exponential functions
        if expr == 'e**x':
            return 'e**x'
        elif 'e**' in expr:
            exp_match = re.search(r'e\*\*([^+\-*/]+)', expr)
            if exp_match:
                exponent = exp_match.group(1)
                if exponent == 'x':
                    return 'e**x'
                else:
                    # More complex exponential - would need advanced techniques
                    return f"∫e**{exponent} dx"

        # Natural logarithm integration by parts
        if expr == 'ln(x)':
            return 'x*ln(x) - x'

        # Sum rule: handle addition and subtraction
        if '+' in expr or '-' in expr:
            return self._handle_sum_integral(expr)

        # If no rule applies, return symbolic form
        return f"∫{expr} dx"

    def _handle_sum_integral(self, expr: str) -> str:
        """Handle sum and difference using linearity of integrals."""
        # Split by + and - while preserving signs
        terms = re.split(r'([+\-])', expr)

        result_terms = []
        current_sign = '+'

        for i, term in enumerate(terms):
            if term in ['+', '-']:
                current_sign = term
            elif term.strip():
                term_integral = self._calculate_indefinite_integral(term.strip())
                if current_sign == '-' and not term_integral.startswith('-'):
                    term_integral = f"-{term_integral}"
                result_terms.append(term_integral)
                current_sign = '+'

        return ' + '.join(result_terms).replace('+ -', '- ')

    def _evaluate_at_point(self, expression: str, point: float) -> float:
        """Evaluate an expression at a specific point."""
        try:
            # Replace mathematical constants
            expression = expression.replace('pi', str(math.pi))
            expression = expression.replace('e', str(math.e))

            # Replace x with the point value
            expression = expression.replace('x', str(point))
            expression = expression.replace('**', '^')

            # Handle special functions
            expression = self._replace_special_functions(expression, point)

            # Safely evaluate (simplified version)
            return self._safe_numerical_eval(expression)

        except Exception as e:
            raise ValueError(f"Could not evaluate at point {point}: {str(e)}")

    def _replace_special_functions(self, expr: str, x_val: float) -> str:
        """Replace special functions with their numerical values."""
        replacements = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'ln': math.log,
            'log': math.log10,
            'sqrt': math.sqrt,
        }

        for func, math_func in replacements.items():
            # Simple function call pattern
            pattern = f'{func}\\(([^)]+)\\)'
            while re.search(pattern, expr):
                match = re.search(pattern, expr)
                if match:
                    arg = float(match.group(1))
                    value = math_func(arg)
                    expr = expr.replace(match.group(0), str(value))

        return expr

    def _safe_numerical_eval(self, expr: str) -> float:
        """Safely evaluate a numerical expression."""
        # Replace ^ with ** for Python
        expr = expr.replace('^', '**')

        # Create safe namespace
        safe_dict = {
            '__builtins__': {},
            'pi': math.pi,
            'e': math.e,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'ln': math.log,
            'log': math.log10,
            'sqrt': math.sqrt,
            'abs': abs,
        }

        try:
            return float(eval(expr, safe_dict))
        except:
            return 0.0  # Fallback value

    def numerical_integration_simpson(self, expression: str, a: float, b: float, n: int = 1000) -> float:
        """
        Calculate definite integral using Simpson's rule for numerical integration.

        Args:
            expression (str): Function to integrate
            a (float): Lower bound
            b (float): Upper bound  
            n (int): Number of intervals (must be even)

        Returns:
            float: Approximate integral value
        """
        if n % 2 != 0:
            n += 1  # Make n even

        h = (b - a) / n

        # Calculate sum using Simpson's rule
        integral_sum = 0

        # Evaluate function at endpoints and interior points
        for i in range(n + 1):
            x = a + i * h
            fx = self._evaluate_function_at_point(expression, x)

            if i == 0 or i == n:
                integral_sum += fx
            elif i % 2 == 1:
                integral_sum += 4 * fx
            else:
                integral_sum += 2 * fx

        return (h / 3) * integral_sum

    def _evaluate_function_at_point(self, expression: str, point: float) -> float:
        """Evaluate the original function at a specific point."""
        expr = expression.replace('x', str(point))
        expr = expr.replace('**', '^')
        expr = self._replace_special_functions(expr, point)
        return self._safe_numerical_eval(expr)

    def get_integration_rules(self) -> Dict[str, str]:
        """Get all available integration rules."""
        return self.basic_integrals.copy()

    def explain_integration_step(self, expression: str) -> List[str]:
        """Provide step-by-step explanation of integration."""
        steps = []
        steps.append(f"Original expression: ∫{expression} dx")

        # Determine which rule applies
        if re.search(r'x\*\*\d+', expression):
            steps.append("Applying power rule: ∫x^n dx = x^(n+1)/(n+1) + C")
        elif 'sin' in expression or 'cos' in expression:
            steps.append("Applying trigonometric integration rule")
        elif 'e**x' in expression:
            steps.append("Applying exponential integration rule")
        elif '+' in expression or '-' in expression:
            steps.append("Applying linearity of integration")
        else:
            steps.append("Applying general integration techniques")

        result = self.calculate_integral(expression)
        steps.append(f"Result: {result}")

        return steps

    def integration_by_parts(self, u: str, dv: str) -> str:
        """
        Apply integration by parts: ∫u dv = uv - ∫v du

        Args:
            u (str): u function
            dv (str): dv function

        Returns:
            str: Result of integration by parts
        """
        # This is a simplified implementation
        # In practice, this would need more sophisticated symbolic manipulation
        return f"∫{u}*{dv} dx = {u}*∫{dv} dx - ∫(d/dx[{u}])*(∫{dv} dx) dx"


# Example usage and testing
if __name__ == "__main__":
    engine = IntegralEngine()

    test_expressions = [
        "x**2",
        "2*x + 3", 
        "sin(x)",
        "cos(x)",
        "e**x",
        "1/x"
    ]

    print("🧪 Testing Integral Engine")
    print("-" * 40)

    for expr in test_expressions:
        integral = engine.calculate_integral(expr)
        print(f"∫{expr} dx = {integral}")
        print()
