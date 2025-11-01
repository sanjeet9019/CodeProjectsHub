# 🧼 Clean List Automation: Shell List Normalizer (`clean_list.sh`)

A robust shell scripting project designed to normalize, clean, and deduplicate input lists, primarily utilizing colon (`:`) and space delimiters. This utility is designed for reliability and is fully validated via an automated test suite.

---

## 📂 Project Structure

| File/Folder | Description |
| :--- | :--- |
| **`clean_list.sh`** | **Main Script:** Performs list normalization, deduplication, and special colon handling (the core logic). |
| **`test_suite_clean_list`** | **Automated Test Suite:** Validates `clean_list.sh` against 23 comprehensive test cases. |
| `docs/clean_list_SPEC.pdf` | Formal specification of the script’s required behavior and constraints. |
| `docs/clean_list_Testing_Guide.pdf` | Annotated guide to the test suite, verification process, and grading summary. |

---

## 🛠 Features

The `clean_list.sh` script rigorously adheres to the following functional requirements:

* **Deduplication:** Removes duplicate entries while strictly **preserving the original order** of the first unique appearance.
* **Input Flexibility:** Correctly processes both **space-separated** and **colon-separated** elements.
* **Special Colon Handling:** Converts specific colon patterns to the current directory (`.`), mimicking standard environment variable behavior:
    * Leading `:` → `.`
    * Trailing `:` → `.`
    * Double `::` → `:.:` (inserts the current directory)
* **Efficiency Constraint:** The script **does not use temporary files** for processing.
* **Validation:** Fully compatible with the automated test suite for comprehensive grading/validation.

---

## Setup & Validation

### Environment

* **OS:** Ubuntu 22.04 (VirtualBox)
* **Shell:** GNU Bash
* **Date:** October 19, 2025

### Step 1: Preparation

Place the primary script (`clean_list.sh`) and the test suite (`test_suite_clean_list`) in the same directory.

### Step 2: Make Scripts Executable

Grant the necessary permissions to run the files:

```bash
chmod +x clean_list.sh
chmod +x test_suite_clean_list
```
### Step 3: Execute Automated Validation

Execute the test suite by passing the main script as the first argument:

```bash
./test_suite_clean_list ./clean_list.sh
```
