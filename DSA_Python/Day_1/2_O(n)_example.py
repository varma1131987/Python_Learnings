"""This program demonstrates both the O(n) complexity of finding the maximum value and the time measurement for the operation. Let me know if you need further clarification! """


import time

# Function to find the maximum value in an array (O(n) complexity)
def find_max_linear(arr):
    max_val = arr[0]  # Assume the first element is the maximum
    for num in arr:  # Iterate through all elements (n operations)
        if num > max_val:  # Compare each element with the current max
            max_val = num  # Update max if a larger value is found
    return max_val

# Input array
arr = [10, 20, 5, 40, 15,90,100, 200, 300, 400, 500]

# Measure the time taken to find the maximum value
start_time = time.time()  # Start the timer
max_value = find_max_linear(arr)  # Find the maximum value
end_time = time.time()  # End the timer

# Print the results
print(f"The maximum value is: {max_value}")
print(f"Time taken to find the maximum value: {end_time - start_time} seconds")