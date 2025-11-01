# 📘 Software Specification Document

**Project:** NR 5G Calculator  
**Filename:** `nr5gcalculator.py`, `nr5gmodule.py`  
**Author:** Sanjeet Prasad  
**Date:** 03-Aug-2025  
**Version:** 1.0

---

## 1. 🎯 Purpose

This tool provides a CLI-based calculator for 5G NR parameters using menu-driven logic. It supports conversions between ARFCN, frequency, band, GSCN, and PRB calculations.

---

## 2. 📦 Scope

Designed for:

- Telecom engineers and students
- Protocol trainers and testers
- Classroom validation and automation

---

## 3. 🧱 System Overview

| Component         | Description                                      |
|------------------|--------------------------------------------------|
| `nr5gcalculator.py` | CLI interface and menu dispatcher               |
| `nr5gmodule.py`     | Conversion logic for NR parameters              |
| `nrarfcn`           | External library for ARFCN utilities            |

---

## 4. 📥 Inputs

- CLI menu selection (1–12)
- ARFCN, frequency, band, numerology, bandwidth

---

## 5. 📤 Outputs

- Tabulated results printed to console
- Duplex mode, PRB count, ARFCN/frequency ranges

---

## 6. ⚙️ Functional Requirements

- ARFCN ↔ Frequency
- Frequency ↔ Band List
- Band ↔ Duplex, ARFCN/Frequency/GSCN ranges
- Numerology ↔ Subcarrier spacing
- PRB calculation

---

## 7. 🧪 Testing Strategy

- Unit tests using `pytest`
- Manual CLI sanity checks

---

## 8. 📦 Dependencies

```bash
pip install nrarfcn pytest
```
## 9. 📁 Folder Structure
```text
NR5G_Calculator/
├── src/
│   ├── nr5gmodule.py
│   └── nr5gcalculator.py
├── test/
│   └── test_nr5gmodule.py
├── docs/
│   ├── specs.md
│   └── test_guide.md
