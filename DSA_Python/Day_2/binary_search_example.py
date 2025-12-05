def binary_search(arr, target):
    """
    Perform binary search on a sorted array to find the target value.
    Time Complexity: O(log n)
    """
    left, right = 0, len(arr) - 1  # Initialize the search space

    while left <= right:
        mid = (left + right) // 2  # Find the middle index
        if arr[mid] == target:
            return mid  # Target found, return its index
        elif arr[mid] < target:
            left = mid + 1  # Search the right half
        else:
            right = mid - 1  # Search the left half

    return -1  # Target not found


# Example usage of the binary_search function
if __name__ == "__main__":
    # Sorted array
    arr = [10, 20, 30, 40, 50, 60, 70]
    target = 40

    # Perform binary search
    result = binary_search(arr, target)

    # Print the result
    if result != -1:
        print(f"Element {target} found at index {result}")
    else:
        print(f"Element {target} not found in the array")