# 📘 Software Specification Document

**Project:** NRThroughputCalculator  
**Filename:** `nr_throughput_calculator.py`  
**Author:** Sanjeet Prasad  
**Email:** sanjeet8.23@gmail.com  
**Date:** 23-Oct-2025  
**Version:** 1.0  
**Interpreter:** Python 3.11.0

---

## 1. 🎯 Purpose

This module provides a programmable interface for calculating theoretical 5G NR throughput based on modulation, coding rate, PRBs, symbol duration, and overhead. It is designed for FR1 (sub-6 GHz) configurations and supports educational, validation, and automation workflows.

---

## 2. 📦 Scope

Intended for:

- Telecom engineers and protocol testers  
- Embedded systems educators and students  
- Classroom demonstrations and reproducible lab scripts  
- Integration into CLI tools and throughput simulators

---

## 3. 🧱 System Overview

| Component                   | Description                                      |
|----------------------------|--------------------------------------------------|
| `nr_throughput_calculator.py` | Core logic for throughput and symbol duration     |
| `NRThroughputCalculator`      | Class encapsulating all configurable parameters   |

---

## 4. 📥 Inputs

- Numerology (0–3)  
- Bandwidth in MHz  
- Modulation order (e.g., 2, 4, 6)  
- Coding rate (0.0–1.0)  
- MIMO layers  
- Component carriers  
- Overhead fraction  
- Subcarrier spacing

---

## 5. 📤 Outputs

- Subcarrier spacing (kHz)  
- PRB count  
- Symbol duration (seconds)  
- Calculated throughput (Mbps)

---

## 6. ⚙️ Functional Requirements

- Map numerology to subcarrier spacing  
- Calculate PRBs from bandwidth and spacing  
- Compute OFDM symbol duration  
- Calculate theoretical throughput using:

```text
Throughput = num_cc × num_mimo × mod_order × coding_rate × num_prbs × symbol_duration × (1 - overhead)
```
## 7. 🧪 Testing Strategy
Unit tests using unittest framework

5 test cases covering:

- Subcarrier spacing
- PRB calculation
- Symbol duration
- Realistic throughput
- Zero throughput edge case

Console output includes test case ID and result

Summary printed at end of execution

## 8. 📦 Dependencies
```text
Python 3.11+
No external libraries required
```
## 9. 📁 Folder Structure
```text
NR_5G_Throughput_Calculator/
├── src/
│   ├── nr_throughput_calculator.py       # Core throughput logic
│   └── nr_throughput_formula.png         # Visual reference (formula diagram)
├── test/
│   └── test_nr_throughput.py             # Unit tests with labeled output
├── docs/
│   ├── specs.md                          # Software specification document
│   └── test_guide.md                     # Test case documentation
├── README.md                             # Project overview 

```
## 10. 📌 Notes
- Designed for FR1 (sub-6 GHz) configurations.

- Symbol duration assumes 14 symbols per slot.

- Overhead accounts for control signaling and reference signals.