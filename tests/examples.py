import os
import time
from tqdm import tqdm

from parallelize import *

def main():
    data = [10**6] * 256 # make a list of tasks to calculate the sum of squares of a million, 256 times
    n_threads = os.cpu_count() # if None, then uses all cores available
    print(f'Using {n_threads} cores')

    #
    # single process example
    #

    start = time.time()
    for el in tqdm(data):
        res = sum(i * i for i in range(el))
    end = time.time()

    print(f'Single Process Time Taken: {end-start:.2f} sec')

    #
    # parallelize decorator example
    #

    @parallelize(n_threads=n_threads, use_tqdm=True)
    def compute_heavy_task(val):
        res = sum(i * i for i in range(val))
        return res

    start = time.time()
    res = compute_heavy_task(data)
    end = time.time()
    print(f'Multi Process Time Taken: {end-start:.2f} sec')

    #
    # parallelize function example
    #

    def compute_heavy_task(val):
        res = sum(i * i for i in range(val))
        return res

    parallel_compute_heavy_task = parallelize(compute_heavy_task, n_threads=n_threads, use_tqdm=True)

    start = time.time()
    res = parallel_compute_heavy_task(data)
    end = time.time()
    print(f'Multi Process Time Taken: {end-start:.2f} sec')

    #
    # parallelize decorator example with enum
    #

    @parallelize(n_threads=n_threads, use_tqdm=True, enum=True)
    def compute_heavy_task_with_enum(val_tuple):
        val, ii  = val_tuple # add enum here
        res = sum(i * i for i in range(val))
        return res

    start = time.time()
    res = compute_heavy_task_with_enum(data)
    end = time.time()
    print(f'Multi Process Time Taken: {end-start:.2f} sec')

if __name__ == "__main__":
    main()