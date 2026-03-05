# Quick_Calc Testing

---

## Testing Strategy

The test suite for the Quick-Calc application was organised in a way that accounts for the separation between the application's two parts: the user interface and the arithmetic logic responsible for handling calculations. The core calculation logic was intentionally extracted into pure, standalone functions (`add`, `subtract`, `multiply`, `divide`, and `calculate`) rather than embedded inside event handlers or GUI callbacks. This separation ensures that the arithmetic logic is independently testable without requiring any UI initialisation, and produces precise, targeted error messages useful for identifying exactly which operation does not work as intended or which edge case is not handled correctly.

A number of aspects of the application were evaluated during the testing process. Firstly, all four arithmetic operations were tested, accounting for positive integers, negative integers, as well as zero. Further, three edge cases were evaluated: division by zero, operations with very large numbers, and the use of an unrecognised operator. When it comes to integration tests, complete user interaction workflows were simulated to verify that the UI layer correctly passes inputs to the calculation logic and writes the obtained results to the display, as well as to confirm that the Clear button correctly resets all fields.

There were, however, also some aspects that were not covered by either the unit tests or the integration tests. The application's performance and response time were not tested, as it was deemed that for a simple single-threaded desktop calculator, such benchmarking would not add any practical value. Additionally, input validation edge cases — such as the presence of empty fields or non-numeric characters — were not included in automated evaluation, since the responsibility for handling such cases is delegated to the UI layer of the application, which incorporates a number of safeguards to prevent errors in such scenarios before any calculation is attempted.

---

## Testing Concepts

### The Testing Pyramid

The test suite reflects the testing pyramid's proportions. The wider base of the pyramid is made up of 15 unit tests that evaluate the arithmetic logic contained in the core calculation functions directly. These tests do not involve any UI initialisation and produce very precise error messages useful for identifying which exact operator does not behave as intended or which edge case is not handled properly. The middle layer of the pyramid consists of 4 integration tests that utilise a hidden `QuickCalc` application instance. These tests are slower than the unit tests and require a display environment to run correctly, while also providing more generalised and broad failure information. They serve their intended purpose of confirming that a proper connection exists between the UI layer and the underlying arithmetic logic. Higher levels of the testing pyramid — such as end-to-end tests driven by a real windowing system — were intentionally not implemented. Their implementation was not required by the assignment scope, and automating a real GUI windowing system would be unreasonably expensive for an application of this scale.

### Black-Box and White-Box Testing

In the unit tests, the arithmetic logic is treated as a black box. More specifically, the unit tests care not about how exactly each operation is internally implemented, but rather about what output is produced for a given pair of inputs. This characteristic is a deliberate benefit: the unit tests remain unaffected by potential internal refactors to the calculation logic, as long as the observable outputs remain correct.

Writing the integration tests required white-box awareness. In order to simulate user interactions meaningfully, it was necessary to understand the sequence in which the `_on_button` method processes inputs, how the operator state is stored between button presses, and what the Clear button is expected to reset. The tests themselves, however, are still classified as black-box tests in terms of what they verify — they only evaluate the final value shown in the result display and do not inspect any intermediate internal state variables.

### Functional vs Non-Functional Testing

All 19 written tests are functional tests. This is due to the fact that they evaluate whether the application performs as it is supposed to and produces the expected outputs. More specifically, the unit tests verify that each arithmetic operator performs correctly in the intended way, while the integration tests check the correctness of the implementation for the user-facing calculator workflow.

Non-functional tests were intentionally excluded. Tests aiming at evaluating the performance of the application or its accessibility were considered excessive for a simple calculator application of this scope, and including them would not meaningfully improve confidence in the software's correctness.

### Regression Testing

The test suite is written in a way that supports potential future regression testing. Firstly, all tests can be executed with a single command (`pytest test_calculator.py -v`), allowing for rapid re-validation whenever new features are introduced or existing logic is modified. Additionally, due to the way in which the UI and arithmetic logic are separated into distinct layers, the tests have a high potential to remain relevant even after the introduction of significant changes to either the interface or the internal implementation, as long as the public-facing behaviour remains consistent.

---

## Test Results Summary

| # | Test Name | Type | Status |
|---|-----------|------|--------|
| 1 | `add_twoPositiveIntegers` | Unit | ✅ Pass |
| 2 | `add_positiveAndNegative` | Unit | ✅ Pass |
| 3 | `add_twoNegativeIntegers` | Unit | ✅ Pass |
| 4 | `subtract_positiveResult` | Unit | ✅ Pass |
| 5 | `subtract_negativeResult` | Unit | ✅ Pass |
| 6 | `subtract_negativeFromPositive` | Unit | ✅ Pass |
| 7 | `multiply_twoPositiveIntegers` | Unit | ✅ Pass |
| 8 | `multiply_twoNegativeIntegers` | Unit | ✅ Pass |
| 9 | `multiply_byZero` | Unit | ✅ Pass |
| 10 | `divide_evenDivision` | Unit | ✅ Pass |
| 11 | `divide_decimalResult` | Unit | ✅ Pass |
| 12 | `divide_negativeByPositive` | Unit | ✅ Pass |
| 13 | `divideByZero_throwsArithmeticException` | Unit | ✅ Pass |
| 14 | `add_veryLargeNumbers` | Unit | ✅ Pass |
| 15 | `unknownOperator_throwsIllegalArgumentException` | Unit | ✅ Pass |
| 16 | `integration_fullAddition` | Integration | ✅ Pass |
| 17 | `integration_clearResetsAllFields` | Integration | ✅ Pass |
| 18 | `integration_negativeNumberMultiplication` | Integration | ✅ Pass |
| 19 | `integration_fullDivision` | Integration | ✅ Pass |
