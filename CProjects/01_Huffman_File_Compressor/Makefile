###############################################################################
#  File         : Makefile
#  Author       : Sanjeet Prasad
#  Email        : sanjeet8.23@gmail.com
#  Description  : Build and test automation for Huffman compression project
#                 - Builds main binary and test runner
#                 - Supports CLI execution and unit testing via Unity
#                 - Cleans up generated files in ./data/ safely
#  Date         : 22-10-2025
#  Usage        :
#     make            → Build the main binary (huffman)
#     make run        → Run the CLI with default or provided filenames
#     make test       → Compile and run unit tests (test_runner)
#     make clean      → Remove all generated files from ./data/
###############################################################################

# Compiler and flags
CC = gcc
CFLAGS = -Wall -Iinclude -DUNITY_INCLUDE_EXEC_TIME

# Source files
SRC = src/huffman.c src/main.c
TEST_SRC = test/test_huffman.c
UNITY = test/unity/unity.h  # Unity is header-only

# Directory used for all input/output test artifacts
DATA_DIR = data

# Command to safely create the data directory if it doesn't exist
MKDIR_DATA = mkdir -p $(DATA_DIR)


# Output binaries
BIN = huffman
TEST_BIN = test_runner

# Declare phony targets (not actual files)
.PHONY: all run test clean

# Default target: build main binary
all: $(BIN)

# Build main binary
$(BIN): $(SRC)
	$(CC) $(CFLAGS) -o $(BIN) $(SRC)

# Run the main program with default files in ./data/
run: $(BIN)
	$(MKDIR_DATA)
	./$(BIN)

# Build and run unit tests
test: $(TEST_SRC) src/huffman.c test/unity/unity.c
	$(MKDIR_DATA)
	$(CC) $(CFLAGS) -Itest/unity -o $(TEST_BIN) \
		$(TEST_SRC) test/unity/unity.c src/huffman.c
	./$(TEST_BIN)


# Clean up all generated files in ./data/
clean:
	rm -f $(BIN) $(TEST_BIN)
	[ -d $(DATA_DIR) ] && find $(DATA_DIR) -type f \( -name "*.bin" -o -name "*.txt" ! -name "input.txt" \) -exec rm -f {} +

# make verify : verify input file and output file(after huffman compression ) size and data mismatch
verify:
	@echo "Verifying roundtrip integrity..."
	@if [ ! -f data/input.txt ]; then \
		echo "Missing file: data/input.txt"; exit 1; \
	elif [ ! -f data/decompressed.txt ]; then \
		echo "Missing file: data/decompressed.txt"; exit 1; \
	else \
		if diff data/input.txt data/decompressed.txt > /dev/null; then \
			echo "Match confirmed: data/input.txt == data/decompressed.txt"; \
		else \
			echo "Mismatch detected between data/input.txt and data/decompressed.txt"; exit 1; \
		fi \
	fi
# make help : help how to use Makefile
help:
	@echo "Huffman Compression Project - Makefile Help"
	@echo ""
	@echo "Usage:"
	@echo "  make            : Build the main binary (huffman)"
	@echo "  make run        : Run the CLI with default or provided filenames"
	@echo "  make test       : Compile and run unit tests (test_runner)"
	@echo "  make clean      : Remove all generated files from ./data/ except input.txt"
	@echo "  make verify     : Compare input.txt and decompressed.txt for roundtrip integrity"
	@echo "  make help       : Show this help message"
