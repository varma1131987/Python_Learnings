
"""Quick Sort implementation in Python.

What is a Pivot in Quick Sort?
The pivot in Quick Sort is a key element used to partition the array into two parts:

Left Partition: Contains elements smaller than or equal to the pivot.
Right Partition: Contains elements greater than the pivot.
The pivot acts as a reference point to divide the array, and the sorting process revolves around it.

How the Pivot Works in Quick Sort
Choose a Pivot:

The pivot can be any element in the array (commonly the first, last, or middle element, or chosen randomly).
The choice of the pivot affects the efficiency of the algorithm.
Partition the Array:

Rearrange the array so that:
All elements smaller than or equal to the pivot are on the left.
All elements greater than the pivot are on the right.
Recursive Sorting:

Recursively apply Quick Sort to the left and right partitions.

"""


def quick_sort(arr):
    """
    Perform Quick Sort on the given array.
    :param arr: List of elements to be sorted
    :return: Sorted list
    """
    if len(arr) <= 1:
        return arr  # Base case: A single element or empty array is already sorted

    # Choose the pivot (e.g., the last element)
    pivot = arr[-1]
    left = [x for x in arr[:-1] if x <= pivot]  # Elements less than or equal to the pivot
    right = [x for x in arr[:-1] if x > pivot]  # Elements greater than the pivot

    # Recursively sort the left and right partitions, then combine
    return quick_sort(left) + [pivot] + quick_sort(right)

def main():
    """
    Main function to demonstrate Quick Sort.
    """
    # Example array
    arr = [38, 27, 43, 3, 9, 82, 10]
    print("Original array:", arr)

    # Perform Quick Sort
    sorted_arr = quick_sort(arr)
    print("Sorted array:", sorted_arr)

if __name__ == "__main__":
    main()