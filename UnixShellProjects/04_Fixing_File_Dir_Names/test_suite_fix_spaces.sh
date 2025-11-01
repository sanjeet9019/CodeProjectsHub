#!/bin/bash

# Automated Test Script for fix_spaces.sh 
# Tests the fix_space.sh implementation against all required functionality

SCRIPT_NAME="fix_spaces"
TEST_DIR_BASE="TestDir"
PASSED=0
FAILED=0
TOTAL_POINTS=0
MAX_POINTS=100
SHOW_INFO=false  # log_info disable for output

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_test() {
    echo -e "${BLUE}[TEST]${NC} $1"
}

log_pass() {
    echo -e "${GREEN}[PASS]${NC} $1"
    ((PASSED++))
}

log_fail() {
    echo -e "${RED}[FAIL]${NC} $1"
    ((FAILED++))
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_info() {
    if [ "$SHOW_INFO" = true ]; then
        echo -e "${BLUE}[INFO]${NC} $1"
    fi
}


# Cleanup function
cleanup() {
    log_info "Cleaning up test files..."
    if [ -d "$TEST_DIR_BASE" ]; then
        rm -rf "$TEST_DIR_BASE"
        log_info "Removed test directory: $TEST_DIR_BASE"
    fi
    
    # Clean up any other test directories that might have been created
    for test_dir in "Test Dir" "readonly test" "Multiple    Spaces" "NoSpaces"; do
        if [ -d "$test_dir" ]; then
            rm -rf "$test_dir"
            log_info "Removed test directory: $test_dir"
        fi
    done
    
    log_info "Cleanup completed"
}

# Create test structure
create_test_structure() {
    local base_dir="$1"
    
    # Remove existing test directory if present
    rm -rf "$base_dir" 2>/dev/null
    
    # Create directory structure with spaces
    mkdir -p "$base_dir/E F/G H/J    K"
    
    # Create files with spaces
    touch "$base_dir/a b"
    touch "$base_dir/E F/a b"
    touch "$base_dir/E F/G H/a b"
    touch "$base_dir/E F/G H/J    K/a b"
    
    # Create some files without spaces for comparison
    touch "$base_dir/normal_file"
    touch "$base_dir/E F/another_normal"
    
    # Create files with multiple spaces
    touch "$base_dir/multiple   spaces"
    touch "$base_dir/E F/more    spaces"
}

# Check if script exists and make it executable
check_script_exists() {
    log_test "Checking if script exists"
    
    if [ ! -f "$SCRIPT_NAME" ]; then
        log_fail "Script '$SCRIPT_NAME' not found"
        return 1
    fi
    
    log_pass "Script exists"
    
    # Make script executable
    log_test "Making script executable"
    if chmod +x "$SCRIPT_NAME" 2>/dev/null; then
        log_pass "Script made executable"
        return 0
    else
        log_fail "Failed to make script executable"
        return 1
    fi
}

# Test script syntax
check_syntax() {
    log_test "Checking script syntax"
    
    if bash -n "$SCRIPT_NAME" 2>/dev/null; then
        log_pass "Script syntax is valid"
        return 0
    else
        log_fail "Script has syntax errors"
        bash -n "$SCRIPT_NAME"
        return 1
    fi
}

# Run a test and capture exit code
run_test_command() {
    local test_name="$1"
    local command="$2"
    local expected_exit="$3"
    local points="$4"
    
    log_test "$test_name"
    log_info "Command: $command"
    
    # Run command and capture exit code
    eval "$command" >/dev/null 2>&1
    local actual_exit=$?
    
    if [ "$actual_exit" -eq "$expected_exit" ]; then
        log_pass "Exit code correct (expected $expected_exit, got $actual_exit)"
        ((TOTAL_POINTS += points))
        return 0
    else
        log_fail "Exit code incorrect (expected $expected_exit, got $actual_exit)"
        return 1
    fi
}

# Test error conditions
test_error_conditions() {
    log_info "=== Testing Error Conditions ==="
    
    run_test_command "No arguments" "./$SCRIPT_NAME" 1 3
    run_test_command "No directory specified" "./$SCRIPT_NAME -f" 1 3
    run_test_command "Current directory" "./$SCRIPT_NAME -f ." 1 3
    run_test_command "Parent directory" "./$SCRIPT_NAME -f .." 1 3
    run_test_command "No flags specified" "./$SCRIPT_NAME '$TEST_DIR_BASE'" 1 3
    run_test_command "Invalid flag" "./$SCRIPT_NAME -x '$TEST_DIR_BASE'" 1 2
    run_test_command "Non-existent directory" "./$SCRIPT_NAME -f 'NonExistentDir123'" 1 3
}

# Test basic functionality
test_basic_functionality() {
    log_info "=== Testing Basic Functionality ==="
    
    # Test files only
    log_test "Testing -f (files only) option"
    create_test_structure "$TEST_DIR_BASE"
    
    if ./$SCRIPT_NAME -f "$TEST_DIR_BASE" >/dev/null 2>&1; then
        # Check if files were renamed but directories weren't
        if [ -f "$TEST_DIR_BASE/a-b" ] && [ -d "$TEST_DIR_BASE/E F" ]; then
            log_pass "Files renamed, directories unchanged (-f option works)"
            ((TOTAL_POINTS += 15))
        else
            log_fail "Files not properly renamed with -f option"
        fi
    else
        log_fail "-f option failed to execute"
    fi
    
    # Test directories only
    log_test "Testing -d (directories only) option"
    create_test_structure "$TEST_DIR_BASE"
    
    if ./$SCRIPT_NAME -d "$TEST_DIR_BASE" >/dev/null 2>&1; then
        # Check if directories were renamed but files weren't
        if [ -d "$TEST_DIR_BASE/E-F" ] && [ -f "$TEST_DIR_BASE/a b" ]; then
            log_pass "Directories renamed, files unchanged (-d option works)"
            ((TOTAL_POINTS += 15))
        else
            log_fail "Directories not properly renamed with -d option"
        fi
    else
        log_fail "-d option failed to execute"
    fi
    
    # Test both files and directories
    log_test "Testing -f -d (both files and directories) option"
    create_test_structure "$TEST_DIR_BASE"
    
    if ./$SCRIPT_NAME -f -d "$TEST_DIR_BASE" >/dev/null 2>&1; then
        # Check if both files and directories were renamed
        if [ -f "$TEST_DIR_BASE/a-b" ] && [ -d "$TEST_DIR_BASE/E-F" ]; then
            log_pass "Both files and directories renamed (-f -d option works)"
            ((TOTAL_POINTS += 20))
        else
            log_fail "Not all files and directories properly renamed with -f -d option"
        fi
    else
        log_fail "-f -d option failed to execute"
    fi
}

# Test space replacement logic
test_space_replacement() {
    log_info "=== Testing Space Replacement Logic ==="
    
    create_test_structure "$TEST_DIR_BASE"
    ./$SCRIPT_NAME -f -d "$TEST_DIR_BASE" >/dev/null 2>&1
    
    # Check multiple consecutive spaces
    log_test "Testing multiple consecutive spaces replacement"
    if [ -f "$TEST_DIR_BASE/multiple---spaces" ]; then
        log_pass "Multiple spaces correctly replaced with multiple dashes"
        ((TOTAL_POINTS += 10))
    else
        log_fail "Multiple spaces not correctly replaced"
    fi
    
    # Check that normal files without spaces are unchanged
    log_test "Testing that files without spaces are unchanged"
    if [ -f "$TEST_DIR_BASE/normal_file" ]; then
        log_pass "Files without spaces remain unchanged"
        ((TOTAL_POINTS += 5))
    else
        log_fail "Files without spaces were incorrectly modified"
    fi
}

# Test nested directory structures
test_nested_structures() {
    log_info "=== Testing Nested Directory Structures ==="
    
    create_test_structure "$TEST_DIR_BASE"
    ./$SCRIPT_NAME -f -d "$TEST_DIR_BASE" >/dev/null 2>&1
    
    # Check deep nesting
    log_test "Testing deeply nested structure processing"
    if [ -d "$TEST_DIR_BASE/E-F/G-H/J----K" ] && [ -f "$TEST_DIR_BASE/E-F/G-H/J----K/a-b" ]; then
        log_pass "Deeply nested structures processed correctly"
        ((TOTAL_POINTS += 15))
    else
        log_fail "Deeply nested structures not properly processed"
        log_info "Expected: $TEST_DIR_BASE/E-F/G-H/J----K/a-b"
        find "$TEST_DIR_BASE" -type f 2>/dev/null | head -10
    fi
}

# Test for common implementation mistakes
test_implementation_issues() {
    log_info "=== Testing for Common Implementation Issues ==="
    
    # Check if script uses temporary files (not allowed)
    log_test "Checking for temporary file usage"
    create_test_structure "$TEST_DIR_BASE"
    
    # Monitor for temp file creation during execution
    temp_files_before=$(ls /tmp/ 2>/dev/null | wc -l)
    ./$SCRIPT_NAME -f -d "$TEST_DIR_BASE" >/dev/null 2>&1
    temp_files_after=$(ls /tmp/ 2>/dev/null | wc -l)
    
    if [ "$temp_files_after" -gt "$temp_files_before" ]; then
        log_fail "Script appears to create temporary files (prohibited)"
        ((TOTAL_POINTS -= 10))
    else
        log_pass "No temporary files detected"
        ((TOTAL_POINTS += 5))
    fi
}

# Test permissions and error handling
test_permissions() {
    log_info "=== Testing Permission Handling ==="
    
    # Create a read-only directory
    mkdir -p "$TEST_DIR_BASE/readonly test"
    touch "$TEST_DIR_BASE/readonly test/test-file"
    chmod 444 "$TEST_DIR_BASE/readonly test"
    
    log_test "Testing read-only directory handling"
    ./$SCRIPT_NAME -f "$TEST_DIR_BASE" >/dev/null 2>&1
    
	chmod 755 "$TEST_DIR_BASE/readonly test"
	chmod 444 "$TEST_DIR_BASE/readonly test/test-file"
	
	readonly_dir="$TEST_DIR_BASE/readonly test"
	readonly_file="$readonly_dir/test-file"

	if [ -d "$readonly_dir" ] && [ -f "$readonly_file" ]; then
		log_pass "Permission issues handled gracefully"
		((TOTAL_POINTS += 5))
	elif [ -d "$TEST_DIR_BASE/readonly-test" ] || [ -f "$TEST_DIR_BASE/readonly-test/test-file" ]; then
		log_fail "Read-only directory or file was renamed (should not happen)"
	else
		log_warn "Permission handling unclear"
	fi
    
    # Restore permissions for cleanup
    chmod 755 "$TEST_DIR_BASE/readonly test" 2>/dev/null
}

# Main test execution
main() {
    log_info "Starting fix_space.sh Tests"
    log_info "Testing script: $SCRIPT_NAME"
    echo "=================================================="
    
    # Setup
    trap cleanup EXIT
    
    log_info "Test files will be automatically cleaned up after testing"
    
    # Prerequisites
    if ! check_script_exists; then
        log_fail "Cannot proceed without script file"
        exit 1
    fi
    
    if ! check_syntax; then
        log_fail "Cannot proceed with syntax errors"
        exit 1
    fi
    
    # Core tests
    test_error_conditions
    test_basic_functionality
    test_space_replacement
    test_nested_structures
    test_implementation_issues
    test_permissions
    
    # Results
    echo "=================================================="
    log_info "Test Results Summary"
    echo "Tests Passed: $PASSED"
    echo "Tests Failed: $FAILED"
	if [ "$TOTAL_POINTS" -gt "$MAX_POINTS" ]; then
    TOTAL_POINTS=$MAX_POINTS
	fi
    echo "Estimated Points: $TOTAL_POINTS / $MAX_POINTS"
    
    if [ "$TOTAL_POINTS" -ge 90 ]; then
        echo -e "${GREEN}Grade Estimate: A range${NC}"
    elif [ "$TOTAL_POINTS" -ge 80 ]; then
        echo -e "${BLUE}Grade Estimate: B range${NC}"
    elif [ "$TOTAL_POINTS" -ge 70 ]; then
        echo -e "${YELLOW}Grade Estimate: C range${NC}"
    else
        echo -e "${RED}Grade Estimate: Below C${NC}"
    fi
    
    # Cleanup before exit
    cleanup
    
    if [ "$FAILED" -eq 0 ]; then
        log_pass "All tests passed!"
        exit 0
    else
        log_warn "Some tests failed. Review implementation."
        exit 1
    fi
}

# Check if script name was provided as argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 <script-name>"
    echo "Example: $0 fix_spaces"
    echo ""
    echo "This script will test the provided script against all given fix-space requirements docs"
    exit 1
fi

SCRIPT_NAME="$1"

# Usage information
if [ "$SCRIPT_NAME" = "-h" ] || [ "$SCRIPT_NAME" = "--help" ]; then
    echo "Usage: $0 <script-name>"
    echo "Example: $0 fix_spaces"
    echo ""
    echo "Tests the fix_spaces script implementation against all fix-space requirements docs."
    echo "The script will be automatically made executable during testing."
    exit 0
fi

# Call main
main "$@"
