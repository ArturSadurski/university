#!/bin/bash

BASE_DIR="/home/artur_176/Big_Data/Text_Files"
TOP_N=10

count_words() {
    local FILES=$1
    if [ -z "$FILES" ]; then
        echo "No files found for analysis." >&2
        return
    fi

    cat $FILES | tr '[:upper:]' '[:lower:]' | tr -d '[:punct:]' | tr ' ' '\n' | grep -E '^[a-z]+' | sort | uniq -c | sort -nr | head -n "$TOP_N"
}

print_table() {
    echo "-------------------------------------------"
    printf "| %-20s | %-10s |\n" "Word" "Occurrences"
    echo "-------------------------------------------"
    while read -r COUNT WORD; do
        printf "| %-20s | %-10s |\n" "$WORD" "$COUNT"
    done
    echo "-------------------------------------------"
}

echo -e "\n **Most common words across all categories:**"
ALL_FILES=$(find "$BASE_DIR" -type f -name "*.txt")
RESULT=$(count_words "$ALL_FILES")
print_table <<< "$RESULT"

for CATEGORY in "$BASE_DIR"/*; do
    if [ -d "$CATEGORY" ]; then
        CATEGORY_NAME=$(basename "$CATEGORY")
        echo -e "\n **Most common words in category: $CATEGORY_NAME**"
        CATEGORY_FILES=$(find "$CATEGORY" -type f -name "*.txt")
        RESULT=$(count_words "$CATEGORY_FILES")
        print_table <<< "$RESULT"
    fi
done
