# Input list of marks
marks = [35, 80, 60, 25]

# List comprehension to mark Pass/Fail
results = ["Pass" if mark >= 40 else "Fail" for mark in marks]

print(results)

# Input List:

# marks = [35, 80, 60, 25] is the input list of marks.
# Condition mark >= 40:

# Checks if the mark is greater than or equal to 40.
# If True, "Pass" is added to the list.
# If False, "Fail" is added to the list.
# List Comprehension:

# Iterates over each mark in the list and applies the condition with if–else.
# Output:

# Creates a new list with "Pass" or "Fail" for each mark