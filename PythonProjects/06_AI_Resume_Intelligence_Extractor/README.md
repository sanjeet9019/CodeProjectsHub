# 🤖 Resume Intelligence Extractor

A modular, CLI-driven Python engine for extracting structured intelligence from resumes using NLP, regex, and AI-powered logic. Built for HR teams, educators, and students working with real-world resume datasets.

---

## 🎯 Purpose

This project provides a hands-on extractor for parsing resumes into structured fields like name, email, phone, skills, experience, job titles, companies, and tech stack. It combines rule-based logic with machine learning and natural language processing (NLP) to support:

- 📚 Classroom demonstrations  
- 🧪 Python Learners ,student,programmers
- 🧑‍💼 HR automation and resume screening  
- 🛠️ AI-powered field extraction workflows

---

## 📁 Project Structure

```text
Resume_Intelligence_Extractor/
├── src/                          # Core logic and extractors
│   └── extractor/
│       ├── resume_parser.py          # Main parser engine
│       ├── config.py                 # Runtime flags and constants
│       ├── field_selector.py         # Field routing logic
│       ├── fields/                   # Modular field extractors
│       │   ├── base.py               # Shared extractor base class
│       │   ├── name_field.py         # Name extractor
│       │   ├── email_field.py        # Email extractor
│       │   ├── phone_field.py        # Phone extractor
│       │   ├── location_field.py     # Location extractor
│       │   ├── experience_field.py   # Experience extractor
│       │   ├── skills_field.py       # Skills extractor
│       │   ├── jobtitle_field.py     # Job title extractor
│       │   ├── company_field.py      # Company extractor
│       │   ├── score_field.py        # Resume score calculator
│       │   └── techstack_field.py    # Tech stack classifier
│       └── utils/
│           ├── pdf_loader.py         # PDF text extraction
│           ├── exporter.py           # CSV exporter
│           ├── logger.py             # Debug-aware logger
│           ├── cleanup.py            # Pycache cleanup utility
│           ├── constants.py          # Regex and config constants
│           └── result_types.py       # Output schema
│
├── scripts/
│   └── run_extractor.py              # CLI entry point
│
├── test/                             # Unittest-based validation
│   └── test_resume_parser.py         # End-to-end parser tests
│
├── data/
│   ├── resumes/                      # Input PDFs
│   └── output/                       # Extracted CSVs
│
├── docs/
│   ├── specs.md                      # Field specs and logic
│   └── test_guide.md                 # Test coverage and walkthrough
│
└── README.md                         # Project overview and usage

```
## 🚀 Getting Started
✅ Prerequisites Python 3.11+ spaCy (with English model) PyPDF2
```python
pip install spacy PyPDF2
python -m spacy download en_core_web_sm
```

---

## ▶️ Run the Resume Extractor
```python
py scripts/run_extractor.py data/resumes/SampleResume.pdf --debug
```
Outputs structured intelligence to console and saves CSV to data/output/ with full debug logs 

```python
py scripts/run_extractor.py data/resumes/SampleResume.pdf 
```
Outputs structured intelligence to console and saves CSV to data/output/ without debug logs 

## ⚙️ CLI Options

| Option              | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `file` (positional) | Path to a single resume PDF to parse. Defaults to `data/resumes/SampleResume.pdf`. |
| `--all`             | Enables batch mode: parses all PDFs in `data/resumes/`.                     |
| `--fields`          | Comma-separated list of fields to extract (e.g., `name,email,skills`).      |
| `--debug`           | Enables verbose logging across all modules and shows timing breakdown and filename with line number .      |

## Sample Output 
```text
$ py scripts/run_extractor.py data/resumes/SampleResume.pdf

📂 Processing: data/resumes/SampleResume.pdf

📄 Final Resume Intelligence Output
👤 Name: SANJEET PRASAD
📧 Email: sanjeet8.23@gmail.com
📞 Phone: +91 9958217807
📍 Current Location: Noida
🛠️ Skills: bash, c, c++, gdb, git, jira, linux, makefile, oracle, python, shell, valgrind, visio, visual studio, wireshark
💼 Job Titles: Senior Principal Engineer
🏢 Companies: Bombardier Transportation, HCL Technologies, Honeywell Aerospace, Hughes Systique Corporation, Samsung Electronics, Wipro Technologies
🗓️ Total Experience: 15 years 7 months
📊 Resume Score: 5/5
🧠 Tech Stack:
    - Languages: c, c++, python
    - Tools: gdb, git, jira, makefile, valgrind, visual studio, wireshark
    - Platforms: linux

📤 CSV Export Complete
📁 Saved to: data/output\SampleResume.csv
```
---
## 🧪 Run Unit Tests
```text
python -m unittest test.test_resume_parser 
```
Expected output:
```text
✅ TC01 passed: Core fields extracted
✅ TC02 passed: Skills extracted and normalized
✅ TC03 passed: Job title extractor respects debug flag
✅ TC04 passed: PDF text extracted
✅ TC05 passed: CSV file created
✅ TC06 passed: Missing fields handled gracefully
```
---
## 📋 Resume Extracted Fields
- 👤 Name
- 📧 Email
- 📞 Phone
- 📍 Location
- 🛠️ Skills
- 💼 Job Titles
- 🏢 Companies
- 🗓️ Experience
- 📊 Resume Score
- 🧠 Tech Stack (Languages, Tools, Platforms)

---

## 🧠 AI & Machine Learning Integration
- Uses spaCy’s NLP pipeline for entity recognition
- Regex-powered field normalization
- Rule-based logic with debug-aware extractors
- Future-ready for ML-based scoring and classification
- Designed for integration with resume ranking models and ATS systems

---

## 🧼 Cleanup Utility
Automatically removes __pycache__ folders after test or script runs

---
## 📚 Documentation
See docs/specs.md and docs/test_guide.md for:
- Field logic and regex rules
- Sample inputs and expected outputs
- Manual validation steps
- CLI walkthrough and test summary

---
## 🛠️ Author
- Author: Sanjeet Prasad
- Email: sanjeet8.23@gmail.com
- LinkedIn: sanjeet9019