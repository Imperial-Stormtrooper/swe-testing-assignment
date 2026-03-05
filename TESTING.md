# Testing Strategy

## Overview

This project uses automated testing to verify the correctness of the calculator implementation.

The tests are written using the pytest framework.

---

## Unit Testing

Unit tests verify individual calculator functions:

* add()
* subtract()
* multiply()
* divide()

Each function is tested independently.

---

## Edge Cases

Special cases tested:

Division by zero

This case ensures that the program correctly raises an error.

---

## Test Execution

Tests can be executed using:

pytest

The framework automatically discovers files starting with **test_** and runs them.

---

## Why pytest?

pytest was chosen because:

* simple and readable syntax
* automatic test discovery
* powerful assertion system
* widely used in Python development
