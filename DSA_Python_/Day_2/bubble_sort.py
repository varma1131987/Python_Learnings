def bubble_sort(arr):
    """
    Perform Bubble Sort on the given array with debugging.
    :param arr: List of elements to be sorted
    :return: None (in-place sorting)
    """
    
    #arr = [64, 34, 25, 12, 22, 90, 11]
    
    n = len(arr)
    for i in range(n): #outer loop for passes
        print(f"Pass {i + 1}:")  # Debugging: Print the pass number
        # Last i elements are already sorted
        for j in range(0, n - i - 1): #inner loop for comparisons
            # Swap if the element found is greater than the next element
            if arr[j] > arr[j + 1]:  #compare adjacent elements
                arr[j], arr[j + 1] = arr[j + 1], arr[j]  #swap if needed
            # Debugging: Print the array after each comparison and swap
            print(f"  After comparing index {j} and {j + 1}: {arr}")
        # Debugging: Print the array after each pass
        print(f"  Array after pass {i + 1}: {arr}\n")

def main():
    """
    Main function to demonstrate Bubble Sort with debugging.
    """
    # Example array
    arr = [64, 34, 25, 12, 22, 90, 11]
    print("Original array:", arr)

    # Perform Bubble Sort
    bubble_sort(arr)
    print("Sorted array:", arr)

if __name__ == "__main__":
    main()