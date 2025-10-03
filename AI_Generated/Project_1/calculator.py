#!/usr/bin/env python3
"""
Calculus Calculator - Main Application Entry Point

A comprehensive calculus calculator that handles derivatives, integrals, 
and basic mathematical operations with high efficiency and accuracy.

Author: Divyansh Shakya
Version: 1.0.0
License: MIT
"""

import sys
import os
from typing import Optional, Dict, Any

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from switch import CalculusRouter
from utils import CalculatorUtils
from modules.basic_math import BasicMathOperations
from modules.formula_loader import FormulaLoader


class CalculusCalculator:
    """Main calculator class that orchestrates all mathematical operations."""

    def __init__(self):
        """Initialize the calculator with all necessary components."""
        self.router = CalculusRouter()
        self.utils = CalculatorUtils()
        self.basic_math = BasicMathOperations()
        self.formula_loader = FormulaLoader()

        # Load formulas at startup
        self._load_formulas()

    def _load_formulas(self) -> None:
        """Load all mathematical formulas and rules."""
        try:
            self.formulas = self.formula_loader.load_all_formulas()
            print("✅ Formulas loaded successfully")
        except Exception as e:
            print(f"⚠️  Warning: Could not load formulas - {e}")
            self.formulas = {}

    def calculate(self, expression: str, operation_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Main calculation method that processes any mathematical expression.

        Args:
            expression (str): The mathematical expression to evaluate
            operation_type (str, optional): Force specific operation type

        Returns:
            Dict containing result, steps, and metadata
        """
        try:
            # Clean and validate input
            expression = self.utils.clean_expression(expression)

            if not expression:
                return {"error": "Empty expression provided"}

            # Determine operation type
            if not operation_type:
                operation_type = self.router.determine_operation(expression)

            # Route to appropriate calculation method
            result = self.router.route_calculation(expression, operation_type, self.formulas)

            return {
                "expression": expression,
                "operation_type": operation_type,
                "result": result,
                "success": True
            }

        except Exception as e:
            return {
                "error": str(e),
                "expression": expression,
                "success": False
            }

    def interactive_mode(self) -> None:
        """Run the calculator in interactive command-line mode."""
        print("=" * 60)
        print("🧮 ADVANCED CALCULUS CALCULATOR")
        print("=" * 60)
        print("Supported Operations:")
        print("• Derivatives: d/dx[expression], derivative(expression)")
        print("• Integrals: ∫[expression]dx, integral(expression)")
        print("• Basic Math: +, -, *, /, ^, sqrt(), ln(), sin(), cos(), etc.")
        print("• Type 'help' for more commands, 'quit' to exit")
        print("-" * 60)

        while True:
            try:
                user_input = input("\n📝 Enter expression: ").strip()

                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Thank you for using Calculus Calculator!")
                    break
                elif user_input.lower() == 'help':
                    self._show_help()
                    continue
                elif user_input.lower() == 'examples':
                    self._show_examples()
                    continue

                # Calculate result
                result = self.calculate(user_input)

                # Display result
                self._display_result(result)

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

    def _display_result(self, result: Dict[str, Any]) -> None:
        """Display calculation results in a formatted way."""
        if result.get("success"):
            print(f"\n✅ Result:")
            print(f"   Expression: {result['expression']}")
            print(f"   Type: {result['operation_type']}")
            print(f"   Answer: {result['result']}")
        else:
            print(f"\n❌ Error: {result.get('error', 'Unknown error')}")

    def _show_help(self) -> None:
        """Display help information."""
        help_text = """
🆘 HELP - Calculator Commands and Syntax

DERIVATIVE OPERATIONS:
• d/dx[x^2 + 3x]        - Find derivative of polynomial
• derivative(sin(x))    - Find derivative of trigonometric function
• diff(ln(x), x)        - Differentiate natural log

INTEGRAL OPERATIONS:
• integral(x^2)         - Find indefinite integral
• ∫[2x + 1]dx          - Integration notation
• definite(x^2, 0, 5)   - Definite integral from 0 to 5

BASIC MATHEMATICS:
• 2 + 3 * 4            - Basic arithmetic
• sqrt(16)             - Square root
• sin(pi/2)            - Trigonometric functions
• ln(e)                - Natural logarithm
• 2^3                  - Exponentiation

SPECIAL COMMANDS:
• help                 - Show this help
• examples             - Show example calculations  
• quit/exit/q          - Exit calculator

VARIABLES:
• Use 'x' as the main variable for calculus operations
• Constants: pi, e, inf (infinity)
        """
        print(help_text)

    def _show_examples(self) -> None:
        """Display example calculations."""
        examples = [
            "d/dx[x^3 + 2x^2 + x + 1]",
            "integral(2x + 5)",
            "derivative(sin(x)*cos(x))",
            "sqrt(144) + 2^3",
            "ln(e^2)",
            "sin(pi/2) + cos(0)"
        ]

        print("\n📚 Example Calculations:")
        for i, example in enumerate(examples, 1):
            print(f"   {i}. {example}")
            result = self.calculate(example)
            if result.get("success"):
                print(f"      → {result['result']}")
            else:
                print(f"      → Error: {result.get('error')}")
            print()


def main():
    """Main entry point of the application."""
    calculator = CalculusCalculator()

    # Check if arguments provided for command-line usage
    if len(sys.argv) > 1:
        expression = " ".join(sys.argv[1:])
        result = calculator.calculate(expression)
        calculator._display_result(result)
    else:
        # Run in interactive mode
        calculator.interactive_mode()


if __name__ == "__main__":
    main()
