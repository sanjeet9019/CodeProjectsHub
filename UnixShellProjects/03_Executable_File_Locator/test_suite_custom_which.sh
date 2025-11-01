#!/bin/bash

# Modified test script based on test-case1 for grading student submissions
# Usage: ./test_suite_custom_which.sh <script_to_test> [-v]

if [ $# -lt 1 ]; then
    echo "Usage: $0 <script_to_test> [-v]"
    echo "  -v: verbose output showing all test details"
    exit 1
fi

SCRIPT_TO_TEST="$1"
VERBOSE=0
if [ "$2" = "-v" ]; then
    VERBOSE=1
fi

if [ ! -f "$SCRIPT_TO_TEST" ]; then
    echo "Error: Script '$SCRIPT_TO_TEST' not found"
    exit 1
fi

# Make sure the script is executable
if [ ! -x "$SCRIPT_TO_TEST" ]; then
    chmod +x "$SCRIPT_TO_TEST"
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Test counters and grade tracking
total_tests=0
total_failed=0
total_passed=0

# Grade component tracking (updated to match new rubric - 100 points total)
program_runs=0             # 5 points - Basic functionality
flag_a_handled=0          # 15 points - -a flag implementation
colon_start_path=0        # 15 points - (:PATH) handling
double_colon_path=0       # 15 points - (::) handling  
colon_end_path=0          # 15 points - (PATH:) handling
dot_in_path=0             # 15 points - (.) handling
space_in_filename=0       # 5 points - Multiple arguments
absolute_path=0           # 5 points - Absolute path handling
relative_path=0           # 5 points - Relative path handling
directory_handling=0      # 2 points - Directory vs file distinction
directory_absolute=0      # 2 points - Absolute directory paths
directory_relative=0      # 1 point - Relative directory paths

# Find system commands dynamically like original test-case1
if [ -f /usr/bin/tar ]; then
    TAR=/usr/bin/tar
    UB=/usr/bin
else
    TAR=/bin/tar
    UB=/bin
fi

if [ -f /usr/bin/ls ]; then
    LS=/usr/bin/ls
    UB=/usr/bin
else
    LS=/bin/ls
    UB=/bin
fi

# Save original PATH
OLDPATH=$PATH

compare_results() {
    local expected="$1"
    local output="$2"
    local cmd="$3"
    local test_name="$4"
    local path_description="$5"
    local grade_component="$6"  # New parameter to identify which component this tests
    
    # Convert to uppercase for case-insensitive comparison of "NOT FOUND"
    local efound=$(echo "$expected" | tr '[:lower:]' '[:upper:]')
    local rfound=$(echo "$output" | tr '[:lower:]' '[:upper:]')
    
    local failed=0
    local RES=""
    
    case $efound in
    *"NOT FOUND"*)
        case $rfound in
        *"NOT FOUND"*)
            ((total_passed += 1))
            RES="PASSED"
            ;;
        *)
            RES="FAILED"
            failed=1
            ((total_failed += 1))
            ;;
        esac
        ;;
    *)
        if [[ "$expected" = "$output" ]]; then
            RES="PASSED"
            ((total_passed += 1))
        else
            RES="FAILED"
            failed=1
            ((total_failed += 1))
        fi
        ;;
    esac
    
    # Award points for specific components if test passed
    if [ $failed -eq 0 ]; then
        case $grade_component in
            "program") program_runs=5 ;;
            "flag_a") flag_a_handled=15 ;;
            "colon_start") colon_start_path=15 ;;
            "double_colon") double_colon_path=15 ;;
            "colon_end") colon_end_path=15 ;;
            "dot_path") dot_in_path=15 ;;
            "space_filename") space_in_filename=5 ;;
            "absolute") absolute_path=5 ;;
            "relative") relative_path=5 ;;
            "directory") directory_handling=2 ;;
            "dir_absolute") directory_absolute=2 ;;
            "dir_relative") directory_relative=1 ;;
        esac
    fi
    
    # If any test passes, award program running points (only once)
    if [ $failed -eq 0 ] && [ ${program_runs:-0} -eq 0 ]; then
        program_runs=5
    fi
    
    if [ $failed -eq 1 ]; then
        echo -e "${RED}✗ FAILED${NC}: $test_name"
        echo "  Issue: $path_description"
        echo "  PATH: $PATH"
        echo "  Command: ./$SCRIPT_TO_TEST $cmd"
        echo "  Expected: $expected"
        echo -e "  ${RED}Your script returned: $output${NC}"
        echo
    elif [ $VERBOSE -eq 1 ]; then
        echo -e "${GREEN}✓ PASSED${NC}: $test_name"
    fi
    
    ((total_tests += 1))
}

