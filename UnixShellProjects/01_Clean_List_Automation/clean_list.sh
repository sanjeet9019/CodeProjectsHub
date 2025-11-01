#!/bin/bash

########################################################################
# Script Name : clean_list.sh
# Description : Cleans a colon-separated list by removing duplicates,
#               applying special colon rules, and preserving order.
#               Handles leading/trailing colons and double colons,
#               and supports space-separated input.
# Author      : Sanjeet Prasad
# Email       : sanjeet8.23@gmail.com
# Date        : October 19, 2025
########################################################################

#-----------------------------#
# Function: normalize_input   #
#-----------------------------#
normalize_input() {
    local input="$*"

    # Convert space-separated to colon-separated
    input="${input// /:}"

    # Count trailing colons (preserved as empty fields)
    local trailing=""
    if [[ "$input" =~ (:)+$ ]]; then
        trailing="${BASH_REMATCH[0]}"
    fi
    local trailing_count=0
    [[ -n "$trailing" ]] && trailing_count=$(awk -v s="$trailing" 'BEGIN{print length(s)}')

    # Split into array using colon
    local IFS=':'
    read -ra raw_items <<< "$input"

    local normalized=()
    for item in "${raw_items[@]}"; do
        if [[ -z "$item" ]]; then
            normalized+=(".")
        else
            normalized+=("$item")
        fi
    done

    # Append one '.' for each trailing colon dropped
    for ((i=0; i<trailing_count; i++)); do
        normalized+=(".")
    done

    local IFS=':'
    echo "${normalized[*]}"
}

#-----------------------------#
# Function: clean_list        #
#-----------------------------#
clean_list() {
    local normalized
    normalized=$(normalize_input "$@")

    local IFS=':'
    read -ra items <<< "$normalized"

    declare -A seen
    local output=()

    for item in "${items[@]}"; do
        [[ -z "$item" ]] && continue

        # Allow only one '.' entry
        if [[ "$item" == "." ]]; then
            if [[ -z "${seen[$item]}" ]]; then
                seen["$item"]=1
                output+=("$item")
            fi
            continue
        fi

        # Deduplicate all other entries
        if [[ -z "${seen[$item]}" ]]; then
            seen["$item"]=1
            output+=("$item")
        fi
    done

    local IFS=':'
    echo "${output[*]}"
}

#-----------------------------#
# Main Execution              #
#-----------------------------#
clean_list "$@"