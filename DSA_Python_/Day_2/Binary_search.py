# Python Built in 

# sort ()

# sorted() -->Merge sort _ Inseration sortg--? Timsort

# min()
# avg()


""" What is O(log n)?
O(log n) refers to an algorithm whose time complexity grows logarithmically with the size of the input. This means that as the input size increases, the number of operations grows very slowly, proportional to the logarithm of the input size.

Key Characteristics of O(log n):
Divide and Conquer:

Algorithms with O(log n) complexity typically reduce the problem size by a constant factor (e.g., half) at each step.
This is why the number of steps grows logarithmically.
Logarithmic Growth:

If the input size doubles, the number of steps increases by only 1.
For example:
Input size = 8 → Steps = 3
Input size = 16 → Steps = 4
Input size = 32 → Steps = 5
Common Examples:

Binary Search: Divides the search space in half at each step.
Tree Traversals: Searching in balanced binary trees (e.g., BST, AVL trees).
Divide and Conquer Algorithms: Algorithms like Merge Sort and Quick Sort (in their recursive calls).

Binary Search: A Classic Example of O(log n)
Binary search works on a sorted array and reduces the search space by half at each step. Here's how it works:

Look at the middle element of the array.
If the middle element is the target, return it.
If the target is smaller, search the left half of the array.
If the target is larger, search the right half of the array.
Repeat until the search space is reduced to size 1."""

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2  # Find the middle index
        if arr[mid] == target:
            return mid  # Target found
        elif arr[mid] < target:
            left = mid + 1  # Search the right half
        else:
            right = mid - 1  # Search the left half

    return -1  # Target not found

"""is part of the binary search algorithm and is used to initialize the boundaries of the search space within the array.

Explanation:
left:

Represents the starting index of the search space.
Initially set to 0 (the first index of the array).
right:

Represents the ending index of the search space.
Initially set to len(arr) - 1 (the last index of the array).
Purpose:

These variables define the range of indices in the array where the algorithm will search for the target value.
As the binary search progresses, the left and right pointers are updated to narrow down the search space."""

