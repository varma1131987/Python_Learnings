# global x tells Python that x inside test() refers to the global variable.

# Without assigning, both prints show the same global value.

# If you assign x = 'changed' inside, it will actually modify the global x.

# Key point: only use global rarely; prefer returning values.

x = 'global x'

def test():
    global x
    # x = 'local y'
    print(x)

test()
print(x)
