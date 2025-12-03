# Python normally finds min in the built‑in scope.

# Defining your own min() in the same file shadows the built‑in, so the call min([...]) now uses your empty function and fails (TypeError / no return).

# This demonstrates the B (Built‑in) part: if you override a built‑in name, you lose that function

import builtins

print(dir(builtins))

def min():
    pass

m = min([5, 1, 8, 8, 4, 9, 2])
print(m)
