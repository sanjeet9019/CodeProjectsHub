# 🧪 NR 5G Calculator – Test & Validation Guide

**Author:** Sanjeet Prasad  
**Email:** sanjeet8.23@gmail.com  
**Date:** 22-Oct-2025  
**Environment:** Ubuntu 22.04 / Windows 11  
**Interpreter:** Python 3.11.0  
**Tool:** `nr5gcalculator.py` (CLI)  
**Module:** `nr5gmodule.py` (logic)  

---

## ✅ Test Preparation

Ensure the following files are present:

- `src/nr5gcalculator.py`
- `src/nr5gmodule.py`
- `test/test_nr5gmodule.py`
- `docs/test_guide.md`

Install dependencies:

```bash
pip install nrarfcn pytest
```

## ✅ Manual Menu Validation

| Menu Option | Description                         | Sample Input(s)           | Expected Output                        |
|-------------|-------------------------------------|---------------------------|----------------------------------------|
| 1           | ARFCN ➡ Frequency                   | `620000`                  | ~3500 MHz (n78 band)                   |
| 2           | Frequency ➡ ARFCN                   | `3500`                    | ~620000                                |
| 3           | Frequency ➡ Band List               | `3500`                    | Includes `n78`                         |
| 4           | ARFCN ➡ Band List                   | `620000`                  | Includes `n78`                         |
| 5           | Band ➡ Duplex Type                  | `n78`                     | `TDD`                                  |
| 6           | Band ➡ ARFCN Range                  | `n78`, `dl`               | Tuple of DL ARFCN range                |
| 7           | Band ➡ Frequency Range              | `n78`, `ul`               | Tuple of UL frequency range (MHz)     |
| 8           | GSCN ➡ Frequency                    | `3000`                    | Valid NR frequency (MHz)              |
| 9           | Frequency ➡ GSCN                    | `3500`                    | Valid GSCN value                       |
| 10          | Band ➡ GSCN Range                   | `n78`                     | Tuple of GSCN range                    |
| 11          | Numerology ➡ Subcarrier Spacing     | `2`                       | `60 kHz`                               |
| 12          | PRB Calculation                     | `Numerology=2`, `BW=100`  | ~1365 PRBs                             |


## ✅ Automated Unit Tests
Run the test suite:
```bash
pytest test/test_nr5gmodule.py
```
Expected result:
15 passed in <time> seconds

## ✅ CLI Test Mode

Run quick validation with 3GPP-compliant values:
```bash
python src/nr5gcalculator.py --test
```
Expected output:

ARFCN ➡ Frequency for 620000

Frequency ➡ ARFCN for 3500

PRB Calculation for 100 MHz, μ=2

## ✅ Log Verification
Check nr5gcalc.log for timestamped entries:
2025-10-22 18:54:12 - ARFCN ➡ Frequency: 3500.0
2025-10-22 18:54:13 - PRB Calculation: 1365

