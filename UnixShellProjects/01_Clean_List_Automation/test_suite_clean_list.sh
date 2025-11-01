#!/bin/bash

# Enhanced Grading Script for clean_list Assignment
# Usage: ./test_suite_clean_list.sh [-e] [-v] [-s] <developed_script>
# -e: Show only errors (failed tests)
# -v: Verbose output with detailed explanations
# -s: Show summary statistics only

# Initialize counters and flags
total_tests=0
total_passed=0
total_failed=0
error_only=0
verbose=0
summary_only=0
max_points=100
earned_points=0

# Test categories and their weights
declare -A category_weights=(
    ["basic"]=15
    ["special_cases"]=35
    ["deduplication"]=30
    ["order_preservation"]=15
    ["edge_cases"]=5
)

declare -A category_tests=(
    ["basic"]=0
    ["special_cases"]=0
    ["deduplication"]=0
    ["order_preservation"]=0
    ["edge_cases"]=0
)

declare -A category_passed=(
    ["basic"]=0
    ["special_cases"]=0
    ["deduplication"]=0
    ["order_preservation"]=0
    ["edge_cases"]=0
)

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to apply special case conversions to expected results
# This ensures we're testing against the correct expected output
apply_special_cases() {
    local input="$1"
    local result="$input"
    
    # Convert leading : to .:
    result="${result/#:/.}"
    
    # Convert trailing : to :.
    result="${result/%:/.}"
    
    # Convert :: to .:.
    result="${result//::/.:.}"
    
    echo "$result"
}

# Function to simulate clean_list behavior for expected results
# This applies the full clean_list logic to generate correct expected outputs
generate_expected_output() {
    local input_args="$1"
    
    # Split arguments and process each one
    local all_elements=()
    local seen_elements=()
    
    # Convert input arguments to array
    IFS=' ' read -ra args <<< "$input_args"
    
    for arg in "${args[@]}"; do
        # Apply special cases first
        arg=$(apply_special_cases "$arg")
        
        # Split by colon and space
        local elements
        IFS=':' read -ra colon_split <<< "$arg"
        elements=()
        
        for element in "${colon_split[@]}"; do
            # Further split by space if needed
            IFS=' ' read -ra space_split <<< "$element"
            elements+=("${space_split[@]}")
        done
        
        # Add to all_elements if not already seen (deduplication)
        for element in "${elements[@]}"; do
            if [[ " ${seen_elements[*]} " != *" $element "* ]]; then
                seen_elements+=("$element")
                all_elements+=("$element")
            fi
        done
    done
    
    # Join with colons
    local IFS=':'
    echo "${all_elements[*]}"
}

# Function to compare results
cmp_results() {
    local expected="$1"
    local actual="$2"
    local test_case="$3"
    local category="$4"
    local description="$5"
    local points="$6"
    
    local passed=0
    ((total_tests++))
    ((category_tests[$category]++))
    
    if [[ "$expected" = "$actual" ]]; then
        ((total_passed++))
        ((category_passed[$category]++))
        ((earned_points += points))
        passed=1
        status="${GREEN}PASSED${NC}"
    else
        ((total_failed++))
        passed=0
        status="${RED}FAILED${NC}"
    fi
    
    if [[ $summary_only -eq 0 ]]; then
        # Only show failed tests with detailed explanation
        if [[ $passed -eq 0 ]]; then
            echo -e "\n${RED}FAILED TEST:${NC} $description"
            echo -e "${BLUE}Category:${NC} $category"
            echo -e "${BLUE}Command:${NC} $PROGRAM $test_case"
            echo -e "${BLUE}Expected:${NC} '$expected'"
            echo -e "${BLUE}Actual:${NC}   '$actual'"
            
            # Provide specific failure analysis
            case $category in
                "basic")
                    echo -e "${RED}Issue:${NC} Basic input/output conversion failure"
                    ;;
                "special_cases")
                    echo -e "${RED}Issue:${NC} Special case conversion not handled correctly"
                    if [[ "$test_case" == :* ]]; then
                        echo -e "${RED}Note:${NC} Leading colon should become leading dot"
                    fi
                    if [[ "$test_case" == *: ]]; then
                        echo -e "${RED}Note:${NC} Trailing colon should become trailing dot"
                    fi
                    if [[ "$test_case" == *::* ]]; then
                        echo -e "${RED}Note:${NC} Double colon should become colon-dot-colon"
                    fi
                    ;;
                "deduplication")
                    echo -e "${RED}Issue:${NC} Duplicate removal not working correctly"
                    echo -e "${RED}Note:${NC} Should preserve first occurrence of each element"
                    ;;
                "order_preservation")
                    echo -e "${RED}Issue:${NC} Original order not preserved"
                    echo -e "${RED}Note:${NC} Elements should appear in order of first occurrence"
                    ;;
                "edge_cases")
                    echo -e "${RED}Issue:${NC} Script doesn't handle unusual input robustly"
                    ;;
            esac
            echo "----------------------------------------"
        fi
    fi
}

