# 🧪 Test Guide: Resume Intelligence Extractor

**Project:** Resume Intelligence Extractor  
**Filename:** `test_resume_parser.py`  
**Author:** Sanjeet Prasad  
**Email:** sanjeet8.23@gmail.com  
**Date:** 26-Oct-2025  
**Framework:** `unittest` (Python Standard Library)

---

## 🎯 Purpose

This guide outlines the unit testing strategy for the `ResumeParser` engine and its modular field extractors. It ensures that resume parsing, field extraction, and CSV export behave reliably across real-world resume formats and edge cases.

---

## 📁 Test File Location

```text
ResumeExtractor/
├── test/
│   ├── test_resume_parser.py
│   ├── test_field_extractors.py
│   ├── test_loader_pdf.py
│   └── test_patterns.py
```

## ✅ Test Cases

| Test ID | Method Name                              | Description                                                   |
|---------|------------------------------------------|---------------------------------------------------------------|
| TC01    | `test_resume_parser_extracts_core_fields`| Verifies name, email, phone, location, and experience fields  |
| TC02    | `test_skills_extraction`                 | Confirms skills are extracted and normalized correctly        |
| TC03    | `test_job_title_debug_flag`              | Ensures job title extractor respects debug flag               |
| TC04    | `test_pdf_loader_reads_text`             | Validates PDF text extraction from sample resume              |
| TC05    | `test_exporter_creates_csv`              | Checks that CSV output is generated and contains expected data|
| TC06    | `test_field_not_found_returns_default`   | Ensures missing fields return 'Not found' or empty values     |


## 🧪 Execution Instructions
Run all tests from project root:

- python -m unittest test/test_resume_parser.py

Run a specific test file:
- python test/test_resume_parser.py



## 🧹 Cleanup Strategy
- Temporary CSV files created during tests are deleted in tearDown()
- Tests are isolated and stateless for reproducibility
- Sample resumes are reused from data/resumes/ for consistency

## 📌 Notes
- Tests are designed for CLI execution and CI integration
- All extractors are modular and testable independently
- Extendable for new fields (e.g., certifications, LinkedIn, GitHub)