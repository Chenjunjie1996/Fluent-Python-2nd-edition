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

print(format(Vector2d(1, 1), 'p'))
print(format(Vector2d(1, 1), '.3ep'))
print(format(Vector2d(1, 1), '0.5fp'))

# A Hashable Vector2d
class Vector2d:
    typecode = 'd'
    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __iter__(self):
        return (i for i in (self.x, self.y))

    def __hash__(self):
        return hash((self.x, self.y))

v1 = Vector2d(3, 4)
v2 = Vector2d(3.1, 4.2)
print(hash(v1), hash(v2))


# Supporting Positional Pattern Matching
def keyword_pattern_demo(v: Vector2d) -> None:
    match v:
        case Vector2d(x=0, y=0):
            print(f'{v!r} is null')
        case Vector2d(x=0):
            print(f'{v!r} is vertical')
        case Vector2d(y=0):
            print(f'{v!r} is horizontal')
        case Vector2d(x=x, y=y) if x==y:
            print(f'{v!r} is diagonal')
        case _:
            print(f'{v!r} is awesome')

# Complete Listing of Vector2d, Version 3
class Vector2d:
    __match_args__ = ('x', 'y')
    typecode = 'd'

    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)

    @property
    def x(self):
        return self.__x

    property
    def y(self):
        return self.__y

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

    def __hash__(self):
        return hash((self.x, self.y))

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def angle(self):
        return math.atan2(self.y, self.x)

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

    @classmethod
    def from_bytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)

# Saving Memory with __slots__
class Pixel:
    __slots__ = ('x', 'y')

p = Pixel()
# print(p.__dict__)  'Pixel' object has no attribute '__dict__'
p.x = 10
p.y = 20
# p.color = "red"  'Pixel' object has no attribute 'color'

class OpenPixel(Pixel):
    pass

op = OpenPixel()
print(op.__slots__)
print(op.__dict__)  # OpenPixel have a __dict__.
op.x = 8
op.color = "green"  # If you set an attribute not named in the __slots__, it is stored in the instance __dict__.
print(op.__dict__)

class ColorPixel(Pixel):
    """
    You can set the attributes declared in the __slots__ of this class
    and super‐classes, but no other
    """
    __slots__ = ("color",)

cp = ColorPixel()
cp.x = 2
cp.color = "blue"

"""Summarizing the Issues with __slots__
• You must remember to redeclare __slots__ in each subclass to prevent their
instances from having __dict__.
• Instances will only be able to have the attributes listed in __slots__, unless you
include '__dict__' in __slots__ (but doing so may negate the memory
savings).
• Classes using __slots__ cannot use the @cached_property decorator, unless
they explicitly name '__dict__' in __slots__.
• Instances cannot be targets of weak references, unless you add '__weakref__' in
__slots__.
"""

