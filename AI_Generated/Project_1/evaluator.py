"""
Evaluator Module - Mathematical Expression Evaluator

This module provides evaluation capabilities for parsed mathematical
expressions using various computation strategies.
"""

from typing import List, Dict, Any, Union, Optional
from parser import Token, TokenType, MathParser
import math


class MathEvaluator:
    """Mathematical expression evaluator for parsed expressions."""

    def __init__(self):
        """Initialize evaluator with mathematical functions and constants."""
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
            'exp': math.exp,
            'sqrt': math.sqrt,
            'abs': abs,
            'floor': math.floor,
            'ceil': math.ceil,
            'round': round,
        }

        self.constants = {
            'pi': math.pi,
            'e': math.e,
            'phi': (1 + math.sqrt(5)) / 2,
            'gamma': 0.5772156649015329,
            'inf': float('inf'),
            'nan': float('nan'),
        }

        self.operators = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y,
            '^': lambda x, y: x ** y,
            '**': lambda x, y: x ** y,
        }

    def evaluate_postfix(self, postfix_tokens: List[Token], 
                        variables: Optional[Dict[str, float]] = None) -> Union[float, int, complex]:
        """
        Evaluate postfix expression tokens.

        Args:
            postfix_tokens (List[Token]): Postfix notation tokens
            variables (Dict, optional): Variable values

        Returns:
            Numerical result of evaluation
        """
        if variables is None:
            variables = {}

        stack = []

        for token in postfix_tokens:
            if token.type == TokenType.NUMBER:
                stack.append(float(token.value))

            elif token.type == TokenType.VARIABLE:
                if token.value in variables:
                    stack.append(variables[token.value])
                else:
                    raise ValueError(f"Undefined variable: {token.value}")

            elif token.type == TokenType.CONSTANT:
                if token.value in self.constants:
                    stack.append(self.constants[token.value])
                else:
                    raise ValueError(f"Unknown constant: {token.value}")

            elif token.type == TokenType.OPERATOR:
                if len(stack) < 2:
                    raise ValueError(f"Insufficient operands for operator {token.value}")

                b = stack.pop()
                a = stack.pop()

                if token.value in self.operators:
                    result = self.operators[token.value](a, b)
                    stack.append(result)
                else:
                    raise ValueError(f"Unknown operator: {token.value}")

            elif token.type == TokenType.FUNCTION:
                if token.value in self.functions:
                    func = self.functions[token.value]

                    # Determine number of arguments (simplified approach)
                    if token.value in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan',
                                     'sinh', 'cosh', 'tanh', 'ln', 'log', 'exp',
                                     'sqrt', 'abs', 'floor', 'ceil', 'round']:
                        if len(stack) < 1:
                            raise ValueError(f"Insufficient arguments for function {token.value}")
                        arg = stack.pop()
                        result = func(arg)
                        stack.append(result)
                    else:
                        # Handle multi-argument functions if needed
                        pass
                else:
                    raise ValueError(f"Unknown function: {token.value}")

        if len(stack) != 1:
            raise ValueError("Invalid expression: incorrect number of values remaining")

        return stack[0]

    def evaluate_expression(self, expression: str, 
                          variables: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """
        Evaluate a complete mathematical expression.

        Args:
            expression (str): Mathematical expression
            variables (Dict, optional): Variable values

        Returns:
            Dict containing evaluation results
        """
        try:
            parser = MathParser()

            # Parse expression
            parse_result = parser.parse_expression(expression)

            if not parse_result['success']:
                return {
                    'success': False,
                    'error': parse_result['error'],
                    'expression': expression
                }

            # Evaluate postfix tokens
            result = self.evaluate_postfix(parse_result['postfix'], variables)

            return {
                'success': True,
                'result': result,
                'expression': expression,
                'tokens': len(parse_result['tokens']) - 1  # -1 for EOF
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'expression': expression
            }

    def evaluate_with_steps(self, expression: str,
                           variables: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """
        Evaluate expression and provide step-by-step breakdown.

        Args:
            expression (str): Mathematical expression
            variables (Dict, optional): Variable values

        Returns:
            Dict containing evaluation results with steps
        """
        steps = []
        steps.append(f"Original expression: {expression}")

        try:
            # Substitute variables if provided
            if variables:
                substituted_expr = expression
                for var, value in variables.items():
                    substituted_expr = substituted_expr.replace(var, str(value))
                steps.append(f"After substitution: {substituted_expr}")

            # Evaluate
            eval_result = self.evaluate_expression(expression, variables)

            if eval_result['success']:
                steps.append(f"Final result: {eval_result['result']}")

                return {
                    'success': True,
                    'result': eval_result['result'],
                    'steps': steps,
                    'expression': expression
                }
            else:
                return {
                    'success': False,
                    'error': eval_result['error'],
                    'steps': steps,
                    'expression': expression
                }

        except Exception as e:
            steps.append(f"Error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'steps': steps,
                'expression': expression
            }


# Example usage and testing
if __name__ == "__main__":
    evaluator = MathEvaluator()

    test_cases = [
        ("2 + 3 * 4", {}),
        ("sin(pi/2) + cos(0)", {}),
        ("sqrt(16) + 2^3", {}),
        ("x^2 + 3*x + 1", {"x": 2}),
        ("ln(e) + log(100)", {}),
    ]

    print("🧪 Testing Mathematical Evaluator")
    print("-" * 40)

    for expression, variables in test_cases:
        print(f"\nExpression: {expression}")
        if variables:
            print(f"Variables: {variables}")

        result = evaluator.evaluate_with_steps(expression, variables)

        if result['success']:
            print("✅ Evaluation successful")
            print(f"Result: {result['result']}")
            print("Steps:")
            for i, step in enumerate(result['steps'], 1):
                print(f"  {i}. {step}")
        else:
            print(f"❌ Error: {result['error']}")
