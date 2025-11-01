# 🖥️ LaptopMonitor

A modular, CLI-based Python tool for real-time system diagnostics including disk usage, ping latency, process monitoring, and optional internet speed testing. Built for embedded systems educators, testers, and students working in Linux and Windows environments.

---

## 🧠 Purpose

This project provides a hands-on system monitor for exploring OS-level diagnostics such as disk usage, network latency, process activity, and folder scanning. It’s designed for:

- 📚 Classroom demonstrations  
- 🧪 Student assignments  
- 🛠️ Embedded and systems validation workflows

---

## 📁 Project Structure

```text
LaptopMonitor/
├── src/                          # Core monitoring logic
│   └── laptopmonitor/
│       ├── __init__.py
│       ├── laptop_monitor.py
│
├── scripts/                      # CLI launcher
│   └── run_monitor.py
│
├── tests/                        # Unittest-based validation
│   └── test_laptop_monitor.py
│
├── docs/                         # Specification and test guides
│   ├── specs.md
│   └── test_guide.md
│
├── .env                          # Runtime configuration
└── README.md                     # Project overview and usage
```

---

## 🚀 Getting Started
✅ Prerequisites Python 3.11+

Required packages:
```python 
pip install psutil ping3 speedtest-cli python-dotenv
```

---

## ▶️ Run the Monitor
```python 
python scripts/run_monitor.py
```
Loads .env, initializes LaptopMonitor, and runs all enabled diagnostics.

---

## 🧪 Run Unit Tests
```python
PYTHONPATH=src python -m unittest discover tests -v
```
Or run directly with summary:
```python
PYTHONPATH=src python tests/test_laptop_monitor.py
```

Expected output:

Test Summary:
```text
Total tests run   : 13
Tests passed      : 13
Tests failed      : 0
Tests with errors : 0
```
---

## 📚 Documentation
See docs/test_guide.md for:

- Numbered test cases and expected outputs
- Manual validation steps
- CLI walkthrough and audit strategy