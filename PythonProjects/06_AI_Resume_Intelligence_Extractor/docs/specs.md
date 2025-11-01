# 📘 Software Specification Document

**Project:** Resume Intelligence Extractor  
**Filename:** `run_extractor.py`  
**Author:** Sanjeet Prasad  
**Email:** sanjeet8.23@gmail.com  
**Date:** 26-Oct-2025  
**Version:** 1.0  
**Interpreter:** Python 3.11.0

---

## 🎯 Purpose

Extract structured insights from resume PDFs using a modular, extensible Python engine. Designed for HR automation, classroom demos, and onboarding workflows.

---

## 📦 Scope

- Resume parsing for HR and educators  
- CLI-based automation and batch mode  
- Field-specific debug logging for teaching  
- CSV export for review and scoring  
- Classroom-ready reproducibility and extension

---

## 🧱 System Overview

| Component               | Description                                              |
|------------------------|----------------------------------------------------------|
| `run_extractor.py`     | CLI launcher with argument parsing and timing breakdown  |
| `ResumeParser`         | Core controller for orchestrating field extraction       |
| `config.py`            | Centralized runtime flags and metadata                   |
| `field_selector.py`    | Dynamically selects which fields to extract              |
| `fields/*.py`          | One class per field: name, email, skills, etc.           |
| `exporter.py`          | Saves results to per-resume CSV                          |
| `logger.py`            | Logging utility with toggleable verbosity                |

---

## 📥 Inputs

- Resume PDF file path (`resume.pdf`)  
- Optional: `--debug` for global logging  
- Optional: `--fields name,email,skills`  
- Optional: `--all` to process all resumes in `data/resumes/`  
- Optional: field-specific debug flags (`--debug-skills`, `--debug-score`, etc.)

---

## 📤 Outputs

- Console logs with structured resume insights  
- CSV file saved to `data/output/`  
- Timing breakdown per extractor (if debug enabled)  
- Final summary with emoji indicators  
- Modular output for classroom review

---

## ⚙️ Functional Requirements

- Load and parse PDF using `PyMuPDF` or `pdfminer`  
- Extract fields using regex and NLP strategies  
- Support dynamic field selection via CLI  
- Enable global and field-specific debug modes  
- Export results to structured CSV  
- Handle missing fields gracefully  
- Log timing for each extractor  
- Support batch mode for multiple resumes  
- Modular design for classroom extension

---

## 🧪 Testing Strategy

Unit tests using `unittest` framework

Test cases cover:

- PDF loading and text extraction  
- Individual field extractors  
- CLI argument parsing and fallback logic  
- CSV export correctness  
- Debug logging behavior  
- Edge-case handling for missing or noisy data

---

## 📦 Dependencies

```text
Python 3.11+
PyMuPDF or pdfminer
regex
argparse
```

## 📁 Folder Structure
```text
ResumeExtractor/
├── src/
│   └── extractor/
│       ├── __init__.py
│       ├── config.py
│       ├── resume_parser.py
│       ├── field_selector.py
│       ├── fields/
│       │   ├── base.py
│       │   ├── name_field.py
│       │   ├── email_field.py
│       │   ├── ...
│       └── utils/
│           ├── constants.py
│           ├── exporter.py
│           ├── logger.py
│           ├── pdf_loader.py
│           ├── result_types.py
├── scripts/
│   └── run_extractor.py
├── test/
│   └── test_resume_parser.py
├── docs/
│   ├── specs.md
│   └── test_guide.md
├── data/
│   ├── resumes/
│   └── output/
├── .env
└── README.md
```
## 📌 Notes
- Designed for CLI use on Linux, Windows, and WSL 
- All extractors are modular and classroom-friendly 
- Easily extensible for scoring, filtering, or resume ranking
- Supports debug-driven teaching and onboarding workflows