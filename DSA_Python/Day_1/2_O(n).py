def find_max_linear(arr):
    max_val = arr[0]  # Assume the first element is the maximum
    for num in arr:  # Iterate through all elements (n operations)
        if num > max_val:  # Compare each element with the current max
            max_val = num  # Update max if a larger value is found
    return max_val
"""
Explanation of O(n):
O(n) means that the time taken by the operation grows linearly with the size of the input.

# [1,2,3,4,5,6,7,8,9,10]
# 


In this example, finding the maximum value in an array requires checking each element once, so the number of operations is proportional to the size of the array.

How It Works:
Input:

arr: The array (or list) in which you want to find the maximum value.

Operation:

The function iterates through all elements in the array using a for loop.
For each element, it checks if the current element is greater than the current maximum value (max_val).

If it is, the maximum value is updated.
Time Complexity:

The loop runs once for each element in the array, so the time complexity is O(n)."""