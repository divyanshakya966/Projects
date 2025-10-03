"""
Parser Module - Mathematical Expression Parser

This module provides advanced parsing capabilities for mathematical
expressions including tokenization, syntax analysis, and AST generation.
"""

import re
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum


class TokenType(Enum):
    """Enumeration of different token types in mathematical expressions."""
    NUMBER = "NUMBER"
    VARIABLE = "VARIABLE"
    OPERATOR = "OPERATOR"
    FUNCTION = "FUNCTION"
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    COMMA = "COMMA"
    CONSTANT = "CONSTANT"
    EOF = "EOF"


class Token:
    """Represents a token in a mathematical expression."""

    def __init__(self, token_type: TokenType, value: str, position: int = 0):
        self.type = token_type
        self.value = value
        self.position = position

    def __repr__(self):
        return f"Token({self.type}, '{self.value}', {self.position})"


class MathParser:
    """Mathematical expression parser with tokenization and syntax analysis."""

    def __init__(self):
        """Initialize the parser with operator precedence and function definitions."""
        self.operators = {
            '+': {'precedence': 1, 'associativity': 'left'},
            '-': {'precedence': 1, 'associativity': 'left'},
            '*': {'precedence': 2, 'associativity': 'left'},
            '/': {'precedence': 2, 'associativity': 'left'},
            '^': {'precedence': 3, 'associativity': 'right'},
            '**': {'precedence': 3, 'associativity': 'right'},
        }

        self.functions = {
            'sin', 'cos', 'tan', 'asin', 'acos', 'atan',
            'sinh', 'cosh', 'tanh', 'ln', 'log', 'exp',
            'sqrt', 'abs', 'floor', 'ceil', 'round',
            'derivative', 'integral', 'diff', 'int'
        }

        self.constants = {
            'pi', 'e', 'phi', 'gamma', 'inf', 'nan'
        }

    def tokenize(self, expression: str) -> List[Token]:
        """
        Tokenize a mathematical expression into a list of tokens.

        Args:
            expression (str): Mathematical expression to tokenize

        Returns:
            List[Token]: List of tokens representing the expression
        """
        tokens = []
        position = 0

        # Clean expression
        expression = expression.replace(' ', '')

        while position < len(expression):
            char = expression[position]

            # Numbers (including decimals and scientific notation)
            if char.isdigit() or char == '.':
                number, new_pos = self._parse_number(expression, position)
                tokens.append(Token(TokenType.NUMBER, number, position))
                position = new_pos
                continue

            # Variables and functions/constants
            if char.isalpha():
                identifier, new_pos = self._parse_identifier(expression, position)

                if identifier in self.functions:
                    tokens.append(Token(TokenType.FUNCTION, identifier, position))
                elif identifier in self.constants:
                    tokens.append(Token(TokenType.CONSTANT, identifier, position))
                else:
                    tokens.append(Token(TokenType.VARIABLE, identifier, position))

                position = new_pos
                continue

            # Operators
            if char in '+-*/^':
                # Check for ** operator
                if char == '*' and position + 1 < len(expression) and expression[position + 1] == '*':
                    tokens.append(Token(TokenType.OPERATOR, '**', position))
                    position += 2
                else:
                    tokens.append(Token(TokenType.OPERATOR, char, position))
                    position += 1
                continue

            # Parentheses
            if char == '(':
                tokens.append(Token(TokenType.LEFT_PAREN, char, position))
                position += 1
                continue

            if char == ')':
                tokens.append(Token(TokenType.RIGHT_PAREN, char, position))
                position += 1
                continue

            # Comma
            if char == ',':
                tokens.append(Token(TokenType.COMMA, char, position))
                position += 1
                continue

            # Skip unknown characters or handle special symbols
            position += 1

        # Add EOF token
        tokens.append(Token(TokenType.EOF, '', position))

        return tokens

    def _parse_number(self, expression: str, start: int) -> Tuple[str, int]:
        """Parse a number from the expression starting at the given position."""
        end = start
        has_decimal = False

        while end < len(expression):
            char = expression[end]

            if char.isdigit():
                end += 1
            elif char == '.' and not has_decimal:
                has_decimal = True
                end += 1
            elif char.lower() == 'e' and end + 1 < len(expression):
                # Scientific notation
                end += 1
                if end < len(expression) and expression[end] in '+-':
                    end += 1
                while end < len(expression) and expression[end].isdigit():
                    end += 1
                break
            else:
                break

        return expression[start:end], end

    def _parse_identifier(self, expression: str, start: int) -> Tuple[str, int]:
        """Parse an identifier (variable, function, or constant) from the expression."""
        end = start

        while end < len(expression) and (expression[end].isalnum() or expression[end] == '_'):
            end += 1

        return expression[start:end], end

    def parse_to_postfix(self, tokens: List[Token]) -> List[Token]:
        """
        Convert infix tokens to postfix notation using the Shunting Yard algorithm.

        Args:
            tokens (List[Token]): List of infix tokens

        Returns:
            List[Token]: List of tokens in postfix notation
        """
        output = []
        operator_stack = []

        for token in tokens:
            if token.type == TokenType.EOF:
                break

            if token.type in [TokenType.NUMBER, TokenType.VARIABLE, TokenType.CONSTANT]:
                output.append(token)

            elif token.type == TokenType.FUNCTION:
                operator_stack.append(token)

            elif token.type == TokenType.COMMA:
                # Pop operators until left parenthesis
                while (operator_stack and 
                       operator_stack[-1].type != TokenType.LEFT_PAREN):
                    output.append(operator_stack.pop())

            elif token.type == TokenType.OPERATOR:
                while (operator_stack and
                       operator_stack[-1].type == TokenType.OPERATOR and
                       self._has_higher_precedence(operator_stack[-1], token)):
                    output.append(operator_stack.pop())
                operator_stack.append(token)

            elif token.type == TokenType.LEFT_PAREN:
                operator_stack.append(token)

            elif token.type == TokenType.RIGHT_PAREN:
                # Pop operators until left parenthesis
                while (operator_stack and 
                       operator_stack[-1].type != TokenType.LEFT_PAREN):
                    output.append(operator_stack.pop())

                # Remove left parenthesis
                if operator_stack:
                    operator_stack.pop()

                # If there's a function on top, add it to output
                if (operator_stack and 
                    operator_stack[-1].type == TokenType.FUNCTION):
                    output.append(operator_stack.pop())

        # Pop remaining operators
        while operator_stack:
            output.append(operator_stack.pop())

        return output

    def _has_higher_precedence(self, op1: Token, op2: Token) -> bool:
        """Check if op1 has higher or equal precedence than op2."""
        if op1.value not in self.operators or op2.value not in self.operators:
            return False

        prec1 = self.operators[op1.value]['precedence']
        prec2 = self.operators[op2.value]['precedence']
        assoc2 = self.operators[op2.value]['associativity']

        return prec1 > prec2 or (prec1 == prec2 and assoc2 == 'left')

    def validate_syntax(self, tokens: List[Token]) -> Tuple[bool, str]:
        """
        Validate the syntax of tokenized expression.

        Args:
            tokens (List[Token]): List of tokens to validate

        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not tokens or tokens[0].type == TokenType.EOF:
            return False, "Empty expression"

        paren_count = 0
        prev_token = None

        for token in tokens:
            if token.type == TokenType.EOF:
                break

            # Check parentheses balance
            if token.type == TokenType.LEFT_PAREN:
                paren_count += 1
            elif token.type == TokenType.RIGHT_PAREN:
                paren_count -= 1
                if paren_count < 0:
                    return False, f"Unmatched closing parenthesis at position {token.position}"

            # Check for consecutive operators
            if (prev_token and 
                prev_token.type == TokenType.OPERATOR and 
                token.type == TokenType.OPERATOR):
                return False, f"Consecutive operators at position {token.position}"

            # Check function calls
            if (token.type == TokenType.FUNCTION and 
                prev_token and 
                prev_token.type not in [TokenType.OPERATOR, TokenType.LEFT_PAREN, TokenType.COMMA]):
                return False, f"Invalid function call at position {token.position}"

            prev_token = token

        # Check final parentheses balance
        if paren_count != 0:
            return False, "Unmatched parentheses"

        # Check if expression ends properly
        if prev_token and prev_token.type == TokenType.OPERATOR:
            return False, "Expression cannot end with an operator"

        return True, ""

    def parse_expression(self, expression: str) -> Dict[str, Any]:
        """
        Parse a complete mathematical expression.

        Args:
            expression (str): Expression to parse

        Returns:
            Dict containing parsing results
        """
        try:
            # Tokenize
            tokens = self.tokenize(expression)

            # Validate syntax
            is_valid, error = self.validate_syntax(tokens)
            if not is_valid:
                return {
                    'success': False,
                    'error': error,
                    'tokens': tokens
                }

            # Convert to postfix
            postfix_tokens = self.parse_to_postfix(tokens)

            return {
                'success': True,
                'tokens': tokens,
                'postfix': postfix_tokens,
                'expression': expression
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'expression': expression
            }


# Example usage and testing
if __name__ == "__main__":
    parser = MathParser()

    test_expressions = [
        "2 + 3 * 4",
        "sin(x) + cos(y)",
        "d/dx[x^2 + 3x + 1]",
        "integral(2*x + 5)",
        "(a + b) * (c - d)",
        "sqrt(16) + ln(e)",
    ]

    print("🧪 Testing Mathematical Parser")
    print("-" * 40)

    for expr in test_expressions:
        print(f"\nExpression: {expr}")
        result = parser.parse_expression(expr)

        if result['success']:
            print("✅ Parsing successful")
            print(f"Tokens: {len(result['tokens']) - 1}")  # -1 for EOF
            print(f"Postfix length: {len(result['postfix'])}")
        else:
            print(f"❌ Error: {result['error']}")
