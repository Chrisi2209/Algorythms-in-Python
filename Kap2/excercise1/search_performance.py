import search
import random
import timeit
from typing import List

# compare speed of linear and binary search in sorted list.
if __name__ == "__main__":
    avg_time_linear_search = 0
    avg_time_binary_search = 0
    for i in range(10):
        print(i)
        container: List = [random.randint(0, 1_000_000) for _ in range(1_000_000)]
        container.sort()
        for j in range(100):
            print("    ", j)
            choice = random.choice(container)

            avg_time_linear_search += timeit.timeit("lambda: search.linear_search(container, choice)")
            avg_time_binary_search += timeit.timeit("lambda: search.binary_search(container, choice)")
    
    avg_time_linear_search /= 10 * 100
    avg_time_binary_search /= 10 * 100

    print(f"linear_search: {avg_time_linear_search}")
    print(f"binary_search: {avg_time_binary_search}")

