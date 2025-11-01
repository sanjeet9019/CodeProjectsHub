#!/bin/bash

##################################################################
# Script Name : fs_usage_warning.sh
# Description : A disk usage monitoring script that sends email
#               alerts when ext2/ext4 file systems exceed a
#               specified usage threshold.
# Author      : Sanjeet Prasad
# Email       : sanjeet8.23@gmail.com
# Date        : October 21, 2025
##################################################################

TEST_MODE=false  # Enable with --test

# Function to display usage instructions
show_usage() {
    echo "Usage: $0 [--test] [-c capacity-percentage] email-address [email-address] ..."
    exit 1
}

# Function to send email using mailx and here-document
send_email() {
    local subject="$1"
    local body="$2"
    for email in "${emails[@]}"; do
        if $TEST_MODE; then
            echo "$subject"
            echo
            echo "$body"
        fi
        mailx -s "$subject" "$email" <<EOF
$body
EOF
        if [[ $? -ne 0 ]]; then
            echo "Error: Failed to send email to $email"
        fi
    done
}

# Main function starts from here
main() {
    local capacity=60
    emails=()

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --test)
                TEST_MODE=true
                ;;
            -c)
                shift
                if [[ "$1" =~ ^[0-9]+$ ]]; then
                    capacity="$1"
                else
                    echo "Error: Invalid capacity percentage."
                    show_usage
                fi
                ;;
            -*)
                echo "Error: Unknown option $1"
                show_usage
                ;;
            *)
                emails+=("$1")
                ;;
        esac
        shift
    done

    if [[ ${#emails[@]} -eq 0 ]]; then
        echo "Error: No email addresses provided."
        show_usage
    fi

    # Capture df output once
    df_output=$(df -k -t ext4 -t ext2)

    # Disk snapshot block (only in normal mode)
    if ! $TEST_MODE; then
        echo "----------------------------------------"
        echo "Current ext2/ext4 Disk Usage Snapshot:"
        echo "$df_output" | awk '
        BEGIN { print "Filesystem     1K-blocks     Used Available Use% Mounted on" }
        { print $0 }
        '
        if ! echo "$df_output" | awk '$2 ~ /^ext2$/' | grep -q .; then
            echo "Note: ext2 is not supported on this system."
        fi
        echo "----------------------------------------"
    fi

    # Process disk usage
    echo "$df_output" | tail -n +2 | while read -r line; do
        usage=$(echo "$line" | awk '{print $(NF-1)}' | sed 's/%//')
        mountpoint=$(echo "$line" | awk '{print $NF}')

        if [[ "$usage" -ge "$capacity" ]]; then
			if [[ "$usage" -ge 90 ]]; then
				subject="Critical Warning: the file system $mountpoint is greater than or equal to 90% capacity"
			else
				subject="Warning: the file system $mountpoint is above $capacity % used"
			fi
            header="Filesystem     1K-blocks     Used Available Use% Mounted on"
            body="$header"$'\n'"$line"
            send_email "$subject" "$body"
        fi
    done
}

main "$@"
exit 0
