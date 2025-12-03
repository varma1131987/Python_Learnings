x = 'global x'

def test():
    x = 'local x'
    # print(y)
    print(x)

test()
print(x)



# No local x inside test(), so print(x) in the function again reads the global and prints "global x".

# print(x) after the function also prints "global x".

# If you uncommented x = 'local x', you would get Example 2 behavior (local shadow).

# The commented print(y) is a reminder that trying to use an undefined name raises NameError.
