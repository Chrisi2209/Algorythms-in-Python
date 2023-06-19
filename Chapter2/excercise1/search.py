from typing import Iterable, TypeVar

T = TypeVar("T")



def linear_search(iterable: Iterable[T], search_for_item: T):
    for item in iterable:
        if item == search_for_item:
            return True
        
    return False

def binary_search(iterable: Iterable[T], search_for_item: T):
    low: int = 0
    high: int = len(iterable)

    while low < high:
        mid = (low + high) // 2
        if search_for_item > iterable[mid]:
            low = mid
        elif search_for_item < iterable[mid]:
            high = mid
        else:
            return True
        
    return False
        
if __name__ == "__main__":
    container: list = [1, 3, 5, 6, 10, 11, 12]
    print(linear_search(container, 5))
    print(binary_search(container, 5))
