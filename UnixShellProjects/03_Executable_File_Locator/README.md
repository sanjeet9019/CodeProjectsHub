# 🔍 Custom Executable Locator (`custom_which.sh`)

A robust shell scripting project that emulates the Unix `which` command. This script locates executable files by checking absolute paths, relative paths, and searching through the `PATH` environment variable. It supports the `-a` flag to find all matching executables and avoids restricted commands or temporary files.

---

## 📂 Project Metadata

| Field           | Value                          |
|-----------------|--------------------------------|
| **Project**     | Custom Executable Locator (`custom_which.sh`) |
| **Author**      | Sanjeet Prasad                 |
| **Email**       | sanjeet8.23@gmail.com          |
| **Environment** | Ubuntu 22.04 (VirtualBox)      |
| **Date**        | October 19, 2025               |

---

## 🛠 Script Features

- **Command Resolution**: Locates executable files based on command names.
- **Pathname Detection**: Treats inputs with `/` as direct pathnames.
- **Permission Checks**: Validates that files are both readable and executable.
- **Directory Exclusion**: Directories are not considered valid commands.
- **Special PATH Handling**:
  - Leading `:` → current directory
  - Trailing `:` → current directory
  - Double `::` → inserts current directory
  - Explicit `.` in PATH → current directory
- **Flag Support**:
  - `-a`: Lists **all** matching executables in `PATH`
- **Constraint**: Does **not** use temporary files or restricted commands (`which`, `type`, `locate`, `ls`)

---

## 🚀 Setup Instructions

### Step 1: Preparation

Place both the main script (`custom_which.sh`) and the test suite (`test_suite_custom_which.sh`) in the same directory.

```
#chmod +x custom_which.sh
#chmod +x test_suite_custom_which.sh

```
### Step 2: Run Automated Validation

```
#./test_suite_custom_which.sh ./custom_which.sh 
#./test_suite_custom_which.sh ./custom_which.sh -v
```
All 23 test cases should pass successfully.

## Manual Sanity Checks
```
#./custom_which.sh bash
# Output: /usr/bin/bash

#./custom_which.sh -a tar
# Output:
# /bin/tar
# /usr/bin/tar

#./custom_which.sh ./myscript.sh
# Output: ./myscript.sh

#./custom_which.sh ./mydir
# Output: NOT FOUND

#./custom_which.sh unknowncmd
# Output: NOT FOUND
```

