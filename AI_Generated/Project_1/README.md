# 🧮 Advanced Calculus Calculator

A comprehensive, efficient calculus calculator built with Python that handles derivatives, integrals, and basic mathematical operations with high precision and professional code quality.

## ✨ Features

### 🔢 Core Mathematical Operations
- **Derivatives**: Symbolic differentiation using power rule, product rule, quotient rule, and chain rule
- **Integrals**: Indefinite and definite integration with symbolic computation
- **Basic Math**: Advanced arithmetic, trigonometric, logarithmic, and exponential functions
- **Formula Database**: Extensive collection of mathematical formulas and rules

### 🎯 Advanced Capabilities
- **Multiple Input Formats**: Support for various mathematical notations
- **High Precision**: Decimal precision up to 28 digits
- **Formula Management**: Organized database of derivatives, integrals, and general formulas
- **Interactive Mode**: Command-line interface with help and examples
- **Batch Processing**: Command-line argument support for single calculations

### 🏗️ Professional Architecture
- **Modular Design**: Clean separation of concerns with dedicated engines
- **Extensible Framework**: Easy to add new mathematical functions and rules
- **Error Handling**: Comprehensive validation and error reporting
- **Unit Testing**: Full test coverage for reliability
- **Documentation**: Complete inline documentation and examples

## 📁 Project Structure

```
calculus_calculator/
├── calculator.py           # Main application entry point
├── switch.py              # Operation type detection and routing
├── utils.py               # Mathematical utilities and helpers
├── requirements.txt       # Project dependencies
├── setup.py              # Package installation script
├── README.md             # This file
│
├── modules/              # Core calculation engines
│   ├── __init__.py
│   ├── derivative_engine.py    # Symbolic differentiation
│   ├── integral_engine.py      # Integration calculations
│   ├── basic_math.py          # Elementary mathematics
│   └── formula_loader.py       # Formula management
│
├── data/                 # Mathematical formulas database
│   ├── derivatives.txt    # Derivative rules and formulas
│   ├── integrals.txt     # Integration rules and formulas
│   ├── formulas.txt      # General mathematical formulas
│   └── constants.txt     # Mathematical constants
│
└── tests/               # Unit tests
    ├── __init__.py
    ├── test_calculator.py
    └── test_utils.py
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Option 1: Direct Installation
```bash
git clone https://github.com/divyanshakya966/calculus-calculator.git
cd calculus-calculator
pip install -r requirements.txt
```

### Option 2: Development Installation
```bash
git clone https://github.com/divyanshakya966/calculus-calculator.git
cd calculus-calculator
pip install -e .
```

## 💻 Usage

### Interactive Mode
Run the calculator in interactive mode for multiple calculations:

```bash
python calculator.py
```

### Command Line Mode
Perform single calculations via command line:

```bash
python calculator.py "d/dx[x^2 + 3x + 1]"
python calculator.py "integral(sin(x))"
python calculator.py "sqrt(16) + 2^3"
```

## 📚 Examples

### Derivative Calculations
```python
# Basic derivatives
d/dx[x^3 + 2x^2 + x + 1]  # → 3x^2 + 4x + 1
derivative(sin(x)*cos(x))  # → cos²(x) - sin²(x)
diff(ln(x^2))             # → 2/x

# Advanced derivatives
d/dx[e^(x^2)]             # → 2x*e^(x^2)
derivative(tan(x))        # → sec²(x)
```

### Integral Calculations
```python
# Basic integrals
integral(x^2)             # → x³/3 + C
∫[2x + 5]dx              # → x² + 5x + C
integral(sin(x))          # → -cos(x) + C

# Advanced integrals
∫[e^x]dx                 # → e^x + C
integral(1/x)            # → ln|x| + C
```

### Basic Mathematics
```python
# Arithmetic and functions
2 + 3 * 4                # → 14
sqrt(144) + 2^3          # → 20
sin(pi/2) + cos(0)       # → 2
ln(e^2)                  # → 2

# Complex expressions
2 * pi * 5               # → 31.41592653589793
log(1000) + sqrt(16)     # → 7
```

## 🎮 Interactive Mode Commands

| Command | Description | Example |
|---------|-------------|---------|
| `help` | Show help information | `help` |
| `examples` | Display example calculations | `examples` |
| `quit`, `exit`, `q` | Exit calculator | `quit` |

### Supported Operations

#### Derivative Notation
- `d/dx[expression]` - Standard derivative notation
- `derivative(expression)` - Function-style notation
- `diff(expression)` - Alternative notation

#### Integral Notation
- `∫[expression]dx` - Mathematical integral notation
- `integral(expression)` - Function-style notation
- `definite(expression, a, b)` - Definite integral

#### Basic Math Functions
- **Trigonometric**: `sin()`, `cos()`, `tan()`, `asin()`, `acos()`, `atan()`
- **Logarithmic**: `ln()`, `log()`, `log2()`
- **Exponential**: `exp()`, `^`, `**`
- **Other**: `sqrt()`, `abs()`, `floor()`, `ceil()`

#### Constants
- `pi`, `π` - Pi (3.14159...)
- `e` - Euler's number (2.71828...)
- `phi` - Golden ratio (1.61803...)

## 🔧 Configuration

### Adding Custom Formulas
Add custom formulas to the appropriate data files:

**derivatives.txt**:
```
# Custom derivative
my_function = my_derivative
```

**integrals.txt**:
```
# Custom integral
my_function = my_integral
```

**formulas.txt**:
```
[MyCategory]
my_formula = my_result
```

### Extending Functionality
The modular architecture makes it easy to extend:

1. **New Operations**: Add to `switch.py` and create new engine
2. **New Functions**: Extend `basic_math.py` function mappings
3. **New Rules**: Add to appropriate data files
4. **Custom Engines**: Create new modules in `modules/` directory

## 🧪 Testing

Run the test suite to ensure everything works correctly:

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=. --cov-report=html

# Run specific test file
python -m pytest tests/test_calculator.py
```

## 📈 Performance

- **High Precision**: 28-digit decimal precision for accurate calculations
- **Efficient Algorithms**: Optimized mathematical operations
- **Memory Management**: Careful handling of large expressions
- **Error Handling**: Robust validation and error recovery

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Write comprehensive tests for new features
- Update documentation for any changes
- Ensure all tests pass before submitting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/calculus-calculator/issues) page
2. Create a new issue with detailed description
3. Contact the maintainers

## 🙏 Acknowledgments

- Built with Python's powerful mathematical libraries
- Inspired by symbolic computation systems
- Thanks to the open-source mathematics community

## 🚀 Future Enhancements

- [ ] Graphical user interface (GUI)
- [ ] 3D plotting capabilities
- [ ] LaTeX output formatting
- [ ] Step-by-step solution explanations
- [ ] Integration with popular math software
- [ ] Mobile app version
- [ ] Web-based interface

---

**Made with ❤️ for mathematics enthusiasts and students worldwide**

*For more information, visit our [documentation](https://github.com/yourusername/calculus-calculator/wiki) or check out the [examples](examples/) directory.*
