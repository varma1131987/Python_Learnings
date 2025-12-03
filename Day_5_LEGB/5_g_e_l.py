
# Inside inner(): "inner x" (local to inner).

# Inside outer() after inner(): "outer x" (local to outer, enclosing for inner).

# After outer() finishes: "global x" (global variable).

# Use this to show three different x values existing at the same time in different scopes.

x = 'global x'

def outer():
    x = 'outer x'

    def inner():
        x = 'inner x'
        print(x)

    inner()
    print(x)

outer()
print(x)