# Function to run a test with timeout
run_test() {
    local test_input="$1"
    timeout 5s $PROGRAM $test_input 2>&1
}

# Parse command line arguments
while getopts "vs" opt; do
    case $opt in
        v) verbose=1 ;;
        s) summary_only=1 ;;
        \?) echo "Usage: $0 [-v] [-s] <student_script>" >&2; exit 1 ;;
    esac
done
shift $((OPTIND-1))

# Check if script argument is provided
if [[ $# -eq 0 ]]; then
    echo "Usage: $0 [-v] [-s] <student_script>" >&2
    exit 1
fi

PROGRAM="$1"

# Check if the script exists and is executable
if [[ ! -f "$PROGRAM" ]]; then
    echo -e "${RED}Error: Script '$PROGRAM' not found${NC}" >&2
    exit 1
fi

chmod +x "$PROGRAM" 2>/dev/null

echo -e "${BLUE}Testing script: $PROGRAM${NC}"
echo -e "${BLUE}Total possible points: $max_points${NC}"
echo "========================================"

# Basic functionality tests (15 points)
echo -e "\n${YELLOW}BASIC FUNCTIONALITY TESTS${NC}"
echo -e "Tests ability to handle basic colon/space conversion and simple input/output"

# Test 1: Single colon (empty list)
TC=":"
ERES="."
RES=$(run_test "$TC")
cmp_results "$ERES" "$RES" "$TC" "basic" "Single colon should become dot" 3

# Test 2: Simple space-separated list
TC="apple orange pear peach"
ERES="apple:orange:pear:peach"
RES=$(run_test "$TC")
cmp_results "$ERES" "$RES" "$TC" "basic" "Space-separated list conversion" 4

# Test 3: Simple colon-separated list (no changes needed)
TC="/usr/bin:/bin"
ERES="/usr/bin:/bin"
RES=$(run_test "$TC")
cmp_results "$ERES" "$RES" "$TC" "basic" "Colon-separated list preservation" 3

# Test 4: Mixed input with spaces and colons
TC=": ."
ERES="."
RES=$(run_test "$TC")
cmp_results "$ERES" "$RES" "$TC" "basic" "Colon and dot handling" 3

# Test 5: Basic concatenation
TC="a b c"
ERES="a:b:c"
RES=$(run_test "$TC")
cmp_results "$ERES" "$RES" "$TC" "basic" "Basic space to colon conversion" 3

# Test 6: No arguments (edge case)
TC=""
ERES=""
RES=$(run_test "$TC")
cmp_results "$ERES" "$RES" "$TC" "basic" "Empty input handling" 4

# Special cases tests (35 points)
echo -e "\n${YELLOW}SPECIAL CASES TESTS${NC}"
echo -e "Tests the three critical special cases: leading :, trailing :, and :: conversions"

# Test 7: Leading colon
TC=":a b c"
ERES=".:a:b:c"
RES=$(run_test "$TC")
cmp_results "$ERES" "$RES" "$TC" "special_cases" "Leading colon becomes leading dot" 5

# Test 8: Trailing colon
TC="a b c:"
ERES="a:b:c:."
RES=$(run_test "$TC")
cmp_results "$ERES" "$RES" "$TC" "special_cases" "Trailing colon becomes trailing dot" 5

# Test 9: Double colon in middle
TC="a b::c"
ERES="a:b:.:c"
RES=$(run_test "$TC")
cmp_results "$ERES" "$RES" "$TC" "special_cases" "Double colon becomes colon-dot-colon" 5

# Test 10: Multiple special cases with deduplication
# Input: ":a b::c:" 
# After special cases: ".:a b:.:c:." (leading : -> .:, :: -> :.:, trailing : -> :.)
# After space->colon: ".:a:b:.:c:."
# After deduplication: ".:a:b:c" (remove duplicate dots)
TC=":a b::c:"
ERES=".:a:b:c"
RES=$(run_test "$TC")
cmp_results "$ERES" "$RES" "$TC" "special_cases" "Multiple special cases combined with deduplication" 5

# Test 11: Complex special case
TC="a :b c"
ERES="a:.:b:c"
RES=$(run_test "$TC")
cmp_results "$ERES" "$RES" "$TC" "special_cases" "Colon with spaces around it" 5

# Test 12: Another complex case
TC="a b: c"
ERES="a:b:.:c"
RES=$(run_test "$TC")
cmp_results "$ERES" "$RES" "$TC" "special_cases" "Trailing colon with following elements" 5

# Deduplication tests (30 points)
echo -e "\n${YELLOW}DEDUPLICATION TESTS${NC}"
echo -e "Tests removal of duplicate elements while preserving first occurrence"

# Test 13: Simple duplication
TC="a a a a a aa"
ERES="a:aa"
RES=$(run_test "$TC")
cmp_results "$ERES" "$RES" "$TC" "deduplication" "Remove duplicate elements" 5

# Test 14: Complex deduplication with order preservation
TC="mar mary mar mark mary martin"
ERES="mar:mary:mark:martin"
RES=$(run_test "$TC")
cmp_results "$ERES" "$RES" "$TC" "deduplication" "Complex deduplication preserving order" 5

# Test 15: Deduplication with special characters
TC="acb:a.b:c:b:a:acb:a"
ERES="acb:a.b:c:b:a"
RES=$(run_test "$TC")
cmp_results "$ERES" "$RES" "$TC" "deduplication" "Deduplication with dots and colons" 5

# Test 16: FIXED - PATH-like deduplication with special case handling
# The key fix: when we have duplicate arguments with trailing ::, 
# the special case conversion should happen BEFORE deduplication
TC="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin::"
# After special case conversion, both become the same thing ending with :.
# After deduplication, only the first occurrence should remain
ERES="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:."
RES=$(run_test "$TC")
cmp_results "$ERES" "$RES" "$TC" "deduplication" "PATH variable deduplication with special cases" 5

# Test 17: Mixed case deduplication
TC=".a:.:a:c:ba:a"
ERES=".a:.:a:c:ba"
RES=$(run_test "$TC")
cmp_results "$ERES" "$RES" "$TC" "deduplication" "Deduplication with leading dots" 5

# Order preservation tests (15 points)
echo -e "\n${YELLOW}ORDER PRESERVATION TESTS${NC}"

# Test 18: Order preservation with deduplication
TC=":a b c a b c . :a b c a b"
ERES=".:a:b:c"
RES=$(run_test "$TC")
cmp_results "$ERES" "$RES" "$TC" "order_preservation" "Order preservation with complex input" 5

# Test 19: Order preservation with special cases
TC="martin mar mary mar mark mary martin:"
ERES="martin:mar:mary:mark:."
RES=$(run_test "$TC")
cmp_results "$ERES" "$RES" "$TC" "order_preservation" "Order preservation with trailing colon" 5

# Test 20: Complex order preservation
TC="x yx yxx . yx xx yxxx xxxx yxxxxx: x:xx:xxx:xxxx:xxxxx yx:yxx:yxxx:yxxxx:yxxxxx"
ERES="x:yx:yxx:.:xx:yxxx:xxxx:yxxxxx:xxx:xxxxx:yxxxx"
RES=$(run_test "$TC")
cmp_results "$ERES" "$RES" "$TC" "order_preservation" "Complex order preservation" 5

# Edge cases tests (5 points)
echo -e "\n${YELLOW}EDGE CASES TESTS${NC}"
echo -e "Tests unusual inputs and robustness (minimal weight)"

# Test 21: Only dots and colons
TC=". : :: :"
ERES="."
RES=$(run_test "$TC")
cmp_results "$ERES" "$RES" "$TC" "edge_cases" "Only special characters" 3

# Test 22: Very long string elements
TC="very_long_string_element_12345 very_long_string_element_12345 short"
ERES="very_long_string_element_12345:short"
RES=$(run_test "$TC")
cmp_results "$ERES" "$RES" "$TC" "edge_cases" "Long string deduplication" 4

# Test 23: Complex real-world example
TC="ab ab ac ae af xy yx ab ba ZZyx xx yxxx xxxx yxxxxx x:xx:xxx:xxxx:xxxxx yx:yxx:yxxx:yxxxx:yxxxxx ."
ERES="ab:ac:ae:af:xy:yx:ba:ZZyx:xx:yxxx:xxxx:yxxxxx:x:xxx:xxxxx:yxx:yxxxx:."
RES=$(run_test "$TC")
cmp_results "$ERES" "$RES" "$TC" "edge_cases" "Complex real-world scenario" 3

# Calculate and display results
echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}GRADING SUMMARY${NC}"
echo -e "${BLUE}========================================${NC}"

for category in "${!category_weights[@]}"; do
    if [[ ${category_tests[$category]} -gt 0 ]]; then
        category_percentage=$((${category_passed[$category]} * 100 / ${category_tests[$category]}))
        category_points=$((${category_weights[$category]} * ${category_passed[$category]} / ${category_tests[$category]}))
        
        # Category descriptions
        case $category in
            "basic")
                desc="Basic input/output conversion (colon/space handling)"
                ;;
            "special_cases") 
                desc="Leading :, trailing :, and :: conversions"
                ;;
            "deduplication")
                desc="Removing duplicates while preserving first occurrence"
                ;;
            "order_preservation")
                desc="Maintaining original element order during processing"
                ;;
            "edge_cases")
                desc="Unusual inputs and robustness"
                ;;
        esac
        
        echo -e "Category: ${YELLOW}$category${NC} - $desc"
        echo -e "  Tests: ${category_passed[$category]}/${category_tests[$category]} (${category_percentage}%)"
        echo -e "  Points: $category_points/${category_weights[$category]}"
    fi
