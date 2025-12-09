# labels = ["even" if x % 2 == 0 else "odd" for x in range(6)]

# print(labels)


# labels = ["even" if print(f"x = {x}") or x % 2 == 0 else "odd" for x in range(6)]
# print(labels)

# labels = ["even" if print(f"x = {x}") or x % 2 == 0 else "odd" for x in range(6)]
# print(labels)

labels = []
for x in range(6):
    print(f"Current value of x: {x}")  # Print the current value of x
    if x % 2 == 0:
        labels.append("even")
        print(f"x is even, adding 'even' to the list")  # Debug message for even
    else:
        labels.append("odd")
        print(f"x is odd, adding 'odd' to the list")  # Debug message for odd

print("Final labels list:", labels)  # Print the final list