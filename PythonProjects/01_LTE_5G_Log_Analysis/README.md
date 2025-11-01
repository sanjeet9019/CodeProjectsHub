# 📡 LTE & NR Log Analyzer (`lte_nr_log_analyzer.py`)

A robust Python-based analyzer for telecom engineers and students, designed to extract LTE signal metrics and decode 5G NR UE capability logs. This utility is modular, reproducible, and validated via an automated test suite.

---

## 📂 Project Structure

| File/Folder                     | Description                                                                 |
|--------------------------------|-----------------------------------------------------------------------------|
| `src/lte_nr_log_analyzer.py`   | **Main Analyzer Script:** Extracts LTE RSRP/CQI values, message blocks, and NR band combinations. |
| `test/test_lte_nr_log_analyzer.py` | **Automated Test Suite:** Validates LTE and NR analyzers against 4 core test cases using `pytest`. |
| `data/LTENetworkLogs.txt`      | Sample LTE log file for signal and message parsing.                        |
| `data/UECapabilityInfo.txt`    | Sample NR capability file for band and combination extraction.            |
| `docs/lte_5g_log_analysis_specs.pdf`                | Formal specification of the analyzer’s behavior and CLI structure.        |
| `docs/lte_5g_log_analysis_test_guide.pdf`           | Annotated guide to the test suite, validation logic, and classroom usage. |

---

## 🛠 Features

The `lte_nr_log_analyzer.py` script adheres to the following functional requirements:

### LTE Analysis
- Extracts `RSRP = -XX` and `CQI = XX` values from logs.
- Identifies and prints message block from `MSG2` to `MSG3`.

### NR Analysis
- Extracts supported `bandNR: XX` entries from UE Capability logs.
- Groups bands into combinations using `featureSetCombination` markers.

### CLI Support
- Accepts `--lte` and `--nr` arguments for selective or combined analysis.
- Defaults to analyzing both if no arguments are passed.

### Formatted Output
- Uses `tabulate` for clean tabular display.
- Logs all actions with timestamps using Python’s `logging` module.

---

## 🧪 Setup & Validation

### Environment
- **OS:** Ubuntu 22.04 or Windows 11 (WSL or native)
- **Interpreter:** Python 3.11+
- **Date:** October 22, 2025

### Step 1: Install Dependencies

```bash
pip install tabulate pytest
```
### Step 2: Run Analyzer
Run both (default):
```bash
py src/lte_nr_log_analyzer.py
```
Run LTE only:
```bash
py src/lte_nr_log_analyzer.py --lte data/LTENetworkLogs.txt
```
Run NR only:
```bash
py src/lte_nr_log_analyzer.py --nr data/UECapabilityInfo.txt
```
Run with custom paths:
```bash
py src/lte_nr_log_analyzer.py --lte path/to/lte_log.txt --nr path/to/nr_log.txt
```
### Step 3: Execute Automated Tests
```bash
pytest test/test_lte_nr_log_analyzer.py
```
👨‍💻 Author
Sanjeet Prasad
📧 sanjeet8.23@gmail.com 
🔗 LinkedIn: sanjeet9019 
