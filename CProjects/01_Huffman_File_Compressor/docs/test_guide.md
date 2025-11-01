# 🧪 Test Guide — Huffman File Compressor

**Author:** Sanjeet Prasad  
**Email:** sanjeet8.23@gmail.com  
**Framework:** Unity (header-only)  
**Last Updated:** 22-Oct-2025

---

## 🎯 Purpose

This guide explains how to run, understand, and extend the unit tests for the Huffman File Compressor project. It covers:

- Test structure and coverage
- Unity framework setup
- How to run tests via `make`
- How to verify compression integrity
- Tips for writing new test cases

---

## 📁 Test Directory Structure
```text
test/
├── test_huffman.c         # ✅ Unit tests for Huffman compression logic
├── unity/                 # ✅ Embedded Unity test framework
│   ├── unity.c            # Core Unity source file
│   ├── unity.h            # Public Unity API (assert macros, test runner)
│   └── unity_internals.h  # Internal macros and lifecycle hooks
```

---

## 🧪 What’s Tested

The test suite covers:

- ✅ Node creation and frequency assignment
- ✅ Min-heap operations (insert, extract)
- ✅ Huffman tree construction
- ✅ Encoding and decoding logic
- ✅ Edge cases (empty input, single character, repeated characters)
- ✅ File roundtrip integrity (via `make verify`)

---

## 🚀 Running Tests

### 🔧 Build and Run

```bash
make test
```
This will:
Compile test_runner using Unity
Run all test cases
Print pass/fail status with execution time

## 🧪 Sample Output
[TEST] [1] Starting test: test_create_node
PASS (3 ms)

[TEST] [2] Starting test: test_build_tree
PASS (5 ms)

[HUFFMAN]: Compression finished. Encoded output saved to: data/compressed.bin

[HUFFMAN]: Decompression finished. Restored output saved to: data/decompressed.txt

## 🔍 Verifying Roundtrip Integrity
To confirm that decompression restores the original file:
```bash
make verify
```
✅ Expected Output
```code
Match confirmed: data/input.txt == data/decompressed.txt
```
❌ If Mismatch
```code
Mismatch detected between data/input.txt and data/decompressed.txt
```
## ✍️ Writing New Tests
To add a new test:

1.Open test/test_huffman.c

2.Define a new function:
```c
void test_encode_single_char(void) {
    TEST_ASSERT_EQUAL_STRING("0", encode("A"));  // Example
}
```
3.Register it in main():
```c
RUN_TEST(test_encode_single_char);
```
4.Re-run:
```bash
make test
```

## 📌 Notes
- Unity is embedded locally and requires no external installation
- All test artifacts are written to the data/ directory
- make clean removes generated test files but preserves input.txt