def matrix_multiply(A, B):
    """
    Multiplies two matrices A and B using a triple nested loop.
    
    Args:
        A (list of list of int/float): First matrix.
        B (list of list of int/float): Second matrix.
        
    Returns:
        list of list of int/float: Resultant matrix after multiplication.
    """
    # Number of rows in A and columns in B
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    
    # Check if multiplication is possible
    if cols_A != rows_B:
        raise ValueError("Number of columns in A must equal number of rows in B")
    
    # Initialize the result matrix with zeros
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    
    # Triple nested loop for matrix multiplication
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    
    return result


# Example usage
if __name__ == "__main__":
    A = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    
    B = [
        [9, 8, 7],
        [6, 5, 4],
        [3, 2, 1]
    ]
    
    result = matrix_multiply(A, B)
    print("Resultant Matrix:")
    for row in result:
        print(row)