get_letter_grade() {
    local score=$1
    if [ $score -ge 94 ]; then
        echo "A"
    elif [ $score -ge 90 ]; then
        echo "A-"
    elif [ $score -ge 87 ]; then
        echo "B+"
    elif [ $score -ge 84 ]; then
        echo "B"
    elif [ $score -ge 80 ]; then
        echo "B-"
    elif [ $score -ge 77 ]; then
        echo "C+"
    elif [ $score -ge 74 ]; then
        echo "C"
    elif [ $score -ge 70 ]; then
        echo "C-"
    elif [ $score -ge 67 ]; then
        echo "D+"
    elif [ $score -ge 60 ]; then
        echo "D"
    else
        echo "F"
    fi
}

get_grade_description() {
    local score=$1
    if [ $score -ge 94 ]; then
        echo "Excellent - Handles all requirements correctly"
    elif [ $score -ge 90 ]; then
        echo "Very Good - Minor implementation details"
    elif [ $score -ge 87 ]; then
        echo "Good - Few minor issues with edge cases"
    elif [ $score -ge 84 ]; then
        echo "Good - Some minor issues with requirements"
    elif [ $score -ge 80 ]; then
        echo "Acceptable - Multiple minor issues"
    elif [ $score -ge 77 ]; then
        echo "Satisfactory - Some PATH handling problems"
    elif [ $score -ge 74 ]; then
        echo "Satisfactory - PATH handling issues"
    elif [ $score -ge 70 ]; then
        echo "Below Average - Significant PATH problems"
    elif [ $score -ge 67 ]; then
        echo "Poor - Major functionality missing"
    elif [ $score -ge 60 ]; then
        echo "Needs improvement - Major functionality missing"
    else
        echo "Significant issues - Basic requirements not met"
    fi
}

get_grade_color() {
    local score=$1
    if [ $score -ge 90 ]; then
        echo "$GREEN"
    elif [ $score -ge 80 ]; then
        echo "$BLUE"
    elif [ $score -ge 70 ]; then
        echo "$YELLOW"
    elif [ $score -ge 60 ]; then
        echo "$CYAN"
    else
        echo "$RED"
    fi
}

print_results() {
    local total_grade=$((program_runs + flag_a_handled + colon_start_path + double_colon_path + colon_end_path + dot_in_path + space_in_filename + absolute_path + relative_path + directory_handling + directory_absolute + directory_relative))
    
    local letter_grade=$(get_letter_grade $total_grade)
    local grade_description=$(get_grade_description $total_grade)
    local grade_color=$(get_grade_color $total_grade)
    
    echo
    echo "================================================"
    echo "Detailed Grade Breakdown"
    echo "================================================"
    echo "Program runs:                      $program_runs/5 points"
    echo "-a flag handling:                  $flag_a_handled/15 points"
    echo ": at start of PATH:                $colon_start_path/15 points"
    echo ":: in PATH:                        $double_colon_path/15 points"
    echo ": at end of PATH:                  $colon_end_path/15 points"
    echo ". in the PATH:                     $dot_in_path/15 points"
    echo "Multiple arguments:                $space_in_filename/5 points"
    echo "Absolute path:                     $absolute_path/5 points"
    echo "Relative path:                     $relative_path/5 points"
    echo "Directory handling:                $directory_handling/2 points"
    echo "Directory with absolute path:      $directory_absolute/2 points"
    echo "Directory with relative path:      $directory_relative/1 point"
    echo "                                   ----"
    echo "TOTAL GRADE:                       $total_grade/100 points"
    
    echo
    echo -e "${grade_color}Letter Grade: $letter_grade - $grade_description${NC}"
    
    echo
    #echo "Test Summary: $total_passed passed, $total_failed failed out of $total_tests tests"
}

# Create test files (matching original test-case1)
setup_test_files() {
    # Create a simple test directory structure
    mkdir -p class
    
    # Create test files that the original test expects
    touch no-read no-execute
    chmod -r no-read 2>/dev/null || true
    chmod -x no-execute
}

cleanup_test_files() {
    rm -rf class no-read no-execute 2>/dev/null || true
}

echo "Testing Executable File Locator: $SCRIPT_TO_TEST"
echo "================================================"

setup_test_files

echo -e "\n${YELLOW}1. Basic Command Finding${NC}"
echo "----------------------------"

# Test 1: Basic vi command (from original test)
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/bin/X11:/usr/lib:.
CMD=vi
RES=$(./"$SCRIPT_TO_TEST" $CMD 2>&1)
if [ -f /usr/bin/vi ]; then
    EXPECTED="/usr/bin/vi"
else
    EXPECTED="/bin/vi"
fi
compare_results "$EXPECTED" "$RES" "$CMD" "Basic vi command location" "Your script should find vi in the system PATH" "program"

PATH=$OLDPATH

echo -e "\n${YELLOW}2. PATH Variations & Special Cases${NC}"
echo "----------------------------------"

