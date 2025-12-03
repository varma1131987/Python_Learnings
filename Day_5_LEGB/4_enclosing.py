def outer():
    x = 'outer x'

    def inner():
        x = 'inner x'   # if this line is commented, Python will use enclosing x
        print(x)

    inner()
    print(x)

outer()

# What happens:

# Inside inner(), the assignment x = 'inner x' creates a new local x, so print(x) shows "inner x".

# After inner(), print(x) in outer() prints "outer x" from the enclosing function scope.

# If you comment out x = 'inner x', inner() has no local x, so Python looks in the enclosing outer() and prints "outer x".

# Our main teaching Goal  “Nested functions first look in their own scope, then in the enclosing function before going global.”