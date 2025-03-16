#!/bin/bash

DICT_FILE="dictionary.txt"
INPUT_FILE="input.txt"  # Bez przekazywania jako argument
TEMP_WORDS="/tmp/words.txt"
UNKNOWN_WORDS="/tmp/unknown_words.txt"
START_TIME=$(date +%s.%N)

if [[ ! -f "$DICT_FILE" ]]; then
    exit 1
fi

if [[ ! -f "$INPUT_FILE" ]]; then
    exit 1
fi

awk '{print tolower($0)}' "$DICT_FILE" | sort -u > /tmp/dictionary_set.txt
grep -oE '\w+' "$INPUT_FILE" | tr '[:upper:]' '[:lower:]' | sort -u > "$TEMP_WORDS"

UNKNOWN=$(comm -23 "$TEMP_WORDS" /tmp/dictionary_set.txt)

echo -e "\nInput file: $INPUT_FILE" >> "$UNKNOWN_WORDS"
cat "$INPUT_FILE" >> "$UNKNOWN_WORDS"
echo -e "\nUnknown words:" >> "$UNKNOWN_WORDS"
echo "$UNKNOWN" >> "$UNKNOWN_WORDS"
echo "-----------------------------------" >> "$UNKNOWN_WORDS"

END_TIME=$(date +%s.%N)
EXECUTION_TIME=$(echo "$END_TIME - $START_TIME" | bc)

echo "Spell check completed in $EXECUTION_TIME seconds."
