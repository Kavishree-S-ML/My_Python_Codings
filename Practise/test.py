import django
from collections import deque
from functools import reduce


def sample(*args, **kwargs):
    """nvjdnvjnnvjd"""
    print args
    """kdjvndvnj"""
    for key in kwargs:
        print(kwargs.get(key))


sample(1, 2, 3, x=7, y=5)
print(sample.__doc__)
a = [1, 2, 3, 4]
print(a)
a.pop()
print(a)
b = deque(a)
print(b)
b.popleft()
print(b)

# ANONYMOUS FUNCTIONS
a = [1, 2, 3, 4]
b = [1, 2, 3, 4]
x = lambda x, y: x + y
print(x(a, b))
m = map(lambda x, y: x + y, a, b)
print(list(m))

f = reduce(x, a)
print(f)
o1 = {'a', 'd', 'c', 'a'}
print(o1)

print(django.get_version())
