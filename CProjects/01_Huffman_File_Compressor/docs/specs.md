# 📄 Huffman File Compressor — Project Specification

**Author:** Sanjeet Prasad  
**Email:** sanjeet8.23@gmail.com  
**Language:** C (GCC)  
**Last Updated:** 22-Oct-2025

---

## 🧩 Overview

This project implements a command-line Huffman compression and decompression tool in C. It supports:

- Encoding and decoding of text files using Huffman coding
- CLI-based orchestration with automatic file handling
- File size reporting and byte-level previews
- Unit testing using the Unity framework
- Reproducible builds and test automation via Makefile

---

## 📁 Directory Structure
```text
huffman_file_compressor/
├── data/                  # ✅ All runtime files (input/output)
│   ├── input.txt          # Default input file (preserved during cleanup)
│   ├── compressed.bin     # Output of Huffman compression
│   └── decompressed.txt   # Output of Huffman decompression
├── docs/                  # ✅ Project documentation
│   ├── specs.md           # Project specification and usage guide
│   └── test_guide.md      # Unit test coverage and instructions
├── include/               # ✅ Header files
│   └── huffman.h          # Public API for Huffman routines
├── src/                   # ✅ Source code
│   ├── huffman.c          # Huffman algorithm implementation
│   └── main.c             # CLI orchestration and reporting
├── test/                  # ✅ Unit tests and test framework
│   ├── test_huffman.c     # Test cases for Huffman logic
│   └── unity.h            # Unity test framework (header-only)
├── Makefile               # ✅ Build/test automation
```
---

## 🚀 Features

- **Compression**: Encodes input text using Huffman coding and writes a `.bin` file.
- **Decompression**: Reconstructs the original file from the compressed binary.
- **CLI Interface**:
  - Accepts a single input file as argument.
  - Automatically generates compressed and decompressed filenames.
  - If no argument is provided, defaults to `data/input.txt`.
- **File Reporting**:
  - Displays original, compressed, and decompressed file sizes.
  - Shows compression ratio.
  - Previews first 32 bytes of each file.
- **Testing**:
  - Uses Unity for unit testing.
  - Includes test cases for node creation, heap operations, tree building, encoding/decoding, and edge cases.
- **Makefile Automation**:
  - `make` — builds the main binary
  - `make run` — runs the CLI with default files
  - `make test` — builds and runs unit tests
  - `make verify` — checks roundtrip integrity
  - `make clean` — removes all generated files except `input.txt`
  - `make help` — prints usage guide

---

## 🖥️ CLI Usage

```bash
./huffman <input_file>
```
Examples
```bash
./huffman data/input.txt
```
If no argument is provided:
```bash
./huffman
```
Uses:
- data/input.txt → input
- data/compressed.bin → compressed output
- data/decompressed.txt → decompressed output

## Unit Testing(Unity Framework)
Run Unit Tests
```bash
make test
```
## Sample Output
[TEST] [1] Starting test: test_create_node
PASS (3 ms)
...
[HUFFMAN]: Compression finished. Encoded output saved to: data/compressed.bin
[HUFFMAN]: Decompression finished. Restored output saved to: data/decompressed.txt

## Verify Roundtrip Integrity
```bash
make verify
```
Checks if data/decompressed.txt matches data/input.txt.

## Clean Up
```bash
make clean
```
Removes:
huffman, test_runner

All .bin and .txt files in data/ except input.txt

## Help
make help
Prints all available targets and usage instructions.

## 📚 Learn More: Huffman Compression
Huffman coding is a lossless data compression algorithm that assigns shorter binary codes to more frequent characters, optimizing space efficiency. It’s widely used in formats like ZIP, JPEG, and MP3. To understand the algorithm and its applications, refer to:
- 📘 Wikipedia: Huffman Coding