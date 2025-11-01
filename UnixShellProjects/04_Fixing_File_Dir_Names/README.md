# fix-spaces.sh

## 📌 Description
`fix-spaces.sh` is a Bash script that recursively renames files and/or directories by replacing spaces in their names with dashes (`-`). It supports selective renaming via flags and handles nested structures, multiple spaces, and permission constraints.

---

## 🧑‍💻 Author
- **Name**: Sanjeet Prasad  
- **Email**: sanjeet8.23@gmail.com  
- **Date**: October 18, 2025  
- **Environment**: Ubuntu 22.04 (VirtualBox)

---

## ⚙️ Usage

```bash
./fix-spaces.sh [-f] [-d] directory-name

Options:
  -f : Rename files only
  -d : Rename directories only

Both -f and -d can be used together

Example:
./fix-spaces.sh -f -d TestDir

```

## Features
- Replaces spaces with dashes in names
- Handles deeply nested directories
- Skips special directories (. and ..)
- Avoids overwriting existing files
- Skips non-writable paths
- No temporary files used

## Sample Before & After
```text
Before:
TestDir/
├── a b
├── E F/
│   └── G H/
│       └── J    K/
│           └── a b

After:
TestDir/
├── a-b
├── E-F/
│   └── G-H/
│       └── J----K/
│           └── a-b
```

## Testing
To validate the script, use the automated test suite:
```bash
./test_suite_fix_spaces.sh fix-spaces.sh
```
All tests should pass with a grade estimate in the A range.