# 🧪 NRThroughputCalculator – Unit Test Guide

**Author:** Sanjeet Prasad  
**Email:** sanjeet8.23@gmail.com  
**Date:** 23-Oct-2025  
**Environment:** Ubuntu 22.04 / Windows 11  
**Interpreter:** Python 3.11.0  
**Module:** `nr_throughput_calculator.py`  
**Test File:** `test_nr_throughput.py`

---

## ✅ Purpose

This guide documents the unit tests for the `NRThroughputCalculator` class. The tests validate core computational methods related to subcarrier spacing, PRB calculation, symbol duration, and throughput estimation. The test suite is designed for clarity, reproducibility, and classroom use.

---

## ✅ Test File Location

```text
NR_5G_Throughput_Calculator/
└── test/
    └── test_nr_throughput.py
```
## ✅ How to Run Tests
Standard (recommended)
```python
python -m unittest test/test_nr_throughput.py 
```
Direct execution with summary
```python
PYTHONPATH=. python test/test_nr_throughput.py
```

## ✅ Test Coverage

| Test ID | Description                                      | Method Tested               |
|---------|--------------------------------------------------|-----------------------------|
| 01      | Subcarrier spacing for numerology 0–3           | `get_subcarrier_spacing()` |
| 02      | PRB calculation for 100 MHz @ 30 kHz             | `get_num_prbs()`           |
| 03      | Symbol duration for 30 kHz spacing               | `calculate_symbol_duration()` |
| 04      | Realistic throughput calculation                 | `calculate_throughput()`   |
| 05      | Zero throughput edge case                        | `calculate_throughput()`   |

## ✅ Console Output Format

Each test prints:

- Test ID and description
- Result (pass/fail)
- Key values (e.g., PRBs, throughput)

Example:
```text
Test 02: PRB calculation for 100 MHz @ 30 kHz
Test 02 passed: Calculated PRBs = 273
```
## ✅ Summary Output
When run directly, the script prints a final summary:

Test Summary:
```text
Total tests run   : 5
Tests passed      : 5
Tests failed      : 0
Tests with errors : 0
```