# Test multiple PATH configurations with specific grade components
test_count=0
path_descriptions=(
    "Standard PATH"
    "PATH with current directory at start (:)"
    "PATH with current directory in middle (::)"
    "PATH with current directory at end (:)"
    "PATH with explicit current directory (.)"
)

for tmpPath in \
    "$UB:/usr/local/bin:/usr/bin/X11" \
    ":$UB:/usr/local/bin:/usr/bin/X11" \
    "$UB::/usr/local/bin:/usr/bin/X11" \
    "$UB:/usr/local/bin:/usr/bin/X11:" \
    "$UB:/usr/local/bin:/usr/bin/X11:."
do
    ((test_count++))
    PATH=$tmpPath
    PathHasDot=0
    current_desc="${path_descriptions[$((test_count-1))]}"
    
    # Check if current directory is in PATH
    case $PATH in
    :*) PathHasDot=1 ;;
    *::*) PathHasDot=1 ;;
    *:) PathHasDot=1 ;;
    *.*) PathHasDot=1 ;;
    *) PathHasDot=0 ;;
    esac

    # Test -a flag - only award flag_a points on first test
    CMD="-a tar"
    RES=$(./"$SCRIPT_TO_TEST" $CMD 2>&1)
    
    # Build expected result by checking what tar locations exist in current PATH
    EXPECTED=""
    IFS=':' read -ra PATH_DIRS <<< "$PATH"
    for dir in "${PATH_DIRS[@]}"; do
        if [ "$dir" = "" ]; then
            dir="."
        fi
        if [ -f "$dir/tar" ] && [ -x "$dir/tar" ]; then
            if [ -z "$EXPECTED" ]; then
                EXPECTED="$dir/tar"
            else
                EXPECTED="$EXPECTED
$dir/tar"
            fi
        fi
    done
    
    if [ -z "$EXPECTED" ]; then
        EXPECTED="NOT FOUND"
    fi
    
    if [ $test_count -eq 1 ]; then
        compare_results "$EXPECTED" "$RES" "$CMD" "-a flag test ($current_desc)" "The -a flag should find ALL occurrences of tar in the PATH" "flag_a"
    else
        compare_results "$EXPECTED" "$RES" "$CMD" "-a flag test ($current_desc)" "The -a flag should find ALL occurrences of tar in the PATH" "program"
    fi

    # Test command with ./ (relative path test) - only award relative points on first test
    CMD="./tar"
    RES=$(./"$SCRIPT_TO_TEST" $CMD 2>&1)
    EXPECTED="NOT FOUND"
    if [ $test_count -eq 1 ]; then
        compare_results "$EXPECTED" "$RES" "$CMD" "Relative path test ($current_desc)" "Commands with ./ should be checked directly, not searched in PATH" "relative"
    else
        compare_results "$EXPECTED" "$RES" "$CMD" "Relative path test ($current_desc)" "Commands with ./ should be checked directly, not searched in PATH" "program"
    fi

    # Test basic command - no special points, just program functionality
    CMD=tar
    RES=$(./"$SCRIPT_TO_TEST" $CMD 2>&1)
    EXPECTED=$TAR
    compare_results "$EXPECTED" "$RES" "$CMD" "Basic command test ($current_desc)" "Should find the first tar in PATH" "program"

    # Test absolute path - only award absolute points on first test
    CMD="$TAR"
    RES=$(./"$SCRIPT_TO_TEST" $CMD 2>&1)
    EXPECTED="$TAR"
    if [ $test_count -eq 1 ]; then
        compare_results "$EXPECTED" "$RES" "$CMD" "Absolute path test ($current_desc)" "Absolute paths should be checked directly" "absolute"
    else
        compare_results "$EXPECTED" "$RES" "$CMD" "Absolute path test ($current_desc)" "Absolute paths should be checked directly" "program"
    fi

    # Test multiple commands (space in filename test) - only award space points on first test
    CMD="tar ls"
    RES=$(./"$SCRIPT_TO_TEST" $CMD 2>&1)
    EXPECTED="$TAR
