import time 

def access_element(arr, index):
    return arr[index]  # 1 operation, always

### Explanation of O(1):
"""
O(1) means that the operation takes the same amount of time regardless of the size of the input.
In this example, accessing an element in an array (or list in Python) by its index is a constant-time operation because:
The memory address of the element is calculated directly using the index.
No iteration or additional computation is required."""

# [1,2,3,4,5,6,7,8,9,10.......100.......1000.....1cr..10billions]  # Example array 



# How It Works:

# Input:

# arr: The array (or list) from which you want to access an element.

# index: The position of the element you want to retrieve.
# Operation:

# arr[index]: This directly retrieves the element at the specified index.

# Time Complexity:

# The operation is performed in constant time, regardless of the size of the array.

# Why is it O(1)?
# The time to access an element in an array is independent of the size of the array.
# The index directly maps to the memory location of the element, so no additional computation is needed.


# Key Takeaway:
# Accessing an element by index in an array or list is a classic example of an O(1) operation because it is always performed in constant time.