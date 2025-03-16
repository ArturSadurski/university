import time
import re

DICT_FILE = "dictionary.txt"
INPUT_FILE = "input.txt"
UNKNOWN_WORDS = "/tmp/unknown_words.txt"


def load_dictionary():
    with open(DICT_FILE, "r", encoding="utf-8") as f:
        return set(line.strip().lower() for line in f)


def extract_words():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        words = set()
        for line in f:
            words.update(word.lower() for word in re.findall(r"\b[a-zA-Z]+\b", line))
    return words


def append_to_unknown_words(input_text, unknown_words):
    with open(UNKNOWN_WORDS, "a", encoding="utf-8") as f:
        f.write(f"\nInput file: {INPUT_FILE}\n")
        with open(INPUT_FILE, "r", encoding="utf-8") as inp:
            f.write(inp.read())
        f.write("\nUnknown words:\n")
        f.write("\n".join(unknown_words))
        f.write("\n-----------------------------------\n")


def check_spelling(dictionary, words):
    unknown_words = words - dictionary
    append_to_unknown_words(INPUT_FILE, unknown_words)
    return len(unknown_words)


def main():
    start_time = time.time()
    dictionary = load_dictionary()
    words = extract_words()
    unknown_count = check_spelling(dictionary, words)
    end_time = time.time()
    print(f"Spell check completed in {end_time - start_time:.4f} seconds.")


if __name__ == "__main__":
    main()