$LS"
    if [ $test_count -eq 1 ]; then
        compare_results "$EXPECTED" "$RES" "$CMD" "Multiple commands ($current_desc)" "Should process each command argument separately" "space_filename"
    else
        compare_results "$EXPECTED" "$RES" "$CMD" "Multiple commands ($current_desc)" "Should process each command argument separately" "program"
    fi

    # Test script finding itself - THIS IS THE CRITICAL TEST for each PATH type
    CMD=$(basename "$SCRIPT_TO_TEST")
    RES=$(./"$SCRIPT_TO_TEST" $CMD 2>&1)
    if [ $PathHasDot -eq 1 ]; then
        EXPECTED="./$CMD"
        # Award the specific PATH component points based on which PATH we're testing
        case $test_count in
            2) compare_results "$EXPECTED" "$RES" "$CMD" "Self-reference test ($current_desc)" "Script should find itself when current directory is in PATH" "colon_start" ;;
            3) compare_results "$EXPECTED" "$RES" "$CMD" "Self-reference test ($current_desc)" "Script should find itself when current directory is in PATH" "double_colon" ;;
            4) compare_results "$EXPECTED" "$RES" "$CMD" "Self-reference test ($current_desc)" "Script should find itself when current directory is in PATH" "colon_end" ;;
            5) compare_results "$EXPECTED" "$RES" "$CMD" "Self-reference test ($current_desc)" "Script should find itself when current directory is in PATH" "dot_path" ;;
            *) compare_results "$EXPECTED" "$RES" "$CMD" "Self-reference test ($current_desc)" "Script should find itself when current directory is in PATH" "program" ;;
        esac
    else
        EXPECTED="NOT FOUND"
        compare_results "$EXPECTED" "$RES" "$CMD" "Self-reference test ($current_desc)" "Script should NOT find itself when current directory is not in PATH" "program"
    fi

    # Test with ./ prefix - no special points
    CMD="./$SCRIPT_TO_TEST"
    RES=$(./"$SCRIPT_TO_TEST" $CMD 2>&1)
    EXPECTED="./$SCRIPT_TO_TEST"
    compare_results "$EXPECTED" "$RES" "$CMD" "Direct ./ reference ($current_desc)" "Commands starting with ./ should always be found if they exist" "program"

    # Test nonexistent commands - no special points
    CMD=nonexistent_command_xyz
    RES=$(./"$SCRIPT_TO_TEST" $CMD 2>&1)
    EXPECTED="NOT FOUND"
    compare_results "$EXPECTED" "$RES" "$CMD" "Nonexistent command ($current_desc)" "Should return 'not found' message for commands that don't exist" "program"

    # Test directory (should not be executable) - only award dir_relative points on first test
    CMD=./class
    RES=$(./"$SCRIPT_TO_TEST" $CMD 2>&1)
    EXPECTED="NOT FOUND"
    if [ $test_count -eq 1 ]; then
        compare_results "$EXPECTED" "$RES" "$CMD" "Directory test ($current_desc)" "Directories should not be considered executable commands" "dir_relative"
    else
        compare_results "$EXPECTED" "$RES" "$CMD" "Directory test ($current_desc)" "Directories should not be considered executable commands" "program"
    fi

    # Test non-executable file - no special points
    CMD=no-execute
    RES=$(./"$SCRIPT_TO_TEST" $CMD 2>&1)
    EXPECTED="NOT FOUND"
    compare_results "$EXPECTED" "$RES" "$CMD" "Non-executable file ($current_desc)" "Files without execute permission should not be found" "program"

done

echo -e "\n${YELLOW}3. Additional Edge Cases${NC}"
echo "------------------------"

# Test directory with absolute path
PATH=/opt/SUNWspro/bin:$UB:/usr/dt/bin:/usr/openwin/bin:/usr/local/bin:.:/usr/ccs/bin:/usr/ucb
CMD=/usr/bin/  # Directory with absolute path
RES=$(./"$SCRIPT_TO_TEST" $CMD 2>&1)
EXPECTED="NOT FOUND"
compare_results "$EXPECTED" "$RES" "$CMD" "Directory with absolute path" "Absolute paths to directories should not be considered executable" "dir_absolute"

# Test with complex PATH
CMD=ls
RES=$(./"$SCRIPT_TO_TEST" $CMD 2>&1)
EXPECTED="$LS"
compare_results "$EXPECTED" "$RES" "$CMD" "Complex PATH test" "Should handle complex PATH with many directories" "directory"

# Test nonexistent commands with current dir in PATH
PATH=$UB:/usr/local/bin:.
CMD=nonexistent123
RES=$(./"$SCRIPT_TO_TEST" $CMD 2>&1)
EXPECTED="NOT FOUND"
compare_results "$EXPECTED" "$RES" "$CMD" "Nonexistent with current dir" "Should return not found even when current directory is in PATH" "program"

# Restore original PATH
PATH=$OLDPATH

cleanup_test_files
print_results

echo
echo "Key Features Tested:"
echo "✓ Basic command location"
echo "✓ PATH variable handling (all current directory cases)"
echo "✓ -a flag for multiple occurrences"
echo "✓ Commands with / (absolute/relative paths)"
echo "✓ Directory vs executable file distinction"
echo "✓ Permission checking"
echo "✓ Multiple command arguments"
echo "✓ Self-reference scenarios"

if [ $total_failed -gt 0 ] && [ $VERBOSE -eq 0 ]; then
    echo
    echo "Run with -v flag for detailed output on all tests"
    echo "Example: $0 $SCRIPT_TO_TEST -v"
fi
