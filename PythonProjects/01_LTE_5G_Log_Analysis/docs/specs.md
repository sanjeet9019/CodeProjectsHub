# 📘 Software Specification Document

**Project:** LTE & NR Log Analyzer  
**Filename:** `lte_nr_log_analyzer.py`  
**Author:** Sanjeet Prasad  
**Date:** 22-Oct-2025  
**Version:** 1.0

---

## 1. 🎯 Purpose

This tool is designed to analyze LTE and 5G NR log files to extract key network metrics and capabilities. It supports:

- Parsing LTE logs to extract RSRP and CQI values and identify message sequences (MSG2 to MSG3)
- Parsing NR UE Capability logs to extract supported NR bands and band combinations
- Providing a command-line interface (CLI) for flexible input
- Logging structured output for traceability
- Displaying results in a clean, tabulated format

---

## 2. 📦 Scope

This script is intended for:

- Telecom engineers analyzing LTE/5G logs
- Students learning about wireless protocol behavior
- Automated grading or validation of log parsing assignments
- Integration into larger test automation frameworks

---

## 3. 🧱 System Overview

| Component        | Description                                                                 |
|------------------|------------------------------------------------------------------------------|
| `LTELogAnalyzer` | Extracts RSRP/CQI values and MSG2–MSG3 message blocks from LTE logs         |
| `NRLogAnalyzer`  | Extracts supported NR bands and band combinations from UE Capability logs   |
| `argparse`       | Enables CLI-based input of file paths                                       |
| `logging`        | Provides structured logs with timestamps and severity levels                |
| `tabulate`       | Formats output into readable tables                                         |

---

## 4. 📥 Inputs

| Input Type | Description                                      |
|------------|--------------------------------------------------|
| `--lte`    | Path to LTE log file (default: `data/LTENetworkLogs.txt`) |
| `--nr`     | Path to NR capability file (default: `data/UECapabilityInfo.txt`) |

---

## 5. 📤 Outputs

| Output Type   | Description                                                                 |
|---------------|------------------------------------------------------------------------------|
| Console Logs  | Tabulated RSRP/CQI values, LTE message block, NR bands, and combinations    |
| Logging       | INFO/WARNING/ERROR messages with timestamps                                 |
| Exit Code     | Always 0 (non-zero codes can be added for CI integration)                   |

---

## 6. ⚙️ Functional Requirements

### 6.1 LTE Analysis

- Extract all `RSRP = -XX` and `CQI = XX` values from LTE logs
- Identify and print message block from `MSG2` to `MSG3`
- Display results in a table using `tabulate`

### 6.2 NR Analysis

- Extract all `bandNR: XX` entries before `supportedBandCombinationList`
- Extract band combinations between `supportedBandCombinationList` and `appliedFreqBandListFilter`
- Group bands under each `featureSetCombination`

### 6.3 CLI & Logging

- Accept custom file paths via `--lte` and `--nr`
- Log all actions using `logging` with levels: INFO, WARNING, ERROR
- Handle missing files gracefully

---

## 7. 🧪 Testing Strategy

- Unit tests written using `pytest` in `test/test_lte_nr_log_analyzer.py`
- Temporary files simulate LTE and NR logs

### Test Coverage Includes:
- RSRP/CQI extraction
- MSG2–MSG3 parsing
- NR band list extraction
- NR band combination grouping

---

## 8. 📦 Dependencies

| Package   | Purpose           |
|-----------|-------------------|
| `tabulate`| Table formatting  |
| `pytest`  | Unit testing      |
| `argparse`| CLI parsing       |
| `logging` | Structured logs   |

### Install with:

```bash
pip install tabulate pytest
```
9. 📁 Folder Structure
```text
01_LTE_5G_Log_Analysis/
├── src/
│   ├── __init__.py
│   └── lte_nr_log_analyzer.py
├── data/
│   ├── LTENetworkLogs.txt
│   └── UECapabilityInfo.txt
├── test/
│   └── test_lte_nr_log_analyzer.py
├── docs/
│   ├── specs.md
│   └── test_guide.md

