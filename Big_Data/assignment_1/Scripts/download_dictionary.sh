#!/bin/bash

DICT_URL="https://raw.githubusercontent.com/dwyl/english-words/master/words.txt"
DICT_FILE="dictionary.txt"

echo "Downloading the dictionary..."
curl -sL "$DICT_URL" -o "$DICT_FILE"

echo "Dictionary downloaded and saved as $DICT_FILE"
