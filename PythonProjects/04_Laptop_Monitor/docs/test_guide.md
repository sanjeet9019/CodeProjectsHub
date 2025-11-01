# 🧪 LaptopMonitor – Test Guide

**Project:** LaptopMonitor  
**Filename:** `test_laptop_monitor.py`  
**Author:** Sanjeet Prasad  
**Email:** sanjeet8.23@gmail.com  
**Date:** 24-Oct-2025  
**Framework:** `unittest` (Python 3.11.0)

---

## 🎯 Purpose

This document outlines the test strategy, coverage, and execution instructions for validating the `LaptopMonitor` system monitoring tool. Each test case is labeled, numbered, and designed for reproducibility and audit clarity.

---

## 🧪 Test Strategy

- Framework: `unittest` (optionally compatible with `pytest`)
- Environment variables are overridden using `os.environ`
- Console output includes test case ID and pass/fail summary
- Verbose runner used for detailed feedback
- Temporary folders used for file monitoring tests
- `assertLogs()` used to capture disk space output

---

## 🔢 Numbered Test Cases

| ID   | Test Description                                      | Method Name                        |
|------|--------------------------------------------------------|------------------------------------|
| TC01 | Validate default ping host fallback                   | `test_01_ping_host_default`        |
| TC02 | Check MONITOR_INTERVAL type                           | `test_02_interval_type`            |
| TC03 | Ensure 'chrome' is in default PROCESS_KEYWORDS        | `test_03_process_keywords`         |
| TC04 | Override PING_HOST via .env                           | `test_04_env_override_ping_host`   |
| TC05 | Override MONITOR_INTERVAL via .env                    | `test_05_env_override_interval`    |
| TC06 | Override MAX_CYCLES via .env                          | `test_06_env_override_max_cycles`  |
| TC07 | Disable speed test via ENABLE_SPEEDTEST=false         | `test_07_env_override_speedtest_toggle` |
| TC08 | Override PROCESS_KEYWORDS with custom list            | `test_08_env_override_process_keywords` |
| TC09 | Fallback folder path should exist                     | `test_09_folder_path_fallback`     |
| TC10 | Handle empty folder in monitor_files gracefully       | `test_10_monitor_files_empty_folder` |
| TC11 | Confirm LOG_LEVEL is set to DEBUG                     | `test_11_log_level_debug`          |
| TC12 | Respect MONITOR_FOLDER_PATH override                  | `test_12_env_override_folder_path` |
| TC13 | Log disk space metrics with monitor_disk_space        | `test_13_monitor_disk_space_logs_output` |

---

## 🧪 Sample Output

```text
🧪 Running extended LaptopMonitor unit tests...

test_01_ping_host_default ... ✅ Passed
test_02_interval_type ... ✅ Passed
test_03_process_keywords ... ✅ Passed
...
----------------------------------------------------------------------
Ran 13 tests in 0.012s

OK
```
## 🚀 How to Run Tests

🔧 Using unittest

```python
PYTHONPATH=src python -m unittest discover tests
```

▶️ Run Single File
```python
PYTHONPATH=src python tests/test_laptop_monitor.py
```