import numpy as np


def generate_matrix(n, m, high):
    """Generate an n by m matrix with random integers up to 'high'."""
    return np.random.randint(1, high, size=(n, m))
