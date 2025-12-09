matrix = [[1, 2], [3, 4], [5, 6]]
flat = [x for row in matrix for x in row]

print(flat)

# # Warn: very complex/nested comprehensions can hurt readability; then prefer normal loops.

# Use Cases of 2D Lists:
# Matrices: Representing mathematical matrices.
# Grids: Storing grid-based data (e.g., game boards, pixel data).
# Tables: Representing tabular data (e.g., rows and columns in a spreadsheet).