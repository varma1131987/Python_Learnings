# Squares of even numbers from 0 to 20
squares_of_evens = [x**2 for x in range(21) if x % 2 == 0]

print(squares_of_evens)

# Explanation:

# range(21):

# Generates numbers from 0 to 20 (inclusive).
# Condition if x % 2 == 0:

# Filters the numbers to include only even numbers.
# Expression x**2:

# Calculates the square of each even number.
# List Comprehension:

# Combines the filtering and transformation into a single line.