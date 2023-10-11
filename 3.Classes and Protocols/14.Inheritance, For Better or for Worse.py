"""
• The super() function
• The pitfalls of subclassing from built-in types
• Multiple inheritance and method resolution order
• Mixin classes
"""
import collections
from collections import OrderedDict


# The super function
class LastUpdatedOrderedDict(OrderedDict):
    """Store items in the order they were last updated
    Overrides __setitem__ to:
    1. Use super().__setitem__ to let it insert or update the key/value pair
    2. Call self.move_to_end to ensure the updated key is in the last position.
    """

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.move_to_end()


# Subclassing Built-In Types Is Tricky
class DoppelDict(dict):
    """
    __setitem__ override is ignored by the __init__ and __update__
    methods of the built-in dict
    """

    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2)


dd = DoppelDict(one=1)  # __init__ method
dd["two"] = 2  # __setitem__ method
dd.update(three=3)  # update method
print(dd)


class AnswerDict(dict):
    """
     The __getitem__ of AnswerDict is bypassed by dict.update
    """

    def __getitem__(self, item):
        return 42


ad = AnswerDict(a="foo")  # ad is an AnswerDict loaded with the key-value pair ('a', 'foo').
print(ad)
print(ad['a'])  # ad['a'] returns 42, as expected.

d = {}
d.update(ad)  # d is an instance of plain dict, which we update with ad.
print(d['a'])  # The dict.update method ignored our AnswerDict.__getitem__.
print(d)


class DoppelDict2(collections.UserDict):
    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2)


class AnswerDict2(collections.UserDict):
    def __getitem__(self, item):
        return 42


dd = DoppelDict2(one=1)
dd['two'] = 2
dd.update(three=3)
print(dd)

ad = AnswerDict2(a="foo")
d = {}
d.update(ad)
print(ad['a'])
print(d['a'])
print(d)

# Multiple Inheritance and Method Resolution Order
"""
diamond problem:
naming conflicts when superclasses implement a method by the same name
"""
class Root:
    def ping(self):
        print(f'{self}.ping() in Root')

    def pong(self):
        print(f'{self}.pong() in Root')

    def __repr__(self):
        cls_name = type(self).__name__
        return f'<instance of {cls_name}>'

class A(Root):
    """both call super()"""
    def ping(self):
        print(f'{self}.ping() in A')
        super().ping()

    def pong(self):
        print(f'{self}.pong() in A')
        super().pong()

class B(Root):
    """ping method call super()"""
    def ping(self):
        print(f'{self}.ping() in B')
        super().ping()

    def pong(self):
        print(f'{self}.pong() in B')

class Leaf(A, B):
    def ping(self):
        print(f'{self}.ping() in Leaf')
        super().ping()

leaf1 = Leaf()
leaf1.ping()
leaf1.pong()

print(Leaf.__mro__)

# the dynamic nature of super()
class U():
    def ping(self):
        print(f'{self}.ping() in U')
        super().ping()

class LeafUA(U, A):
    def ping(self):
        print(f'{self}.ping() in LeafUA')
        super().ping()

u = U()
# u.ping() AttributeError: 'super' object has no attribute 'ping'
leaf2 = LeafUA()
leaf2.ping()
print(LeafUA.__mro__)

# Mixin Classes
"""
A mixin class is designed to be subclassed together with at least one other class in a
multiple inheritance arrangement. A mixin is not supposed to be the only base class
of a concrete class, because it does not provide all the functionality for a concrete
object, but only adds or customizes the behavior of child or sibling classes.
"""

## Case-Insensitive Mappings
def _upper(key):
    try:
        return key.upper()
    except AttributeError:
        return key

class UpperCaseMixin:
    def __setitem__(self, key, item):
        super().__setitem__(_upper(key), item)

    def __getitem__(self, key):
        return super().__getitem__(_upper(key))

    def get(self, key, default=None):
        return super().get(_upper(key), default)

    def __contains__(self, key):
        return super().__contains__(_upper(key))

class UpperDict(UpperCaseMixin, collections.UserDict):
    pass

class UpperCounter(UpperCaseMixin, collections.Counter):
    """Specialized 'Counter' that uppercases string keys"""
    pass

d = UpperDict([('a', 'letter A'), (2, 'digit two')])
print(list(d.keys()))
d['b'] = 'letter B'
print('b' in d)
print(d['a'], d.get('B'))
print(list(d.keys()))

c = UpperCounter('BaNanA')
print(c.most_common())

# Multiple Inheritance in the Real World
## ABCs Are Mixins Too
"""
In the Python standard library, the most visible use of 
multiple inheritance is the collections.abc package.
"""