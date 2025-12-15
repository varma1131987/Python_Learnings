import time

def access_element(arr, index):
    
    return arr[index]  # 1 operation, always

arr = [10, 20, 30, 40, 50]
index = 2
# Access the element at index 2

element = access_element(arr, index)
print(f"Element at index {index}: {element}")
# Measure time taken to access the element
start_time = time.time()   
print(f"Time taken to access element: {time.time() - start_time} seconds") 


f