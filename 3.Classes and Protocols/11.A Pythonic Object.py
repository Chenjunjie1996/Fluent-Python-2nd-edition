# Object Representations
"""
repr()
Return a string representing the object as the developer wants to see it. It’s what
you get when the Python console or a debugger shows an object.
str()
Return a string representing the object as the user wants to see it. It’s what you
get when you print() an object.
"""

# Vector Class Redux
from array import array
from datetime import datetime
import math

class Vector2d:
    typecode = 'd'

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __iter__(self):
        return (i for i in (self.x, self.y))

    def __repr__(self):
        class_name = type(self).__name__
        return '{}({!r}, {!r})'.format(class_name, *self)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) +
                bytes(array(self.typecode, self)))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def __format__(self, format_spec=''):
        if format_spec.endswith('p'):
            format_spec = format_spec[:-1]
            coords = (abs(self), self.angle())
            outer_fmt = "<{}, {}>"
        else:
            coords = self
            outer_fmt = "({}, {})"
        components = (format(c, format_spec) for c in coords)
        return outer_fmt.format(*components)
        # components = (format(c, format_spec) for c in self)
        # return "({}, {})".format(*components)

    def angle(self):
        return math.atan2(self.y, self.x)


v1 = Vector2d(3, 4)
print(v1.x, v1.y)
x, y = v1
print(x, y)
print(v1)
v1_clone = eval(repr(v1))
print(v1 == v1_clone)
octests = bytes(v1)
print(octests)
print(abs(v1))
print(bool(v1))
print(bool(Vector2d(0, 0)))

# An Alternative Constructor
@classmethod
def frombytes(cls, octets):
    typecode = chr(octets[0])
    memv = memoryview(octets[1:]).cast(typecode)
    return cls(*memv)

# classmethod vs staticmethod
class Demo:
    @classmethod
    def klassmeth(*args):
        return args

    @staticmethod
    def statemeth(*args):
        return args

print(Demo.klassmeth())
print(Demo.statemeth())
print(Demo.klassmeth("spam"))
print(Demo.statemeth("spam"))

# Formatted Displays
brl = 1 / 4.82
print(brl)
print(format(brl, '0.4f'))
print(f"1 USD = {1 / brl:0.2f} BRL")
print(format(2 / 3, '.1%'))

now = datetime.now()
print(format(now, "%H:%M:%S"))

v1 = Vector2d(3, 4)
print(format(v1))
print(format(v1, '.2f'))
print(format(v1, '.3e'))

# A Hashable Vector2d
