# 🎧 PDFToAudioConverter

Convert multi-page PDF documents into MP3 audio using text-to-speech synthesis. Designed for accessibility, education, and automation workflows.

---

## 🧠 Overview

PDFToAudioConverter is a Python-based CLI tool that reads text from PDF files and converts it into spoken audio using `pyttsx3`. It supports multi-page documents, console previews, progress tracking, and graceful interruption handling.

---

## 🚀 Features

- 📄 Multi-page PDF parsing with `PyPDF2`
- 🗣️ Text-to-speech synthesis via `pyttsx3`
- 💾 MP3 output generation
- 🔍 Console preview of page content (first 200 characters)
- 📊 Word count and estimated audio duration
- ⏹️ Graceful handling of `Ctrl+C` interrupts
- 🔄 Progress bar using `tqdm`

---

## 📁 Folder Structure

```text
PDFToAudioConverter/
├── src/                          # Core conversion logic
│   └── pdfaudio/
│       ├── __init__.py
│       └── pdf_to_audio_converter.py
│
├── scripts/                      # CLI launcher
│   └── run_converter.py
│
├── test/                        # Unittest-based validation
│   └── test_pdf_to_audio_converter.py
│
├── docs/                         # Specification and test guides
│   ├── specs.md
│   └── test_guide.md
│
├── data/                         # Input/output files
│   └── input.pdf                 # Sample input PDF
│
├── .env                          # Optional runtime configuration
└── README.md                     # Project overview and usage
```

## 🛠️ Installation
```bash
pip install pyttsx3 PyPDF2 tqdm
```

## 🧪 Running Tests
```bash
python -m unittest test.test_pdf_to_audio_converter
```
Or run directly:
```bash
python test/test_pdf_to_audio_converter.py
```
## 🚀 Usage
Basic conversion:
```bash
python -m scripts.run_converter
```
Custom input/output:
```bash
python -m scripts.run_converter --pdf data/input.pdf --out data/output.mp3
```
## 📦 Dependencies
```bash
Python 3.11+
pyttsx3
PyPDF2
tqdm
```
## 📚 Documentation
See docs/test_guide.md for:
- Numbered test cases and expected outputs
- Manual validation steps
- CLI walkthrough and audit strategy

