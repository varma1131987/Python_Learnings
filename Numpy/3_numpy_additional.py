"""To expand our understanding of NumPy arrays and their applications, here are additional concepts and operations you can learn:"""
#  Array Attributes

# 1. arr.ndim: Returns the number of dimensions of the array

import numpy as np

# arr = np.array([1, 2, 3,4, 5, 6])  

# print("Number of Dimensions:", arr.ndim) 

# # #2 arr.size: Returns the total number of elements in the array


# # print("Size of Array:", arr.size)  # Output: 6


# # print("Data Type:", arr.dtype)  # Output: int64 (or int32 depending on your system) 

# # # Array Indexing and Slicing  

# # # 1. Negative Indexing: Access elements from the end of the array using negative indices.

# # print("Last Element:", arr[-1])  # Output: 6

# # print("First Element:", arr[0])  # Output: 1

# # print("Elements from index 1 to end:", arr[1:])  # Output: [2 3 4 5 6]

# # print("Elements up to index 3:", arr[:3])  # Output: [1 2 3]

# # Array Reshaping

# # 1. Reshape: Change the shape of an array without changing its data.

# # arr_reshaped = arr.reshape(1, 6)  # Reshape to 1 row and 6 columns

# # print("Reshaped Array:\n", arr_reshaped)

# # Array Concatenation and Splitting 

# # 1. Concatenate: Join two or more arrays along an existing axis.

# # arr1 = np.array([1, 2, 3])
# # arr2 = np.array([4, 5, 6])
# # arr_concatenated = np.concatenate((arr1, arr2))
# # print("Concatenated Array:", arr_concatenated)  # Output: [1 2 3 4 5 6]
# # # 2. Split: Split an array into multiple sub-arrays.
# # arr_split = np.array_split(arr_concatenated, 3)
# # print("Split Arrays:", arr_split)  # Output: [array([1, 2]), array([3, 4]), array([5, 6])]

# # Array Broadcasting
arr = np.array([1, 2, 3,4, 5, 6])
# arr1 = np.array([1, 2, 3])
# # # 1. Broadcasting: Perform operations on arrays of different shapes.
# arr_small = np.array([10, 20, 30])
# arr_broadcasted = arr1 + arr_small  # arr1 is [1, 2, 3]
# print("Broadcasted Addition:", arr_broadcasted)  # Output: [11 22 33]   

# # Array Copying and Views

# 1. Copy: Create a deep copy of an array.
arr_copy = arr.copy()
arr_copy[0] = 100
# print("Original Array after modifying copy:", arr) 
# print(arr_copy)# Output: [1 2 

# # # # 2. View: Create a view of an array (shallow copy).
arr_view = arr.view()
arr_view[0] = 99
print("Original Array:", arr)  # Output: [1 2 3 4 5 6]
print("Copied Array:", arr_copy)  # Output: [1 2 3 4 5 6]
print("View of Array:", arr_view)  # Output: [1 2 3 4 5 6]  
 # Changes reflect in the original array

# # # # Stacking and Concatenation  

arr2 = np.array([6, 7, 8, 9, 10])
print("Horizontal Stack:", np.hstack((arr, arr2)))
# Output: [ 1  2  3  4  5  6  7  8  9 10]

# # print("Vertical Stack:\n", np.vstack((arr, arr2)))
# Output:
# [[ 1  2  3  4  5]
#  [ 6  7  8  9 10]]