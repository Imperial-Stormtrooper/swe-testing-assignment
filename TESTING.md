# TESTING.md — Quick-Calc Test Documentation

---

## 1. Overview of the Testing Approach

Quick-Calc was built with testability as a first-class concern. Rather than embedding calculation logic inside GUI event handlers, all arithmetic was isolated into a set of pure, stateless functions — `add`, `subtract`, `multiply`, `divide`, and the central dispatcher `calculate`. This design decision was not accidental: it makes the business logic independently verifiable without ever launching a window, and keeps test failure messages precise enough to pinpoint exactly which operation or edge case broke.

The overall suite contains **19 tests** split across two layers:

- **15 unit tests** targeting the raw arithmetic functions
- **4 integration tests** simulating real button-press sequences through the GUI state machine

What was *not* tested is just as deliberate. Performance benchmarking was excluded — a single-threaded desktop calculator has no realistic latency requirements worth automating against. UI input validation (empty fields, non-numeric characters) is handled defensively inside the GUI layer itself before any calculation is ever triggered, so testing it at the logic level would be redundant.

---

## 2. Lecture Concepts Applied

### 2.1 The Testing Pyramid

The suite is shaped like the pyramid — deliberately so.

The **base** is wide: 15 unit tests run directly against the calculation functions with zero GUI involvement. They are fast, isolated, and produce surgical failure messages. If `test_divide_by_zero_raises_error` fails, you know exactly where to look.

The **middle layer** holds 4 integration tests. These spin up a hidden `QuickCalc` window instance and drive it through `_on_button()` calls — the same code path a real user triggers. They are slower, require a display environment, and produce broader failure information, but they answer a question the unit tests cannot: does the UI actually wire up to the logic correctly?

The **top of the pyramid** (end-to-end tests driven by a real windowing system like `pyautogui`) was deliberately left out. For a calculator of this scale, that level of automation would cost far more than it would return in confidence.

---

### 2.2 Black-Box vs White-Box Testing

The **unit tests are pure black-box**. They feed inputs into `add(3, -1)` or `calculate(5, "/", 0)` and assert on the output. They have no opinion about internal variable names, branching logic, or how the dispatcher resolves an operator string internally. This means they survive refactors — rewrite the internals completely and the tests still pass, as long as the outputs stay correct.

The **integration tests required white-box knowledge to write** — understanding which method handles button presses (`_on_button`), how operator state is buffered between the first number and the second, and what "Clear" is expected to do to internal state. However, what the integration tests *verify* is still black-box: they only assert on the final string shown in the result display, never on internal variables like `_first_num` or `_operator`.

---

### 2.3 Functional vs Non-Functional Testing

Every one of the 19 tests is a **functional test** — each one asks "does this produce the right output?" rather than "how fast does it run?" or "is the button contrast WCAG-compliant?".

Unit tests confirm that arithmetic operations return correct values across positive numbers, negative numbers, zero, decimals, and very large operands. Integration tests confirm that the full user-facing workflow — entering numbers, pressing operators, reading results, clearing the display — behaves as expected end to end.

**Non-functional testing was intentionally excluded.** Performance testing a calculator that runs arithmetic on a modern CPU in microseconds would be noise, not signal. Accessibility testing, while valuable in production software, falls outside the scope of a logic-focused assignment.

---

### 2.4 Regression Testing

The suite is structured to act as a regression safety net for future changes. Three properties make this possible:

1. **Single-command execution** — `pytest test_calculator.py -v` runs all 19 tests in one go. Adding this to a CI pipeline or a pre-commit hook takes under a minute.
2. **Layer independence** — because UI and logic are separated, changing the button layout or colour scheme will not break unit tests. Refactoring the arithmetic functions will not break integration tests unless the observable outputs change.
3. **Edge case coverage** — tests like `test_divide_by_zero_raises_error` and `test_invalid_operator_raises_error` guard against common regression points where a future shortcut might accidentally remove a guard clause.

---

## 3. Test Results

| # | Test Name | Layer | Result |
|---|-----------|-------|--------|
| 1 | `test_add_two_positive_numbers` | Unit | ✅ Pass |
| 2 | `test_add_positive_and_negative` | Unit | ✅ Pass |
| 3 | `test_add_both_negative` | Unit | ✅ Pass |
| 4 | `test_subtract_gives_positive_result` | Unit | ✅ Pass |
| 5 | `test_subtract_gives_negative_result` | Unit | ✅ Pass |
| 6 | `test_subtract_negative_from_positive` | Unit | ✅ Pass |
| 7 | `test_multiply_positive_numbers` | Unit | ✅ Pass |
| 8 | `test_multiply_negative_numbers` | Unit | ✅ Pass |
| 9 | `test_multiply_any_number_by_zero` | Unit | ✅ Pass |
| 10 | `test_divide_clean_result` | Unit | ✅ Pass |
| 11 | `test_divide_produces_decimal` | Unit | ✅ Pass |
| 12 | `test_divide_negative_dividend` | Unit | ✅ Pass |
| 13 | `test_divide_by_zero_raises_error` | Unit | ✅ Pass |
| 14 | `test_add_extremely_large_values` | Unit | ✅ Pass |
| 15 | `test_invalid_operator_raises_error` | Unit | ✅ Pass |
| 16 | `test_gui_addition_flow` | Integration | ✅ Pass |
| 17 | `test_gui_clear_button_resets_display` | Integration | ✅ Pass |
| 18 | `test_gui_multiplication_with_negative` | Integration | ✅ Pass |
| 19 | `test_gui_division_flow` | Integration | ✅ Pass |
