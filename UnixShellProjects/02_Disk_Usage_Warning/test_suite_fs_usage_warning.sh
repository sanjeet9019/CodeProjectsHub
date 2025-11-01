#!/bin/bash

##################################################################
# Test Suite for fs_usage_warning.sh
# Description : Validates disk usage alert logic and email delivery
# Author      : Sanjeet Prasad
# Email       : sanjeet8.23@gmail.com
# Date        : October 19, 2025
##################################################################

SCRIPT="./fs_usage_warning.sh"
EMAIL="sanjeet8.23@gmail.com"
total=0
passed=0
failed=0

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Show current ext2/ext4 disk usage
echo -e "${BLUE}Current ext2/ext4 Disk Usage Snapshot:${NC}"
df -T -P | awk '
BEGIN { print "Filesystem\tType\tSize\tUsed\tAvail\tUse%\tMounted on" }
$2 ~ /^ext[24]$/ { print $0 }
'
if ! df -T -P | awk '$2 ~ /^ext2$/' | grep -q .; then
    echo -e "${YELLOW}Note:${NC} ext2 is not supported on this system."
fi
echo "----------------------------------------"

# Function to run and verify output
run_test_case() {
    local name="$1"
    local threshold="$2"
    local expected_subject="$3"
    local use_mock="$4"

    ((total++))
    echo -e "${BLUE}[TEST]${NC} $name"

    if [[ "$use_mock" == "true" ]]; then
        mkdir -p mock_bin
		cat > mock_bin/df <<EOF
#!/bin/bash
cat <<DATA
Filesystem     Type  1K-blocks    Used Available Use% Mounted on
/dev/sda3      ext4  40453376  40453376        0 100% /
DATA
EOF
        chmod +x mock_bin/df

        # Inject mock_bin into PATH safely
        export PATH="$(pwd)/mock_bin:$PATH"

        output=$($SCRIPT --test -c "$threshold" "$EMAIL" 2>&1)

        # Clean up
        rm -rf mock_bin
    else
        output=$($SCRIPT --test -c "$threshold" "$EMAIL" 2>&1)
    fi

    if [[ "$output" == *"$expected_subject"* ]]; then
        echo -e "${GREEN}[PASS]${NC} $name"
        ((passed++))
    else
        echo -e "${RED}[FAIL]${NC} $name"
        echo -e "${YELLOW}Expected Subject:${NC} $expected_subject"
        echo -e "${YELLOW}Actual Output:${NC}\n$output"
        ((failed++))
    fi
    echo "----------------------------------------"
}

# Run live tests against real disk usage
run_test_case "Trigger warning at 10%" 10 "Warning: the file system / is above 10 % used"
run_test_case "Trigger warning at 20%" 20 "Warning: the file system / is above 20 % used"
run_test_case "Trigger warning at 30%" 30 "Warning: the file system / is above 30 % used"
run_test_case "Trigger warning at 40%" 40 "Warning: the file system / is above 40 % used"
run_test_case "Trigger warning at 50%" 50 "Warning: the file system / is above 50 % used"
run_test_case "Trigger warning at 60%" 60 "Warning: the file system / is above 60 % used"
run_test_case "Trigger warning at 70%" 70 "Warning: the file system / is above 70 % used"
run_test_case "Trigger warning at 80%" 80 "Warning: the file system / is above 80 % used"

# Run mock tests for critical alerts
run_test_case "Mock critical at 90%" 90 "Critical Warning: the file system / is greater than or equal to 90% capacity" true
run_test_case "Mock critical at 100%" 100 "Critical Warning: the file system / is greater than or equal to 90% capacity" true

# Summary
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Test Suite Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "Total Tests: $total"
echo -e "Passed: ${GREEN}$passed${NC}"
echo -e "Failed: ${RED}$failed${NC}"