done

percentage=$((total_passed * 100 / total_tests))
echo -e "\n${BLUE}OVERALL RESULTS:${NC}"
echo -e "Tests Passed: ${GREEN}$total_passed${NC}/$total_tests (${percentage}%)"
echo -e "Tests Failed: ${RED}$total_failed${NC}/$total_tests"
echo -e "Points Earned: ${GREEN}$earned_points${NC}/$max_points"

# Determine letter grade
if [[ $earned_points -ge 94 ]]; then
    grade="A"
elif [[ $earned_points -ge 90 ]]; then
    grade="A-"
elif [[ $earned_points -ge 87 ]]; then
    grade="B+"
elif [[ $earned_points -ge 84 ]]; then
    grade="B"
elif [[ $earned_points -ge 80 ]]; then
    grade="B-"
elif [[ $earned_points -ge 77 ]]; then
    grade="C+"
elif [[ $earned_points -ge 74 ]]; then
    grade="C"
elif [[ $earned_points -ge 70 ]]; then
    grade="C-"
elif [[ $earned_points -ge 67 ]]; then
    grade="D+"
elif [[ $earned_points -ge 60 ]]; then
    grade="D"
else
    grade="F"
fi

echo -e "Letter Grade: ${YELLOW}$grade${NC}"

# Check for special requirements
echo -e "\n${BLUE}REQUIREMENT CHECKS:${NC}"
if grep -q "tmp\|temp" "$PROGRAM" 2>/dev/null; then
    echo -e "${RED}WARNING: Script appears to use temporary files (automatic deduction)${NC}"
fi

if [[ ! -x "$PROGRAM" ]]; then
    echo -e "${RED}WARNING: Script is not executable${NC}"
fi

echo -e "\n${BLUE}========================================${NC}"