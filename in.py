def inside(x, a, b):
    if a == b: 
        return True
    if a < b:
        if a < x and x <= b: 
            return True
        else:
            return False
    else:
        if b < x and x <= a:
            return False
        else:
            return True


def inside2(x, a, b, incl=True):
    if a == b: 
        return incl or x != a
    if a < b:
        if a < x:
            if incl:
                return x <= b
            else:
                return x < b
        else:
            return False
    else:
        if x <= a:
            if incl:
                return b >= x
            else:
                return b > x
        else:
            return True

def simple_inside(x, a, b, incl=True):
    if incl:
        if a < b:
            return (a < x and x <= b)
        else:
            return (a < x or x <= b)
    else:
        if a < b:
            return (a < x and x < b)
        else:
            return (a < x or x < b)

print inside(2, 10, 33)
print inside(2, 33, 10)
print inside(10, 2, 33)
print inside(10, 33, 2)
print inside(33, 2, 10)
print inside(33,33, 2)
print inside(2, 10, 2)
print inside (3, 3, 45)
print inside (3, 45, 45)
print inside (3, 45, 3)
print inside (333, 45, 333)


print "...."
print inside2(2, 10, 33), simple_inside(2, 10, 33)
print inside2(2, 33, 10), simple_inside(2, 33, 10)
print inside2(10, 2, 33), simple_inside(10, 2, 33)
print inside2(10, 33, 2), simple_inside(10, 33, 2)
print inside2(33, 2, 10), simple_inside(33, 2, 10)
print inside2(33,33, 2), simple_inside(33,33, 2)
print inside2(2, 10, 2), simple_inside(2, 10, 2)
print inside2(3, 3, 45), simple_inside(3, 3, 45)
print inside2(3, 45, 45), simple_inside(3, 45, 45)
print inside2(3, 45, 3), simple_inside(3, 45, 3)
print inside2(333, 45, 333), simple_inside(333, 45, 333)
print inside2(333, 333, 333), simple_inside(333, 333, 333)

print inside2(2, 10, 33, False) , simple_inside(2, 10, 33, False) 
print inside2(2, 33, 10, False) , simple_inside(2, 33, 10, False) 
print inside2(10, 2, 33, False) , simple_inside(10, 2, 33, False) 
print inside2(10, 33, 2, False) , simple_inside(10, 33, 2, False) 
print inside2(33, 2, 10, False) , simple_inside(33, 2, 10, False) 
print inside2(33,33, 2, False) , simple_inside(33,33, 2, False) 
print inside2(2, 10, 2, False) , simple_inside(2, 10, 2, False) 
print inside2(3, 3, 45, False) , simple_inside(3, 3, 45, False) 
print inside2(3, 45, 45, False) , simple_inside(3, 45, 45, False) 
print inside2(3, 45, 3, False) , simple_inside(3, 45, 3, False) 
print inside2(333, 45, 333, False) , simple_inside(333, 45, 333, False) 
print inside2(333, 333, 333, False) , simple_inside(333, 333, 333, False) 
