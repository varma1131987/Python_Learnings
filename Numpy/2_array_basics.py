"""An array is a data structure that stores a collection of elements, typically of the same data type, in a contiguous block of memory. Arrays are widely used in programming for efficient storage and manipulation of data.

In Python, arrays are commonly implemented using the NumPy library, which provides powerful tools for creating and working with arrays.

Key Features of Arrays

Homogeneous: All elements in an array are of the same data type (e.g., integers, floats).
Fixed Size: The size of an array is defined at the time of creation and cannot be changed.
Efficient: Arrays are memory-efficient and allow fast access to elements using their index.

Difference Between Python Lists and NumPy Arrays
--------------------------------------------------------------
Feature	           Python List	                    NumPy Array
Data Type	       Can store mixed data types	    Stores elements of the same type
Performance	         Slower for numerical operations	Faster due to optimized C code

Memory Efficiency
                        Less efficient	      More memory-efficient
Operations	         No built-in vectorized operations	Supports vectorized operations """


# Database : Relational and Non-Relational Databases and Vector databases 

# https://www.datacamp.com/blog/the-top-5-vector-databases

# https://www.geeksforgeeks.org/python/how-to-convert-images-to-numpy-array/

import numpy as np

# 1D Array:
# A single row of elements.
# Example: [1, 2, 3]

# Create a NumPy array
arr = np.array([1, 2, 3, 4, 5])

# print("Array:", arr)
# print("Type:", type(arr))
# print("Shape:", arr.shape)

# Common Operations on Arrays : Accessing Elements:



print(arr[1]) # Output: 2

print(arr[0:2])  # Output: [1 2]
print(arr + 5)  # Output: [ 6  7  8  9 10]
print(arr * 2)  # Output: [ 2  4  6  8 10]
print(arr.mean())  # Output: 3.0    



    