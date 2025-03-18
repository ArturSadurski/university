import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matrix_operation import generate_matrix
from count_functions import serial_count, parallel_count
from timing_utils import time_function
from bbp_pi import compute_pi_serial, compute_pi_parallel
from matrix_multiplication import generate_matrices


def test_single_case(size, low, high):
    matrix = generate_matrix(size, size, 1000)
    _, serial_time = time_function(serial_count, matrix, low, high)
    _, parallel_time = time_function(parallel_count, matrix, low, high)

    print(f"Matrix size: {size}x{size}")
    print(f"Serial execution time: {serial_time:.6f} seconds")
    print(f"Parallel execution time: {parallel_time:.6f} seconds")


def simulate_and_plot(sizes, low, high, line_style, marker):
    serial_times = []
    parallel_times = []

    for size in sizes:
        matrix = np.random.randint(1, 1000, size=(size, size))
        _, serial_time = time_function(serial_count, matrix, low, high)
        _, parallel_time = time_function(parallel_count, matrix, low, high)

        serial_times.append(serial_time)
        parallel_times.append(parallel_time)

    import pandas as pd

    data = pd.DataFrame(
        {
            "Matrix Size": sizes,
            "Serial Time": serial_times,
            "Parallel Time": parallel_times,
        }
    )

    data_melted = data.melt("Matrix Size", var_name="Type", value_name="Time")

    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.lineplot(
        x="Matrix Size",
        y="Time",
        hue="Type",
        style="Type",
        markers=True,
        dashes=False,
        data=data_melted,
    )
    plt.title("Performance Comparison")
    plt.show()


sns.set_theme(style="whitegrid")


def simulate_and_plot_pi(test_cases):
    """Przeprowadza symulację czasu obliczeń dla różnych wartości digits i rysuje wykres z Seaborn."""
    serial_times = []
    parallel_times = []

    for digits in test_cases:
        print(f"Testing digits: {digits}")

        # Seryjne obliczenia
        _, serial_time = compute_pi_serial(digits)
        serial_times.append(serial_time)

        # Równoległe obliczenia
        _, parallel_time = compute_pi_parallel(digits)
        parallel_times.append(parallel_time)

    # Tworzenie wykresu z Seaborn
    plt.figure(figsize=(10, 6))
    sns.lineplot(
        x=test_cases, y=serial_times, marker="o", label="Serial", linestyle="--"
    )
    sns.lineplot(
        x=test_cases, y=parallel_times, marker="s", label="Parallel", linestyle="--"
    )

    plt.xlabel("Digits computed", fontsize=12)
    plt.ylabel("Execution time (seconds)", fontsize=12)
    plt.title("Comparison of Serial vs Parallel Execution Time", fontsize=14)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.show()


def simulate_and_plot_matrix(test_cases):
    """Przeprowadza symulację czasu obliczeń dla różnych rozmiarów macierzy i rysuje wykres."""
    serial_times = []
    parallel_times = []

    for size in test_cases:
        print(f"Testing matrix size: {size}x{size}")

        A, B = generate_matrices(size)

        _, serial_time = multiply_serial(A, B)
        serial_times.append(serial_time)

        _, parallel_time = multiply_parallel(A, B)
        parallel_times.append(parallel_time)

    plt.figure(figsize=(10, 6))
    sns.lineplot(
        x=test_cases, y=serial_times, marker="o", label="Serial", linestyle="--"
    )
    sns.lineplot(
        x=test_cases, y=parallel_times, marker="s", label="Parallel", linestyle="--"
    )

    plt.xlabel("Matrix size (NxN)", fontsize=12)
    plt.ylabel("Execution time (seconds)", fontsize=12)
    plt.title("Comparison of Serial vs Parallel Execution Time", fontsize=14)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.show()
