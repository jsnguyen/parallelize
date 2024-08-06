import time
from parallelize import *
from tqdm import tqdm

def main():
    data = [10**6] * 256 # Repeat the task 8 times for parallel processing

    #
    # single process example
    #

    def compute_heavy_task(data):
        num  = data
        result = sum(i * i for i in range(num))
        return result

    start = time.time()
    for el in tqdm(data):
        _ = compute_heavy_task(el)
    end = time.time()

    print(f'Single Process Time Taken: {end-start:.2f} sec')

    #
    # parallelize decorator example
    #

    @parallelize(n_threads=16, use_tqdm=True)
    def compute_heavy_task(data):
        num  = data
        result = sum(i * i for i in range(num))
        return result

    start = time.time()
    res = compute_heavy_task(data)
    end = time.time()
    print(f'Multi Process Time Taken: {end-start:.2f} sec')

    #
    # parallelize function example
    #

    def compute_heavy_task(data):
        num = data
        result = sum(i * i for i in range(num))
        return result

    parallel_compute_heavy_task = parallelize(compute_heavy_task, n_threads=16, use_tqdm=True)

    start = time.time()
    res = parallel_compute_heavy_task(data)
    end = time.time()
    print(f'Multi Process Time Taken: {end-start:.2f} sec')

    #
    # parallelize decorator example with enum
    #

    @parallelize(n_threads=16, use_tqdm=True, enum=True)
    def compute_heavy_task_with_enum(data):
        num, ii  = data # add enum here
        result = sum(i * i for i in range(num))
        return result

    start = time.time()
    res = compute_heavy_task_with_enum(data)
    end = time.time()
    print(f'Multi Process Time Taken: {end-start:.2f} sec')

if __name__ == "__main__":
    main()