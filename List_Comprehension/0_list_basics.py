# Creating a list
# Acessing the elements

my_list = [1, 2, 3, "hello", 4.5]

# Accessing elements
# print(my_list[0])  # Output: 1
# print(my_list[3])  # Output: hello
# print(my_list[-1])  # Output: 4.5

# # Modifying elements
# my_list[1] = 20
# print(my_list)  # Output: [1, 20, 3, "hello", 4.5]

# # Adding elements

# my_list.append(6)
# print(my_list)  # Output: [1, 20, 3, "hello", 4.5, 6]

# # Removing elements

# my_list.remove(3)
# print(my_list)  # Output: [1, 20, "hello", 4.5, 6]

#2 Slicing ##

# print(my_list[1:4])  # Output: [20, "hello", 4.5]

# 3 Iterating ##

# for item in my_list:
#     print(item)
    
# # 4 List Comprehensions ##

squares = [x*x for x in range(5)]
print(squares)  # Output: [0, 1, 4, 9, 16]




