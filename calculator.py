"""
Simple Calculator Application
SWE Testing Assignment

This module implements a basic calculator with four operations:
addition, subtraction, multiplication and division.

Author: Marahim
Version: 1.0.0
"""

class Calculator:

    def add(self, a, b):
        """Return the sum of two numbers."""
        return a + b

    def subtract(self, a, b):
        """Return the difference of two numbers."""
        return a - b

    def multiply(self, a, b):
        """Return the product of two numbers."""
        return a * b

    def divide(self, a, b):
        """Return the division of two numbers."""
        if b == 0:
            raise ValueError("Division by zero is not allowed")
        return a / b
