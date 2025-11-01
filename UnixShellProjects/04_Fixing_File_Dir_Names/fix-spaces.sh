#!/bin/bash

##################################################################
# Script Name : fix-spaces.sh
# Description : Recursively renames files and/or directories by
#               replacing spaces with dashes in their names.
#               Supports options to rename only files (-f),
#               only directories (-d), or both.
#               Uses provided utility functions for modular design:
#               - pathname(): returns directory part of path
#               - basename(): returns filename part of path
#               - find_files(): finds files with spaces
#               - find_dirs(): finds directories with spaces
#               - my_rename(): renames a file or directory safely
# Author      : Sanjeet Prasad
# Email       : sanjeet8.23@gmail.com
# Date        : October 18, 2025
##################################################################

#-----------------------------#
# Function: show_usage       #
#-----------------------------#
show_usage() {
    echo "Usage: $0 [-f] [-d] directory-name"
    echo "  -f    Rename files only"
    echo "  -d    Rename directories only"
    echo "  Both -f and -d may be specified together"
    exit 1
}

#-----------------------------#
# Utility: pathname          #
#-----------------------------#
pathname() {
    echo "${1%/*}"
}

#-----------------------------#
# Utility: basename          #
#-----------------------------#
basename() {
    echo "${1##*/}"
}

#-----------------------------#
# Utility: find_dirs         #
#-----------------------------#
find_dirs() {
    find "$1" -depth -type d -name "* *"
}

#-----------------------------#
# Utility: find_files        #
#-----------------------------#
find_files() {
    find "$1" -depth -type f -name "* *"
}

#-----------------------------#
# Function: my_rename        #
#-----------------------------#
my_rename() {
    local old_path="$1"
    local new_path="$2"
    local parent_dir

    parent_dir="$(pathname "$old_path")"

    if [ ! -w "$parent_dir" ]; then
        echo "Error: Cannot write to directory '$parent_dir'"
        return 1
    fi

    if [ -e "$new_path" ]; then
        echo "Warning: '$new_path' already exists. Skipping."
        return 1
    fi

    mv "$old_path" "$new_path"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to rename '$old_path' to '$new_path'"
        return 1
    else
        echo "Renamed: '$old_path' → '$new_path'"
        return 0
    fi
}

#-----------------------------#
# Function: fix_files        #
#-----------------------------#
fix_files() {
    find_files "$target_dir" | while IFS= read -r file; do
        base=$(basename "$file")
        dir=$(pathname "$file")
        new_base="${base// /-}"
        new_path="$dir/$new_base"
        my_rename "$file" "$new_path"
    done
}

#-----------------------------#
# Function: fix_dirs         #
#-----------------------------#
fix_dirs() {
    find_dirs "$target_dir" | while IFS= read -r dir_path; do
        base=$(basename "$dir_path")
        parent=$(pathname "$dir_path")
        new_base="${base// /-}"
        new_path="$parent/$new_base"
        my_rename "$dir_path" "$new_path"
    done
}

#-----------------------------#
# Main function starts here  #
#-----------------------------#
main() {
    rename_files=false
    rename_dirs=false

    # Parse options
    while [[ "$1" == -* ]]; do
        case "$1" in
            -f) rename_files=true ;;
            -d) rename_dirs=true ;;
            *) echo "Invalid option: $1"; show_usage ;;
        esac
        shift
    done

    # Check if directory is provided
    if [ $# -ne 1 ]; then
        echo "Error: Directory name missing."
        show_usage
    fi

    target_dir="$1"

    # Validate special directories
    if [ "$target_dir" = "." ] || [ "$target_dir" = ".." ]; then
        echo "Error: Cannot process special directories '.' or '..'"
        exit 1
    fi

    # Validate directory existence
    if [ ! -d "$target_dir" ]; then
        echo "Error: '$target_dir' is not a valid directory."
        exit 1
    fi

    # Ensure at least one flag is set
    if ! $rename_files && ! $rename_dirs; then
        echo "Error: Must specify at least -f or -d"
        show_usage
    fi

    # Call appropriate fix functions
    $rename_files && fix_files
    $rename_dirs && fix_dirs
}

# Call main
main "$@"
exit 0

