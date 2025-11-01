# 📘 Software Specification Document

**Project:** LaptopMonitor  
**Filename:** `laptop_monitor.py`  
**Author:** Sanjeet Prasad  
**Email:** sanjeet8.23@gmail.com  
**Date:** 24-Oct-2025  
**Version:** 1.0  
**Interpreter:** Python 3.11.0

---

## 1. 🎯 Purpose

LaptopMonitor is a cross-platform CLI tool that provides real-time system diagnostics including disk usage, network latency, active processes, and optional speed testing. It is designed for educational use, reproducible classroom workflows, and automation-friendly integration.

---

## 2. 📦 Scope

Intended for:

- Embedded systems educators and students  
- Linux/Windows developers and testers  
- CLI tool builders and automation engineers  
- Classroom labs and reproducible teaching scripts

---

## 3. 🧱 System Overview

| Component             | Description                                      |
|----------------------|--------------------------------------------------|
| `laptop_monitor.py`  | Core monitoring logic and environment parsing    |
| `LaptopMonitor`      | Class encapsulating all monitoring routines      |
| `run_monitor.py`     | CLI launcher with `.env` loading and user guidance|

---

## 4. 📥 Inputs

Configured via `.env` or environment variables:

- `PING_HOST` (e.g., `google.com`)  
- `MONITOR_INTERVAL` (seconds)  
- `MAX_CYCLES` (0 = unlimited)  
- `MONITOR_FOLDER_PATH` (absolute or relative path)  
- `ENABLE_SPEEDTEST` (`true` or `false`)  
- `LOG_LEVEL` (`INFO`, `DEBUG`, etc.)  
- `PROCESS_KEYWORDS` (comma-separated list)

---

## 5. 📤 Outputs

- Disk usage summary (Total, Used, Free, Usage %)  
- Ping latency to target host  
- Speed test results (Download, Upload, Ping)  
- File count and size in monitored folder  
- Active process matches with keyword filtering

---

## 6. ⚙️ Functional Requirements

- Load configuration from `.env` or fallback defaults  
- Inject `src/` into `sys.path` for modular imports  
- Monitor disk space using `psutil.disk_usage()`  
- Ping target host using `ping3.ping()`  
- Run speed test using `speedtest-cli` (if enabled)  
- Scan folder for file count and total size  
- Match running processes against keyword list  
- Log all outputs with timestamp and severity level

---

## 7. 🧪 Testing Strategy

Unit tests using `unittest` framework

10 test cases covering:

- `.env` overrides and default fallbacks  
- Disk space logging  
- Folder path resolution  
- Speed test toggle behavior  
- Process keyword matching  
- Type and value assertions  
- Empty folder handling  
- Logging level configuration  
- Ping host override  
- Symbolic path resolution

Console output includes test case ID, description, and pass/fail summary

---

## 8. 📦 Dependencies

```text
Python 3.11+
psutil
ping3
speedtest-cli
python-dotenv
```
## 9. 📁 Folder Structure
```text
LaptopMonitor/
├── src/
│   └── laptopmonitor/
│       ├── __init__.py
│       ├── laptop_monitor.py
├── scripts/
│   └── run_monitor.py
├── tests/
│   └── test_laptop_monitor.py
├── docs/
│   ├── specs.md
│   └── test_guide.md
├── .env
├── README.md
```

## 10. 📌 Notes

- Designed for Linux and Windows environments
- All monitoring routines are non-blocking and cycle-limited
- .env guidance is printed at runtime for onboarding
- Folder path resolution supports symbolic and absolute paths