import multiprocessing
import time
from decimal import Decimal, getcontext

# Ustawienie precyzji dla obliczeń
getcontext().prec = 10000  # Można zwiększyć, jeśli chcesz więcej cyfr π


def bbp_formula(n):
    """Zwraca n-tą cyfrę liczby π obliczoną algorytmem BBP."""
    k = Decimal(n)
    return (1 / Decimal(16) ** k) * (
        (Decimal(4) / (8 * k + 1))
        - (Decimal(2) / (8 * k + 4))
        - (Decimal(1) / (8 * k + 5))
        - (Decimal(1) / (8 * k + 6))
    )


def compute_pi_serial(digits):
    """Seryjne obliczanie liczby π do podanej liczby cyfr."""
    start_time = time.time()
    pi = sum(bbp_formula(n) for n in range(digits))
    duration = time.time() - start_time
    return pi, duration


def compute_pi_parallel(digits):
    """Równoległe obliczanie liczby π za pomocą multiprocessing."""
    start_time = time.time()
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(bbp_formula, range(digits))
    pi = sum(results)
    duration = time.time() - start_time
    return pi, duration
