#!/bin/bash

##################################################################
# Script Name: custom_which.sh
# Description: A custom implementation of the Unix 'which' command.
#              This script locates executable files by checking
#              absolute paths, relative paths, and searching through
#              the PATH environment variable. It supports the -a flag
#              to find all matching executables.
#              It avoids using restricted commands like which, type,
#              locate, or ls, and does not use temporary files.
# Author: Sanjeet Prasad
# Email: sanjeet8.23@gmail.com
# Date: October 19, 2025
##################################################################

#-----------------------------#
# Function: check_executable #
#-----------------------------#
check_executable() {
    local cmd="$1"
    local found=0

    # If command contains a slash, treat as pathname
    if [[ "$cmd" == */* ]]; then
        if [ -d "$cmd" ]; then
            return 1
        elif [ -f "$cmd" ] && [ -r "$cmd" ] && [ -x "$cmd" ]; then
            echo "$cmd"
            return 0
        else
            return 1
        fi
    else
        # Only check current directory if PATH includes it
        if [[ ":$PATH:" == *::* || ":$PATH:" == *:.:* || "$PATH" == :* || "$PATH" == *: ]]; then
            if [ -f "./$cmd" ] && [ -r "./$cmd" ] && [ -x "./$cmd" ] && [ ! -d "./$cmd" ]; then
                echo "./$cmd"
                return 0
            fi
        fi

        # Split PATH into array
        IFS=':' read -ra path_dirs <<< "$PATH"
        for path in "${path_dirs[@]}"; do
            [ -z "$path" ] && path="."  # Handle empty PATH entries
            full_path="$path/$cmd"
            if [ -f "$full_path" ] && [ -r "$full_path" ] && [ -x "$full_path" ] && [ ! -d "$full_path" ]; then
                echo "$full_path"
                found=1
                [ "$all_matches" = true ] || return 0
            fi
        done
        [ "$found" -eq 1 ] && return 0 || return 1
    fi
}

#-----------------------------#
# Main Execution              #
#-----------------------------#
main() {
    all_matches=false

    # Check for -a flag
    if [ "$1" = "-a" ]; then
        all_matches=true
        shift
    fi

    # No commands provided
    if [ $# -eq 0 ]; then
        echo "Usage: $0 [-a] command1 [command2 ...]"
        exit 1
    fi

    # Process each command
    for cmd in "$@"; do
        check_executable "$cmd"
        if [ $? -ne 0 ]; then
            echo "NOT FOUND"
        fi
    done
}

main "$@"
exit 0