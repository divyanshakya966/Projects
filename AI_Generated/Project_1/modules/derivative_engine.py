"""
Derivative Engine - Advanced Derivative Calculation Module

This module implements symbolic differentiation using various rules
including power rule, product rule, quotient rule, and chain rule.
"""

import re
import math
from typing import Dict, List, Optional, Union


class DerivativeEngine:
    """Advanced engine for calculating symbolic derivatives."""

    def __init__(self):
        """Initialize derivative rules and patterns."""
        self.basic_derivatives = {
            'c': '0',  # Constant rule
            'x': '1',  # Variable rule
            'x^n': 'n*x^(n-1)',  # Power rule
            'sin(x)': 'cos(x)',
            'cos(x)': '-sin(x)', 
            'tan(x)': 'sec²(x)',
            'ln(x)': '1/x',
            'e^x': 'e^x',
            'log(x)': '1/(x*ln(10))',
            'sqrt(x)': '1/(2*sqrt(x))',
            'abs(x)': 'x/abs(x)',
        }

        self.trigonometric_derivatives = {
            'sin': 'cos',
            'cos': '-sin', 
            'tan': 'sec²',
            'csc': '-csc*cot',
            'sec': 'sec*tan',
            'cot': '-csc²',
            'asin': '1/sqrt(1-x²)',
            'acos': '-1/sqrt(1-x²)',
            'atan': '1/(1+x²)',
        }

    def calculate_derivative(self, expression: str, formulas: Dict = None) -> str:
        """
        Calculate the derivative of a mathematical expression.

        Args:
            expression (str): Mathematical expression to differentiate
            formulas (Dict, optional): Additional derivative formulas

        Returns:
            str: Derivative expression
        """
        try:
            # Clean and prepare expression
            expr = self._clean_expression(expression)

            # Handle special cases
            if self._is_constant(expr):
                return '0'

            if expr == 'x':
                return '1'

            # Apply derivative rules
            result = self._apply_derivative_rules(expr)

            # Simplify result
            result = self._simplify_expression(result)

            return result

        except Exception as e:
            return f"Error calculating derivative: {str(e)}"

    def _clean_expression(self, expr: str) -> str:
        """Clean and normalize the expression."""
        # Remove spaces
        expr = re.sub(r'\s+', '', expr)

        # Replace common symbols
        expr = expr.replace('^', '**')
        expr = expr.replace('π', 'pi')

        return expr

    def _is_constant(self, expr: str) -> bool:
        """Check if expression is a constant."""
        # If no 'x' and can be evaluated as number, it's constant
        if 'x' not in expr:
            try:
                float(expr.replace('pi', str(math.pi)).replace('e', str(math.e)))
                return True
            except:
                pass
        return False

    def _apply_derivative_rules(self, expr: str) -> str:
        """Apply appropriate derivative rules."""

        # Power rule: x^n
        power_match = re.search(r'x\*\*(\d+\.?\d*)', expr)
        if power_match:
            n = float(power_match.group(1))
            if n == 1:
                return '1'
            elif n == 0:
                return '0'
            else:
                new_power = n - 1
                if new_power == 1:
                    return f"{n}"
                else:
                    return f"{n}*x**{new_power}"

        # Simple polynomial terms
        poly_match = re.search(r'(\d*\.?\d*)\*?x(?:\*\*(\d+\.?\d*))?', expr)
        if poly_match:
            coeff = poly_match.group(1) or '1'
            power = float(poly_match.group(2)) if poly_match.group(2) else 1

            if power == 0:
                return '0'
            elif power == 1:
                return coeff if coeff != '1' else '1'
            else:
                new_coeff = float(coeff) * power
                new_power = power - 1
                if new_power == 1:
                    return f"{new_coeff}*x" if new_coeff != 1 else "x"
                else:
                    return f"{new_coeff}*x**{new_power}"

        # Trigonometric functions
        for func, derivative in self.trigonometric_derivatives.items():
            pattern = f'{func}\\(([^)]+)\\)'
            match = re.search(pattern, expr)
            if match:
                inner = match.group(1)
                inner_derivative = self._apply_derivative_rules(inner) if inner != 'x' else '1'

                if derivative.startswith('-'):
                    return f"-{derivative[1:]}({inner})" + (f"*{inner_derivative}" if inner_derivative != '1' else "")
                else:
                    return f"{derivative}({inner})" + (f"*{inner_derivative}" if inner_derivative != '1' else "")

        # Exponential functions
        if 'e**' in expr:
            exp_match = re.search(r'e\*\*([^+\-*/]+)', expr)
            if exp_match:
                exponent = exp_match.group(1)
                if exponent == 'x':
                    return 'e**x'
                else:
                    exp_derivative = self._apply_derivative_rules(exponent)
                    return f"e**{exponent}*{exp_derivative}"

        # Natural logarithm
        if 'ln(' in expr or 'log(' in expr:
            log_match = re.search(r'ln\(([^)]+)\)', expr)
            if log_match:
                inner = log_match.group(1)
                if inner == 'x':
                    return '1/x'
                else:
                    inner_derivative = self._apply_derivative_rules(inner)
                    return f"({inner_derivative})/({inner})"

        # Sum rule: handle addition and subtraction
        if '+' in expr or '-' in expr:
            return self._handle_sum_difference(expr)

        # Product rule: handle multiplication
        if '*' in expr:
            return self._handle_product_rule(expr)

        # If no rule applies, return original expression
        return f"d/dx[{expr}]"

    def _handle_sum_difference(self, expr: str) -> str:
        """Handle sum and difference using linearity of derivatives."""
        # Split by + and - while preserving signs
        terms = re.split(r'([+\-])', expr)

        result_terms = []
        current_sign = '+'

        for i, term in enumerate(terms):
            if term in ['+', '-']:
                current_sign = term
            elif term.strip():
                term_derivative = self._apply_derivative_rules(term.strip())
                if current_sign == '-' and not term_derivative.startswith('-'):
                    term_derivative = f"-{term_derivative}"
                result_terms.append(term_derivative)
                current_sign = '+'

        return ' + '.join(result_terms).replace('+ -', '- ')

    def _handle_product_rule(self, expr: str) -> str:
        """Handle product rule: (fg)' = f'g + fg'."""
        # Simple implementation for basic products
        factors = expr.split('*')

        if len(factors) == 2:
            f, g = factors
            f_prime = self._apply_derivative_rules(f)
            g_prime = self._apply_derivative_rules(g)

            return f"({f_prime})*({g}) + ({f})*({g_prime})"

        # For more complex products, return symbolic form
        return f"d/dx[{expr}]"

    def _simplify_expression(self, expr: str) -> str:
        """Simplify the derivative expression."""

        # Remove unnecessary parentheses and clean up
        expr = re.sub(r'\(1\)\*', '', expr)  # Remove (1)*
        expr = re.sub(r'\*1(?![\d.])', '', expr)  # Remove *1
        expr = re.sub(r'\b1\*', '', expr)  # Remove 1*
        expr = expr.replace('*1', '')
        expr = expr.replace('+ 0', '')
        expr = expr.replace('0 +', '')
        expr = expr.replace('+-', '-')

        # Clean up extra spaces
        expr = re.sub(r'\s+', ' ', expr).strip()

        return expr

    def get_derivative_rules(self) -> Dict[str, str]:
        """Get all available derivative rules."""
        all_rules = {}
        all_rules.update(self.basic_derivatives)
        all_rules.update({f"{k}(x)": v for k, v in self.trigonometric_derivatives.items()})

        return all_rules

    def explain_derivative_step(self, expression: str) -> List[str]:
        """Provide step-by-step explanation of derivative calculation."""
        steps = []
        steps.append(f"Original expression: {expression}")

        # Determine which rule applies
        if self._is_constant(expression):
            steps.append("Applying constant rule: d/dx[c] = 0")
        elif expression == 'x':
            steps.append("Applying variable rule: d/dx[x] = 1")
        elif re.search(r'x\*\*\d+', expression):
            steps.append("Applying power rule: d/dx[x^n] = n*x^(n-1)")
        elif any(trig in expression for trig in self.trigonometric_derivatives):
            steps.append("Applying trigonometric derivative rule")
        else:
            steps.append("Applying general differentiation rules")

        result = self.calculate_derivative(expression)
        steps.append(f"Result: {result}")

        return steps


# Example usage and testing
if __name__ == "__main__":
    engine = DerivativeEngine()

    test_expressions = [
        "x**2",
        "3*x**2 + 2*x + 1",
        "sin(x)",
        "cos(x)*x",
        "ln(x)",
        "e**x"
    ]

    print("🧪 Testing Derivative Engine")
    print("-" * 40)

    for expr in test_expressions:
        derivative = engine.calculate_derivative(expr)
        print(f"f(x) = {expr}")
        print(f"f'(x) = {derivative}")
        print()
