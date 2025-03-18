import os
import time
import pickle
from collections import Counter
import matplotlib.pyplot as plt
from multiprocessing import Pool, cpu_count


def count_words_in_file(file_path):
    """Zlicza słowa w pojedynczym pliku."""
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    words = content.split()
    return Counter(words)


def process_files_serially(directory):
    """Przetwarza pliki seryjnie, zliczając słowa i generując histogram."""
    start_time = time.time()
    total_words = Counter()
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            words_count = count_words_in_file(file_path)
            total_words.update(words_count)
    duration = time.time() - start_time
    return total_words, duration


def process_files_in_parallel(directory):
    """Przetwarza pliki równolegle."""
    start_time = time.time()
    pool = Pool(processes=cpu_count())
    files = [
        os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".txt")
    ]
    all_counts = pool.map(count_words_in_file, files)
    total_words = Counter()
    for count in all_counts:
        total_words.update(count)
    duration = time.time() - start_time
    pool.close()
    pool.join()
    return total_words, duration


def plot_histogram(word_counts, top_n=30):
    """Rysuje histogram najczęściej występujących słów."""
    top_words = word_counts.most_common(top_n)
    words, counts = zip(*top_words)
    plt.figure(figsize=(10, 8))
    plt.bar(words, counts)
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    plt.title("Top words in books")
    plt.xticks(rotation=45)
    plt.show()


def main():
    books_directory = (
        "/home/artur_176/university/Big_Data/assignment_3/Scripts/downloaded_books"
    )

    # Przetwarzanie seryjne
    total_words_serial, time_serial = process_files_serially(books_directory)
    print(f"Serial processing took {time_serial:.2f} seconds.")

    # Przetwarzanie równoległe
    total_words_parallel, time_parallel = process_files_in_parallel(books_directory)
    print(f"Parallel processing took {time_parallel:.2f} seconds.")

    with open("results_serial.pkl", "wb") as f:
        pickle.dump((total_words_serial, time_serial), f)

    with open("results_parallel.pkl", "wb") as f:
        pickle.dump((total_words_parallel, time_parallel), f)


if __name__ == "__main__":
    main()
