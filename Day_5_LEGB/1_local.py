x = 'global x'

def test():
    y = 'local y'
    print(y)
    print(x)

test()

print(y)


#LEGB Rule Explanation:
# Inside test(), y is created, so print(y) works and shows "local y".

# x is not defined inside the function, so Python looks outward and finds the global x, printing "global x".

# After test() finishes, y no longer exists; print(y) at the bottom raises NameError because y is local to the function only.