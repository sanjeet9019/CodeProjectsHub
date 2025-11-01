# 📡 LTE & NR Log Analyzer (`lte_nr_log_analyzer.py`) – Test and Verification Guide

| Field       | Value                                           |
|-------------|--------------------------------------------------|
| Project     | LTE & NR Log Analyzer (`lte_nr_log_analyzer.py`) |
| Author      | Sanjeet Prasad                                  |
| Email       | sanjeet8.23@gmail.com                           |
| Environment | Ubuntu 22.04 (VirtualBox) / Windows 11          |
| Date        | October 22, 2025                                |

---

## 1. 🧠 Script Functionality Specification

The `lte_nr_log_analyzer.py` script processes LTE and NR log files to extract signal metrics and capability information.

### Core Features

- **LTE Analysis**
  - Extracts `RSRP = -XX` and `CQI = XX` values
  - Prints message block from `MSG2` to `MSG3`

- **NR Analysis**
  - Extracts supported `bandNR: XX` entries
  - Groups bands into combinations using `featureSetCombination`

- **CLI Support**
  - Accepts `--lte` and `--nr` arguments
  - Defaults to analyzing both if no arguments are passed

- **Output Format**
  - Tabulated results using `tabulate`
  - Structured logging with timestamps

---

## 2. ✅ Verification Steps

### Step 1: Preparation

Ensure the following files are present:

- `src/lte_nr_log_analyzer.py`
- `test/test_lte_nr_log_analyzer.py`
- `data/LTENetworkLogs.txt`
- `data/UECapabilityInfo.txt`

### Install Dependencies

```bash
pip install tabulate pytest
```
### Step 2: Automated Validation
Run the full test suite:
```bash
pytest test/test_lte_nr_log_analyzer.py
```
## ✅ Test Suite Results (4 Tests)
| Test ID | Test Focus                  | Status  |
|---------|-----------------------------|---------|
| T1      | LTE Signal Extraction       | Passed  |
| T2      | LTE Message Block Detection | Passed  |
| T3      | NR Band Extraction          | Passed  |
| T4      | NR Band Combination Parsing | Passed  |

### Step 3: 🔍 Manual Sanity Check
Command	Expected Output	Status
| Command                                                   | Expected Output             | Status   |
|-----------------------------------------------------------|-----------------------------|----------|
| `py src/lte_nr_log_analyzer.py`                           | LTE + NR tabulated results | Verified |
| `py src/lte_nr_log_analyzer.py --lte data/LTENetworkLogs.txt` | LTE results only            | Verified |
| `py src/lte_nr_log_analyzer.py --nr data/UECapabilityInfo.txt` | NR results only             | Verified |


## 3. 📁 Folder Structure
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
```
### ✅ Final Test Result Summary
All automated and manual tests passed successfully on both Ubuntu Linux and Windows 11 environments.
