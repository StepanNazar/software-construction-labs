def partition[T](arr: list[T], low: int, high: int) -> int:
    """
    Partitions the array into two parts, one with elements less than the pivot and the other with
    elements greater than the pivot. The pivot is the last element in the array before partitioning.
    Returns the index of the pivot after partitioning.
    """
    x = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= x:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quick_sort[T](arr: list[T], low: int = 0, high: int = None) -> list[T]:
    """
    Sorts the array using quick sort algorithm.

    >>> quick_sort([5, 3, 8, 4, 2, 7, 1, 10]) # each number is unique
    [1, 2, 3, 4, 5, 7, 8, 10]
    >>> quick_sort(["5", "3", "8", "4", "2", "7", "1", "9"]) # other data type
    ['1', '2', '3', '4', '5', '7', '8', '9']
    >>> quick_sort([5, 3, 8, 4, 2, 7, 1, 10], 0, 3) # subarray at beginning
    [3, 4, 5, 8, 2, 7, 1, 10]
    >>> quick_sort([5, 3, 8, 4, 2, 7, 1, 10], 1, 5) # subarray in the middle
    [5, 2, 3, 4, 7, 8, 1, 10]
    >>> quick_sort([5, 3, 8, 4, 2, 7, 11, 10], 6, 7) # subarray at the end
    [5, 3, 8, 4, 2, 7, 10, 11]
    >>> quick_sort([5, 3, 8, 4, 2, 7, 11, 10], 7, 7) # subarray with one element
    [5, 3, 8, 4, 2, 7, 11, 10]
    >>> quick_sort([1, 1, 1, 1, 1]) # all elements are the same
    [1, 1, 1, 1, 1]
    >>> quick_sort([2, 1, 2, 5, 4]) # some elements are the same
    [1, 2, 2, 4, 5]
    >>> quick_sort([]) # empty list
    []
    """
    if high is None:
        high = len(arr) - 1
    if low < high:
        p = partition(arr, low, high)
        quick_sort(arr, low, p - 1)
        quick_sort(arr, p + 1, high)
    return arr


if __name__ == "__main__":
    import doctest

    doctest.testmod()
