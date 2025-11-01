# 📶 NR 5G Throughput Calculator

A modular, CLI-based Python tool for calculating theoretical 5G NR throughput using key physical layer parameters. Built for telecom engineers, educators, and students working with FR1 configurations.

---

## 🧠 Purpose

This project provides a hands-on calculator for exploring 5G NR throughput concepts such as modulation order, coding rate, PRBs, symbol duration, and overhead. It’s designed for:

- 📚 Classroom demonstrations  
- 🧪 Student assignments  
- 🛠️ Telecom validation workflows

---

## 📁 Project Structure

```text
NR_5G_Throughput_Calculator/
├── src/                          # Core logic and visual reference
│   ├── nr_throughput_calculator.py   # OOP-based throughput calculator
│   └── nr_throughput_formula.png     # Formula diagram (optional)
│
├── test/                         # Unittest-based validation
│   └── test_nr_throughput.py
│
├── docs/                         # Specification and test guides
│   ├── specs.md
│   └── test_guide.md
│
└── README.md                     # Project overview and usage
```

## 🚀 Getting Started
✅ Prerequisites
Python 3.11+

Pillow (for image display)

nrarfcn (optional for CLI extensions)
```python
pip install Pillow nrarfcn
```

## ▶️ Run the Throughput Calculator
```python
python src/nr_throughput_calculator.py
```

Displays formula image, prompts for input, and calculates throughput.
## 🧪 Run Unit Tests
```python
python -m unittest test.test_nr_throughput -v
```
Or run directly with summary:
```python
PYTHONPATH=. python test/test_nr_throughput.py
```
Expected output:
```text
Test Summary:
Total tests run   : 5
Tests passed      : 5
Tests failed      : 0
Tests with errors : 0
```

## 📋 Key Parameters
- Component carriers (CCs)
- MIMO layers
- Modulation order (QPSK, 16QAM, 64QAM)
- Coding rate
- Subcarrier spacing (based on numerology)
- PRB count
- Symbol duration
- Overhead (DL/UL, FR1/FR2)

## 📚 Documentation
See docs/test_guide.md for:

- Sample inputs and expected outputs
- Manual validation steps
- CLI walkthrough and test summary

## 🛠️ Author
- Author: Sanjeet Prasad
- Email: sanjeet8.23@gmail.com
- Linkedin : [sanjeet9019](https://www.linkedin.com/in/sanjeet9019/)