# Quick-Calc

Quick-Calc is a lightweight desktop calculator application built with Python and tkinter. It supports the four fundamental arithmetic operations — addition, subtraction, multiplication, and division — delivered through a clean, dark-themed graphical user interface. The project was developed as part of a software engineering and testing assignment, with a strong emphasis on code quality, testability, and a well-structured multi-layered test suite.

---

## Setup Instructions

**Requirements:** Python 3.8 or higher. No third-party packages are needed to run the application — tkinter is included with standard Python installations.

**To run the application:**

```bash
python calculator.py
```

**To run the test suite**, first install pytest if you do not have it:

```bash
pip install pytest
```

Then execute all tests with:

```bash
pytest test_calculator.py -v
```

---

## How to Run Tests

All tests are located in `test_calculator.py` and can be executed with a single command from the project root:

```bash
pytest test_calculator.py -v
```

The `-v` flag enables verbose output, showing each individual test name and its pass/fail status. The suite contains 19 tests in total: 15 unit tests and 4 integration tests.

---

## Testing Framework Research

### Pytest vs Unittest

Python ships with two prominent testing solutions: the built-in `unittest` module and the third-party `pytest` framework. Understanding their differences is essential for choosing the right tool for a given project.

`unittest` is part of the Python standard library and requires no installation. It follows the xUnit style, meaning tests are organised as methods inside classes that inherit from `unittest.TestCase`. This structure is familiar to developers coming from Java or C#, and it integrates well with IDEs out of the box. However, the verbosity of `unittest` can become a drawback — even a simple assertion requires calling a specific method such as `self.assertEqual(result, 8)`, and setting up or tearing down test state involves overriding `setUp` and `tearDown` methods explicitly. For larger test suites, this ceremony adds up quickly and reduces readability.

`pytest`, on the other hand, favours simplicity and expressiveness. Tests are plain functions (or optionally grouped into classes without any required base class), and assertions are written using Python's native `assert` keyword. Pytest automatically discovers test files and functions matching the `test_` prefix convention, making it trivially easy to add new tests without any boilerplate registration. It also provides significantly more informative failure messages, highlighting exactly which values differed. Additionally, pytest supports fixtures — a powerful dependency injection mechanism for managing shared setup logic — and has a rich plugin ecosystem covering coverage reporting, parameterisation, mocking, and more.

For Quick-Calc, **pytest** was chosen as the testing framework. The project's emphasis is on clear, readable tests that directly reflect the behaviour being verified. Pytest's minimal syntax, superior output formatting, and fixture support make it the more practical and maintainable choice for this scope, while still scaling well should the project grow in complexity.

---

## Project Structure

```
swe-testing-assignment/
├── calculator.py       # Application source code (GUI + core logic)
├── test_calculator.py  # Full test suite (unit + integration)
├── README.md           # Project documentation
└── TESTING.md          # Testing strategy and results
```
