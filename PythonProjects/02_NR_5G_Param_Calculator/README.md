# 📡 NR 5G Parameter Calculator

A modular, menu-driven CLI tool for calculating and validating key 5G NR parameters — built for telecom engineers, educators, and students.

---

## 🧠 Purpose

This project provides a hands-on calculator for exploring 5G NR concepts such as ARFCN, frequency, band mapping, duplex modes, GSCN, numerology, and PRB allocation. It’s designed for:

- 📚 Classroom demonstrations
- 🧪 Student assignments
- 🛠️ Telecom validation workflows

---

## 📁 Project Structure

```text
NR_5G_Param_Calculator/
├── src/                          # Main CLI and logic modules
│   ├── nr5gcalculator.py         # Menu-driven CLI interface
│   └── nr5gmodule.py             # Core calculation functions
│
├── test/                         # Pytest-based unit tests
│   └── test_nr5gmodule.py
│
├── docs/                         # Guides and validation references
│   ├── test_guide.md             # Manual test walkthrough
│   └── specs.md                  # 3GPP specs and parameter notes
│
└── README.md                     # Project overview and usage

```
---
## 🚀 Getting Started

### ✅ Prerequisites

- Python 3.11+
- `nrarfcn` library (for ARFCN/Frequency mapping)

```bash
pip install nrarfcn pytest
```
## ▶️ Run the 5G Calculator
```bash
python src/nr5gcalculator.py
```
## 🧪 Run in Test Mode
```bash
python src/nr5gcalculator.py --test
```
Runs 3GPP-compliant sample cases for ARFCN, Frequency, and PRB calculation

## 📋 Menu Options

| Option | Description                         |
|--------|-------------------------------------|
| 1      | ARFCN ➡ Frequency                   |
| 2      | Frequency ➡ ARFCN                   |
| 3      | Frequency ➡ Band List               |
| 4      | ARFCN ➡ Band List                   |
| 5      | Band ➡ Duplex Type                  |
| 6      | Band ➡ ARFCN Range                  |
| 7      | Band ➡ Frequency Range              |
| 8      | GSCN ➡ Frequency                    |
| 9      | Frequency ➡ GSCN                    |
| 10     | Band ➡ GSCN Range                   |
| 11     | Numerology ➡ Subcarrier Spacing     |
| 12     | PRB Calculation (Numerology + BW)   |

## 🧪 Testing
Run all unit tests:
```bash
pytest test/test_nr5gmodule.py
```

Expected output:
15 passed in n seconds

## 📚 Documentation
See docs/test_guide.md for:

- Sample inputs and expected outputs
- Manual validation steps
- CLI test mode walkthrough

## 🛠️ Author
- Author: Sanjeet Prasad
- Email: sanjeet8.23@gmail.com
- Linkedin : [sanjeet9019](https://www.linkedin.com/in/sanjeet9019/)