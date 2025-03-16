#!/bin/bash

URL="https://ghtorrent.org/downloads.html"
TMP_FILE="/tmp/links.txt"

echo "Pobieranie strony..."
curl -sL "$URL" > /tmp/page.html

echo "Wyciąganie linków..."
grep -oP '(?<=href=\")[^\"]+' /tmp/page.html | grep -E '^http' > "$TMP_FILE"

echo "Znalezione linki:"
cat "$TMP_FILE"

echo "Sprawdzanie linków..."
while read -r link; do
    status=$(curl -o /dev/null --silent --head --write-out '%{http_code}' "$link")
    echo "Link: $link - Status: $status"
    if [ "$status" -eq 404 ]; then
        echo "BŁĄD: $link zwraca 404"
    fi
done < "$TMP_FILE"

rm "$TMP_FILE"
echo "Sprawdzanie zakończone."
