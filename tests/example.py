import time
from parallelize import parallelize

def main():
    num = 10**7  # Large number to make the task computationally heavy
    data = [num] * 128  # Repeat the task 8 times for parallel processing

    start_time = time.time()
    @parallelize(data, pool_size=16, use_tqdm=True, enum=True)
    def compute_heavy_task(data):
        num, ii  = data
        print(ii)
        result = sum(i * i for i in range(num))
        return result

    results = compute_heavy_task()
    end_time = time.time()

    print(f"Results: {results}")
    print(f"Time taken: {end_time - start_time:.3f} seconds")

if __name__ == "__main__":
    main()