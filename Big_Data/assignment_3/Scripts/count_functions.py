from multiprocessing import Pool


def count_in_range(row, low, high):
    return sum(low <= x <= high for x in row)


def serial_count(matrix, low, high):
    return sum(count_in_range(row, low, high) for row in matrix)


def parallel_count(matrix, low, high):
    with Pool() as pool:
        result = sum(pool.starmap(count_in_range, [(row, low, high) for row in matrix]))
    return result
