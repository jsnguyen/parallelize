import time
from parallelize import parallelize

def main():
    num = 10**7  # Large number to make the task computationally heavy
    data = [num] * 64 # Repeat the task 8 times for parallel processing

    start_time = time.time()

    @parallelize(data, pool_size=1, use_tqdm=True, enum=True)
    def compute_heavy_task(data):
        num, ii  = data
        result = sum(i * i for i in range(num))
        return result

    results = compute_heavy_task()
    end_time = time.time()

    print(f"Single process time taken: {end_time - start_time:.3f} seconds")

    start_time = time.time()

    @parallelize(data, use_tqdm=True, enum=True)
    def compute_heavy_task(data):
        num, ii  = data
        result = sum(i * i for i in range(num))
        return result

    results = compute_heavy_task()
    end_time = time.time()

    print(f"Multi process time taken: {end_time - start_time:.3f} seconds")

if __name__ == "__main__":
    main()