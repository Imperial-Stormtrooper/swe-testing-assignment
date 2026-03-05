"""
test_calculator.py — Test suite for Quick-Calc
Run with:  pytest test_calculator.py -v

Covers:
  - Unit tests  : all four operations + edge cases
  - Integration : simulated user interaction via the GUI state machine
"""

import pytest
from calculator import add, subtract, multiply, divide, calculate, QuickCalc


# ══════════════════════════════════════════════
#  UNIT TESTS — pure calculation logic
# ══════════════════════════════════════════════

class TestAddition:
    def test_add_positive_numbers(self):
        assert add(5, 3) == 8

    def test_add_negative_numbers(self):
        assert add(-4, -6) == -10

    def test_add_zero(self):
        assert add(0, 99) == 99

    def test_add_floats(self):
        assert add(1.1, 2.2) == pytest.approx(3.3)


class TestSubtraction:
    def test_subtract_basic(self):
        assert subtract(10, 4) == 6

    def test_subtract_negative_result(self):
        assert subtract(3, 10) == -7

    def test_subtract_same_numbers(self):
        assert subtract(7, 7) == 0


class TestMultiplication:
    def test_multiply_basic(self):
        assert multiply(6, 7) == 42

    def test_multiply_by_zero(self):
        assert multiply(999, 0) == 0

    def test_multiply_negative(self):
        assert multiply(-3, 4) == -12

    def test_multiply_large_numbers(self):
        assert multiply(1_000_000, 1_000_000) == 1_000_000_000_000


class TestDivision:
    def test_divide_basic(self):
        assert divide(10, 2) == 5

    def test_divide_returns_float(self):
        assert divide(7, 2) == pytest.approx(3.5)

    def test_divide_by_zero_raises(self):
        with pytest.raises(ZeroDivisionError):
            divide(5, 0)

    def test_divide_negative(self):
        assert divide(-12, 4) == -3


class TestEdgeCases:
    def test_very_large_addition(self):
        assert add(1e15, 1e15) == 2e15

    def test_decimal_subtraction(self):
        assert subtract(0.9, 0.1) == pytest.approx(0.8)

    def test_multiply_two_negatives_gives_positive(self):
        assert multiply(-5, -5) == 25

    def test_divide_fraction_result(self):
        assert divide(1, 3) == pytest.approx(0.3333, rel=1e-3)


class TestCalculateDispatcher:
    def test_dispatch_addition(self):
        assert calculate(2, "+", 3) == 5

    def test_dispatch_subtraction(self):
        assert calculate(10, "-", 3) == 7

    def test_dispatch_multiplication(self):
        assert calculate(4, "*", 5) == 20

    def test_dispatch_division(self):
        assert calculate(8, "/", 2) == 4

    def test_dispatch_unknown_operator(self):
        with pytest.raises(ValueError):
            calculate(1, "^", 2)

    def test_dispatch_division_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            calculate(9, "/", 0)


# ══════════════════════════════════════════════
#  INTEGRATION TESTS — GUI state machine
# ══════════════════════════════════════════════

@pytest.fixture
def app(tmp_path):
    """
    Create a QuickCalc instance without showing a window.
    We withdraw it immediately so no window pops up during testing.
    """
    calc = QuickCalc()
    calc.withdraw()   # hide the window
    yield calc
    calc.destroy()


class TestGUIIntegration:
    def test_full_addition_sequence(self, app):
        """
        Simulate: 5  +  3  =  → display shows '8'
        """
        for ch in "5":
            app._on_button(ch)
        app._on_button("+")
        for ch in "3":
            app._on_button(ch)
        app._on_button("=")

        assert app._result_var.get() == "8"

    def test_clear_resets_display(self, app):
        """
        After a calculation, pressing C must reset the display to '0'.
        """
        for ch in "9":
            app._on_button(ch)
        app._on_button("*")
        for ch in "9":
            app._on_button(ch)
        app._on_button("=")
        app._on_button("C")

        assert app._result_var.get() == "0"
        assert app._expr_var.get() == ""

    def test_division_by_zero_shows_error(self, app):
        """
        Dividing by zero must show an error string, not crash.
        """
        for ch in "5":
            app._on_button(ch)
        app._on_button("/")
        for ch in "0":
            app._on_button(ch)
        app._on_button("=")

        result = app._result_var.get()
        assert "Error" in result or "error" in result.lower()

    def test_chained_operations_via_clear(self, app):
        """
        10 - 4 = 6, then C, then 3 * 3 = 9
        """
        for ch in "10":
            app._on_button(ch)
        app._on_button("-")
        for ch in "4":
            app._on_button(ch)
        app._on_button("=")
        assert app._result_var.get() == "6"

        app._on_button("C")

        for ch in "3":
            app._on_button(ch)
        app._on_button("*")
        for ch in "3":
            app._on_button(ch)
        app._on_button("=")
        assert app._result_var.get() == "9"

    def test_decimal_input_and_result(self, app):
        """
        1.5 + 1.5 = 3
        """
        for ch in "1.5":
            app._on_button(ch)
        app._on_button("+")
        for ch in "1.5":
            app._on_button(ch)
        app._on_button("=")

        assert app._result_var.get() == "3"
