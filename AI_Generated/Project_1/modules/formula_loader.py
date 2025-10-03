"""
Formula Loader Module - Mathematical Formula Management

This module handles loading, parsing, and managing mathematical formulas
from text files including derivatives, integrals, and general formulas.
"""

import os
import re
from typing import Dict, List, Optional, Tuple, Any
import json


class FormulaLoader:
    """Class for loading and managing mathematical formulas from files."""

    def __init__(self, data_directory: str = 'data'):
        """
        Initialize the formula loader.

        Args:
            data_directory (str): Directory containing formula files
        """
        self.data_dir = data_directory
        self.formulas = {
            'derivatives': {},
            'integrals': {},
            'algebraic': {},
            'trigonometric': {},
            'logarithmic': {},
            'exponential': {},
            'constants': {}
        }

        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)

    def load_all_formulas(self) -> Dict[str, Any]:
        """
        Load all mathematical formulas from files.

        Returns:
            Dict containing all loaded formulas organized by type
        """
        try:
            # Load each type of formula
            self._load_derivatives()
            self._load_integrals()
            self._load_general_formulas()
            self._load_constants()

            return self.formulas.copy()

        except Exception as e:
            print(f"Error loading formulas: {str(e)}")
            return self.formulas

    def _load_derivatives(self) -> None:
        """Load derivative formulas from derivatives.txt."""
        file_path = os.path.join(self.data_dir, 'derivatives.txt')

        if not os.path.exists(file_path):
            self._create_derivatives_file(file_path)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            derivatives = self._parse_formula_file(content, 'derivative')
            self.formulas['derivatives'].update(derivatives)

        except Exception as e:
            print(f"Error loading derivatives: {str(e)}")

    def _load_integrals(self) -> None:
        """Load integral formulas from integrals.txt.""" 
        file_path = os.path.join(self.data_dir, 'integrals.txt')

        if not os.path.exists(file_path):
            self._create_integrals_file(file_path)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            integrals = self._parse_formula_file(content, 'integral')
            self.formulas['integrals'].update(integrals)

        except Exception as e:
            print(f"Error loading integrals: {str(e)}")

    def _load_general_formulas(self) -> None:
        """Load general formulas from formulas.txt."""
        file_path = os.path.join(self.data_dir, 'formulas.txt')

        if not os.path.exists(file_path):
            self._create_general_formulas_file(file_path)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse different sections
            sections = self._split_formula_sections(content)

            for section_name, section_content in sections.items():
                formulas = self._parse_formula_file(section_content, section_name)
                if section_name in self.formulas:
                    self.formulas[section_name].update(formulas)
                else:
                    self.formulas[section_name] = formulas

        except Exception as e:
            print(f"Error loading general formulas: {str(e)}")

    def _load_constants(self) -> None:
        """Load mathematical constants from constants.txt."""
        file_path = os.path.join(self.data_dir, 'constants.txt')

        if not os.path.exists(file_path):
            self._create_constants_file(file_path)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            constants = self._parse_constants_file(content)
            self.formulas['constants'].update(constants)

        except Exception as e:
            print(f"Error loading constants: {str(e)}")

    def _parse_formula_file(self, content: str, formula_type: str) -> Dict[str, str]:
        """
        Parse formula file content.

        Args:
            content (str): File content
            formula_type (str): Type of formulas

        Returns:
            Dict mapping expressions to their formulas
        """
        formulas = {}

        # Split into lines and process each line
        lines = content.split('\n')

        for line in lines:
            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith('#') or line.startswith('//'):
                continue

            # Parse formula line
            formula_data = self._parse_formula_line(line)
            if formula_data:
                expression, result = formula_data
                formulas[expression] = result

        return formulas

    def _parse_formula_line(self, line: str) -> Optional[Tuple[str, str]]:
        """
        Parse a single formula line.

        Args:
            line (str): Formula line to parse

        Returns:
            Tuple of (expression, result) or None
        """
        # Handle different formula formats
        formats = [
            r'^(.+?)\s*=\s*(.+)$',        # expression = result
            r'^(.+?)\s*->\s*(.+)$',       # expression -> result
            r'^(.+?)\s*:\s*(.+)$',        # expression : result
            r'^(.+?)\s*\|\s*(.+)$',      # expression | result
        ]

        for pattern in formats:
            match = re.match(pattern, line)
            if match:
                expression = match.group(1).strip()
                result = match.group(2).strip()
                return expression, result

        return None

    def _split_formula_sections(self, content: str) -> Dict[str, str]:
        """Split content into different formula sections."""
        sections = {}
        current_section = 'general'
        current_content = []

        lines = content.split('\n')

        for line in lines:
            line = line.strip()

            # Check for section headers
            if line.startswith('[') and line.endswith(']'):
                # Save previous section
                if current_content:
                    sections[current_section] = '\n'.join(current_content)

                # Start new section
                current_section = line[1:-1].lower()
                current_content = []
            else:
                current_content.append(line)

        # Save last section
        if current_content:
            sections[current_section] = '\n'.join(current_content)

        return sections

    def _parse_constants_file(self, content: str) -> Dict[str, float]:
        """Parse constants file content."""
        constants = {}

        lines = content.split('\n')

        for line in lines:
            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith('#') or line.startswith('//'):
                continue

            # Parse constant definition
            parts = re.split(r'\s*[=:]\s*', line, 1)
            if len(parts) == 2:
                name = parts[0].strip()
                try:
                    value = float(parts[1].strip())
                    constants[name] = value
                except ValueError:
                    # Handle special values
                    value_str = parts[1].strip().lower()
                    if value_str == 'pi':
                        constants[name] = 3.141592653589793
                    elif value_str == 'e':
                        constants[name] = 2.718281828459045
                    # Add more special cases as needed

        return constants

    def _create_derivatives_file(self, file_path: str) -> None:
        """Create a default derivatives.txt file.""" 
        derivatives_content = """# Derivative Formulas
# Format: function = derivative

# Basic Rules
c = 0
x = 1
x^n = n*x^(n-1)
1/x = -1/x^2

# Trigonometric Functions
sin(x) = cos(x)
cos(x) = -sin(x)
tan(x) = sec^2(x)
csc(x) = -csc(x)*cot(x)
sec(x) = sec(x)*tan(x)
cot(x) = -csc^2(x)

# Inverse Trigonometric Functions
asin(x) = 1/sqrt(1-x^2)
acos(x) = -1/sqrt(1-x^2)
atan(x) = 1/(1+x^2)

# Exponential and Logarithmic
e^x = e^x
a^x = a^x*ln(a)
ln(x) = 1/x
log_a(x) = 1/(x*ln(a))

# Hyperbolic Functions
sinh(x) = cosh(x)
cosh(x) = sinh(x)
tanh(x) = sech^2(x)
"""

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(derivatives_content)

    def _create_integrals_file(self, file_path: str) -> None:
        """Create a default integrals.txt file."""
        integrals_content = """# Integral Formulas
# Format: function = integral

# Basic Rules
1 = x
x = x^2/2
x^n = x^(n+1)/(n+1)
1/x = ln|x|

# Trigonometric Functions
sin(x) = -cos(x)
cos(x) = sin(x)
tan(x) = -ln|cos(x)|
sec^2(x) = tan(x)
csc^2(x) = -cot(x)
sec(x)*tan(x) = sec(x)
csc(x)*cot(x) = -csc(x)

# Exponential and Logarithmic
e^x = e^x
a^x = a^x/ln(a)
1/x = ln|x|
ln(x) = x*ln(x) - x

# Common Forms
1/sqrt(1-x^2) = arcsin(x)
1/(1+x^2) = arctan(x)
1/sqrt(x^2+a^2) = ln|x + sqrt(x^2+a^2)|
1/sqrt(a^2-x^2) = arcsin(x/a)

# Hyperbolic Functions
sinh(x) = cosh(x)
cosh(x) = sinh(x)
tanh(x) = ln|cosh(x)|
"""

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(integrals_content)

    def _create_general_formulas_file(self, file_path: str) -> None:
        """Create a default formulas.txt file."""
        formulas_content = """# General Mathematical Formulas

[Algebraic]
# Quadratic Formula
quadratic = (-b +/- sqrt(b^2 - 4ac)) / (2a)

# Binomial Theorem  
binomial = (a + b)^n = sum(C(n,k) * a^(n-k) * b^k, k=0 to n)

# Difference of Squares
difference_squares = a^2 - b^2 = (a+b)(a-b)

[Trigonometric]
# Pythagorean Identity
pythagorean = sin^2(x) + cos^2(x) = 1

# Angle Addition
sin_addition = sin(a + b) = sin(a)cos(b) + cos(a)sin(b)
cos_addition = cos(a + b) = cos(a)cos(b) - sin(a)sin(b)

# Double Angle
sin_double = sin(2x) = 2sin(x)cos(x)
cos_double = cos(2x) = cos^2(x) - sin^2(x)

[Logarithmic]
# Logarithm Properties
log_product = log(ab) = log(a) + log(b)
log_quotient = log(a/b) = log(a) - log(b)
log_power = log(a^n) = n*log(a)

# Change of Base
change_base = log_a(x) = ln(x)/ln(a)

[Exponential]
# Exponential Properties
exp_product = a^m * a^n = a^(m+n)
exp_quotient = a^m / a^n = a^(m-n)
exp_power = (a^m)^n = a^(mn)
"""

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(formulas_content)

    def _create_constants_file(self, file_path: str) -> None:
        """Create a default constants.txt file."""
        constants_content = """# Mathematical Constants

# Basic Constants
pi = 3.141592653589793
e = 2.718281828459045

# Physical Constants (commonly used in calculations)
phi = 1.618033988749895
gamma = 0.5772156649015329
sqrt2 = 1.4142135623730951
sqrt3 = 1.7320508075688772

# Conversion Factors
deg_to_rad = 0.017453292519943295
rad_to_deg = 57.29577951308232

# Infinity and undefined
inf = inf
nan = nan
"""

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(constants_content)

    def add_custom_formula(self, category: str, expression: str, result: str) -> None:
        """
        Add a custom formula to the specified category.

        Args:
            category (str): Formula category
            expression (str): Mathematical expression
            result (str): Formula result
        """
        if category not in self.formulas:
            self.formulas[category] = {}

        self.formulas[category][expression] = result

    def search_formulas(self, query: str, category: Optional[str] = None) -> Dict[str, List[Tuple[str, str]]]:
        """
        Search for formulas containing the query string.

        Args:
            query (str): Search query
            category (str, optional): Specific category to search

        Returns:
            Dict mapping categories to lists of matching formulas
        """
        results = {}
        query_lower = query.lower()

        categories_to_search = [category] if category else self.formulas.keys()

        for cat in categories_to_search:
            if cat in self.formulas:
                matches = []
                for expr, result in self.formulas[cat].items():
                    if (query_lower in expr.lower() or 
                        query_lower in result.lower()):
                        matches.append((expr, result))

                if matches:
                    results[cat] = matches

        return results

    def get_formula_categories(self) -> List[str]:
        """Get list of all formula categories."""
        return list(self.formulas.keys())

    def get_formulas_by_category(self, category: str) -> Dict[str, str]:
        """Get all formulas in a specific category."""
        return self.formulas.get(category, {}).copy()


# Example usage and testing
if __name__ == "__main__":
    loader = FormulaLoader()

    print("🧪 Testing Formula Loader")
    print("-" * 40)

    # Load all formulas
    all_formulas = loader.load_all_formulas()

    # Display categories
    categories = loader.get_formula_categories()
    print(f"Available categories: {categories}")

    print("✅ Formula Loader test completed")
