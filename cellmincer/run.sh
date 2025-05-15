#!/bin/bash

process_files() {
    # Check if files.txt exists
    if [[ ! -f "files.txt" ]]; then
        echo "Error: files.txt not found."
        exit 1
    fi

    # Iterate over each line in files.txt
    while IFS= read -r file; do
        # Skip empty lines
        [[ -z "$file" ]] && continue
        echo "$script: $file"
        # Run preprocess.sh on the file
        "$script" "$file"
    done < files.txt
}

script="./preprocess.sh"
process_files

script="./denoise.sh"
process_files
