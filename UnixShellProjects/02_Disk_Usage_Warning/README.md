# 🔍 Disk Usage Warning Script (`fs_usage_warning.sh`)

A reliable shell script that monitors ext2/ext4 file systems and sends email alerts when disk usage exceeds a specified threshold. It supports both live alerting and test mode for validation, and includes mock testing for critical usage scenarios.

---

## 📂 Project Metadata

| Field           | Value                                  |
|-----------------|----------------------------------------|
| **Project**     | Disk Usage Warning Script (`fs_usage_warning.sh`) |
| **Author**      | Sanjeet Prasad                         |
| **Email**       | sanjeet8.23@gmail.com                  |
| **Environment** | Ubuntu 22.04 (VirtualBox)              |
| **Date**        | October 19, 2025                       |

---

## 🛠 Script Features

-  **Threshold-Based Alerts**: Warns when usage exceeds a user-defined percentage.
-  **Critical Alert Logic**: Triggers critical warnings at ≥ 90% usage.
-  **Filesystem Filtering**: Monitors only ext2/ext4 file systems.
-  **Email Delivery**: Sends formatted alerts via `mailx`.
-  **Test Mode**:
  - `--test`: Prints alert output instead of sending emails.
-  **Disk Snapshot**: Displays current ext2/ext4 usage in normal mode.
-  **Mock Testing Support**: Simulates high usage for critical alert validation.
-  **Constraint**: Does **not** use temporary files or external monitoring tools.

---

## 🚀 Setup Instructions

### Step 1: Preparation

Place both the main script (`fs_usage_warning.sh`) and the test suite (`test_suite_fs_usage.sh`) in the same directory.

```
chmod +x fs_usage_warning.sh
chmod +x test_suite_fs_usage.sh
```
### Step 2: Run Automated Validation

```
./test_suite_fs_usage.sh 
```
All 10 test cases should pass successfully:

8 live tests (10%–80%)
2 mock tests simulating 99% usage

Manual Sanity Checks

```
./fs_usage_warning.sh --test -c 80 sanjeet8.23@gmail.com
# Output:
# Warning: the file system / is above 80 % used
# Filesystem    Type    Size    Used    Avail   Use%    Mounted on
# /dev/sda3    ext4   ...

./fs_usage_warning.sh --test -c 100 sanjeet8.23@gmail.com
# Output: (none if usage < 100%)

./fs_usage_warning.sh -c 80 sanjeet8.23@gmail.com
# Sends real email alert if usage ≥ 80%
```
### Final Test Result Summary
Total Tests Run: 10

Passed:  All tests passed

Manual Checks: Verified