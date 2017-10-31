from array import array

a = (1, 2, 3, 5, 34)
b = [1, 2, 3, 5, 34]
c = array('i', [1, 2, 3, 5, 34])
d = ('test', 1, 4)
e = {1, 4, 2, 3, 5}

print(a[0])
print(type(a))
print(type(b))
print(type(c))
print(type(d))
print(type(e))