def merge_sort(arr):
    """
    Perform Merge Sort on the given array.
    :param arr: List of elements to be sorted
    :return: Sorted list
    """
    if len(arr) <= 1:
        return arr

    # Divide the array into two halves
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    # Merge the sorted halves
    return merge(left, right)

def merge(left, right):
    """
    Merge two sorted arrays into a single sorted array.
    :param left: First sorted array
    :param right: Second sorted array
    :return: Merged sorted array
    """
    sorted_array = []
    i = j = 0

    # Merge the two arrays
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            sorted_array.append(left[i])
            i += 1
        else:
            sorted_array.append(right[j])
            j += 1

    # Add remaining elements
    sorted_array.extend(left[i:])
    sorted_array.extend(right[j:])
    return sorted_array

def main():
    """
    Main function to demonstrate Merge Sort.
    """
    # Example array
    arr = [38, 27, 43, 3, 9, 82, 10]
    print("Original array:", arr)

    # Perform Merge Sort
    sorted_arr = merge_sort(arr)
    print("Sorted array:", sorted_arr)

if __name__ == "__main__":
    main()