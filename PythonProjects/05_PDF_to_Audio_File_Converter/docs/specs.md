# 📘 Software Specification Document

**Project:** PDFToAudioConverter  
**Filename:** `pdf_to_audio_converter.py`  
**Author:** Sanjeet Prasad  
**Email:** sanjeet8.23@gmail.com  
**Date:** 24-Oct-2025  
**Version:** 1.0  
**Interpreter:** Python 3.11.0

---

## 🎯 Purpose

Convert multi-page PDF documents into MP3 audio using text-to-speech synthesis. Designed for accessibility, education, and automation.

---

## 📦 Scope

- Audio notes for students  
- Accessibility for visually impaired users  
- CLI-based automation and batch conversion  
- Classroom-ready reproducibility and onboarding

---

## 🧱 System Overview

| Component                   | Description                                      |
|----------------------------|--------------------------------------------------|
| `pdf_to_audio_converter.py`| Core logic for PDF parsing and speech synthesis  |
| `PDFToAudioConverter`      | Class encapsulating all conversion routines      |
| `run_converter.py`         | CLI launcher with argument parsing               |

---

## 📥 Inputs

- PDF file path (`--pdf`)  
- Output MP3 filename (`--out`)  
- Optional: voice engine configuration (via `pyttsx3.init()`)

---

## 📤 Outputs

- Console logs with page previews  
- MP3 audio file  
- Word count and estimated duration  
- Page-wise text extraction summary  
- Summary report with emoji indicators

---

## ⚙️ Functional Requirements

- Load and parse PDF using `PyPDF2`  
- Extract text from each page  
- Preview first 200 characters per page  
- Synthesize text using `pyttsx3`  
- Save output as MP3  
- Show progress bar with `tqdm`  
- Estimate duration based on word count  
- Handle `KeyboardInterrupt` gracefully  
- Log errors and skip unreadable pages

---

## 🧪 Testing Strategy

Unit tests using `unittest` framework

Test cases cover:

- PDF file existence  
- Reader initialization  
- Audio conversion without exceptions  
- MP3 file creation  
- Cleanup and reproducibility  
- CLI argument parsing (via `run_converter.py`)

---

## 📦 Dependencies

```text
Python 3.11+
pyttsx3
PyPDF2
tqdm
```

## 📁 Folder Structure
```text
PDFToAudioConverter/
├── src/
│   └── pdfaudio/
│       ├── __init__.py
│       └── pdf_to_audio_converter.py
├── scripts/
│   └── run_converter.py
├── tests/
│   └── test_pdf_to_audio_converter.py
├── docs/
│   ├── specs.md
│   └── test_guide.md
├── data/
│   └── input.pdf
├── .env
└── README.md
```
## 📌 Notes
Designed for CLI use on Linux, Windows, and WSL

All routines are modular and classroom-friendly

Easily extensible for per-page audio, GUI, or batch mode