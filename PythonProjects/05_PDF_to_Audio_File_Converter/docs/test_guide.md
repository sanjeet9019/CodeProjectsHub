# 🧪 Test Guide: PDFToAudioConverter

**Project:** PDFToAudioConverter  
**Filename:** `test_pdf_to_audio_converter.py`  
**Author:** Sanjeet Prasad  
**Email:** sanjeet8.23@gmail.com  
**Date:** 24-Oct-2025  
**Framework:** `unittest` (Python Standard Library)

---

## 🎯 Purpose

This guide outlines the unit testing strategy for the `PDFToAudioConverter` class. It ensures that core functionality — PDF parsing, audio synthesis, and file generation — behaves reliably across environments and input conditions.

---

## 📁 Test File Location
```text
PDFToAudioConverter/
├── tests/
│   └── test_pdf_to_audio_converter.py
```

---

## ✅ Test Cases

| Test ID | Method Name                            | Description                                                  |
|---------|----------------------------------------|--------------------------------------------------------------|
| TC01    | `test_pdf_file_exists`                 | Verifies that the input PDF file exists                      |
| TC02    | `test_read_pdf_initializes_reader`     | Confirms that the PDF reader is initialized correctly        |
| TC03    | `test_convert_to_audio_runs_without_error` | Ensures audio conversion completes without exceptions    |
| TC04    | `test_audio_file_created`              | Checks that the MP3 output file is generated                 |

---

## 🧪 Execution Instructions

### Run all tests from project root:
```bash
python -m unittest tests.test_pdf_to_audio_converter
```
Or run the file directly:
```bash
python tests/test_pdf_to_audio_converter.py
```
---
### 🧹 Cleanup Strategy
- tearDown() removes test_output.mp3 after each test to ensure reproducibility and prevent clutter.
- All tests are isolated and do not depend on prior state.

---
### 📌 Notes
- Tests are designed for CLI execution and CI integration.
- All outputs are logged with pass/fail status and exception trace if applicable.
- Extendable for edge cases: empty PDFs, unreadable pages, per-page audio generation