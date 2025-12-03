x = 'global x'

def test():
    x = 'local x'
    print(x)

test()
print(x)


# Inside test(), assigning x = 'local x' creates a new local variable x that shadows the global.

# print(x) inside test() prints "local x" from the local scope.

# print(x) after the function still sees the global x, so it prints "global x".

# This shows that changing x inside the function does not touch the global x unless global x is used.