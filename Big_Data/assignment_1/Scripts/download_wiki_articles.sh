#!/bin/bash


BASE_DIR="/home/artur_176/Big_Data/Text_Files"
ARTICLES_PER_CATEGORY=5

mkdir -p "$BASE_DIR"

CATEGORIES=(
    "Machine_learning"
    "Artificial_intelligence"
    "Computer_science"
    "Physics"
    "Mathematics"
    "History"
    "Geography"
    "Biology"
    "Chemistry"
    "Economics"
)

is_redirect() {
    local TITLE="$1"
    REDIRECT_CHECK=$(curl -s "https://en.wikipedia.org/w/api.php?action=query&titles=${TITLE// /_}&redirects&format=json" | jq -r '.query.pages | to_entries[].value.redirect')
    if [[ "$REDIRECT_CHECK" != "null" ]]; then
        return 0  # Jest przekierowaniem
    fi
    return 1  # Nie jest przekierowaniem
}

get_random_articles() {
    CATEGORY="$1"
    CATEGORY_DIR="${BASE_DIR}/${CATEGORY}"  
    mkdir -p "$CATEGORY_DIR" 

    ARTICLES=$(curl -s "https://en.wikipedia.org/w/api.php?action=query&format=json&list=categorymembers&cmtitle=Category:${CATEGORY// /_}&cmlimit=50" | jq -r '.query.categorymembers[].title')
    
    if [ -z "$ARTICLES" ]; then
        echo "Brak artykułów w kategorii: $CATEGORY" >&2
        return
    fi

    FILTERED_ARTICLES=$(echo "$ARTICLES" | grep -E -v "^(Category:|Portal:|List of )")

    SELECTED_ARTICLES=$(echo "$FILTERED_ARTICLES" | shuf -n "$ARTICLES_PER_CATEGORY")

    while IFS= read -r RANDOM_ARTICLE; do
        if is_redirect "$RANDOM_ARTICLE"; then
            echo "Pomijam przekierowanie: $RANDOM_ARTICLE"
            continue
        fi

        ARTICLE_TEXT=$(curl -s "https://en.wikipedia.org/api/rest_v1/page/html/${RANDOM_ARTICLE// /_}" | w3m -dump -T text/html)

        if [[ -z "$ARTICLE_TEXT" || "$ARTICLE_TEXT" == "/w/rest.php/v1/page/"* ]]; then
            echo "Niepoprawna treść artykułu: $RANDOM_ARTICLE" >&2
            continue
        fi

        SAFE_FILENAME="${CATEGORY_DIR}/$(echo "$RANDOM_ARTICLE" | tr ' /' '_-').txt"

        echo "$ARTICLE_TEXT" > "$SAFE_FILENAME"
        echo "Zapisano: $SAFE_FILENAME"
    done <<< "$SELECTED_ARTICLES"
}

for CATEGORY in "${CATEGORIES[@]}"; do
    get_random_articles "$CATEGORY"
done

echo "Zakończono pobieranie artykułów."
