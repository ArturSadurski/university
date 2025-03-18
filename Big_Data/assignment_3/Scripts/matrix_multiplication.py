import numpy as np
import multiprocessing
from numba import njit, prange
import time


def generate_matrices(size):
    """Generuje dwie losowe macierze o podanym rozmiarze."""
    A = np.random.rand(size, size)
    B = np.random.rand(size, size)
    return A, B


# 🚀 **1. Implementacja z `np.dot()`**
def multiply_np_dot(A, B):
    """Mnożenie macierzy za pomocą zoptymalizowanej funkcji NumPy."""
    start_time = time.time()
    result = np.dot(A, B)
    duration = time.time() - start_time
    return result, duration


# 🚀 **2. Własna implementacja mnożenia macierzy (Seryjna)**
def multiply_manual_serial(A, B):
    """Seryjne mnożenie macierzy bez użycia `np.dot()`."""
    start_time = time.time()
    size = A.shape[0]
    result = np.zeros((size, size))

    for i in range(size):
        for j in range(size):
            for k in range(size):
                result[i, j] += A[i, k] * B[k, j]

    duration = time.time() - start_time
    return result, duration


# 🚀 **3. Własna implementacja mnożenia macierzy (Równoległa)**
def _multiply_row(A, B, i):
    """Oblicza pojedynczy wiersz macierzy wynikowej."""
    size = A.shape[0]
    row_result = np.zeros(size)
    for j in range(size):
        for k in range(size):
            row_result[j] += A[i, k] * B[k, j]
    return i, row_result


def multiply_manual_parallel(A, B):
    """Równoległe mnożenie macierzy metodą `multiprocessing.Pool()`."""
    start_time = time.time()
    size = A.shape[0]
    result = np.zeros((size, size))

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.starmap(_multiply_row, [(A, B, i) for i in range(size)])

    # Składanie wyników
    for i, row_result in results:
        result[i, :] = row_result

    duration = time.time() - start_time
    return result, duration


# 🚀 **4. Implementacja w `Numba`**
@njit(parallel=True)
def multiply_numba(A, B):
    """Równoległe mnożenie macierzy przy użyciu `Numba`."""
    size = A.shape[0]
    result = np.zeros((size, size))

    for i in prange(size):  # `prange` = wielowątkowość
        for j in range(size):
            for k in range(size):
                result[i, j] += A[i, k] * B[k, j]

    return result
