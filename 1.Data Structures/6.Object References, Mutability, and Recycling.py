import copy

l1 = [3, [66, 55, 44], (7, 8, 9)]
l2 = list(l1)  # shallow copy
print(l1)
print(l2)
l1.append(100)  # no effect
l1[1].remove(55)  # effect
print(l1)
print(l2)
l1[1] += [33, 22]  # mutable object, effect
l2[2] += (10, 11)  # create a new tuple, no effect
print(l1)
print(l2)

# Deep and Shallow Copies
class Bus:
    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = list(passengers)

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)

bus1 = Bus(["Alice", "Bill", "Claire", "David"])
bus2 = copy.copy(bus1)
bus3 = copy.deepcopy(bus1)
bus1.drop("Bill")
print(bus2.passengers)  # shallow copy, effect
print(bus3.passengers)  # deep copy, no effect

# Function Parameters as References
def f(a, b):
    a += b
    return a

f(1, 2)  # The number x is unchanged.
f([1, 2], [3, 4])  # The list a is changed.
f((10, 20), (30, 40))  # The tuple t is unchanged.

# Mutable Types as Parameter Defaults: Bad Idea
class HauntedBus:
    def __init__(self, passengers=[]):
        self.passengers = passengers

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)

bus1 = HauntedBus(['Alice', 'Bill'])
print(bus1.passengers)

bus1.pick('Charlie')
bus1.drop('Alice')
print(bus1.passengers)

bus2 = HauntedBus()
bus2.pick('Carrie')
print(bus2.passengers)

bus3 = HauntedBus()
print(bus3.passengers)

bus3.pick('Dave')
print(bus2.passengers)

print(bus2.passengers is bus3.passengers)

print(bus1.passengers)

"""
The problem: bus2.passengers and bus3.passengers refer to the same list.
But bus1.passengers is a distinct list.
don’t get an initial passenger list end up 
sharing the same passenger list among themselves
"""
print(HauntedBus.__init__.__defaults__)

# Defensive Programming with Mutable Parameters
# A simple class to show the perils of mutating received arguments
class TwilightBus:
    """A bus model that makes passengers vanish"""
    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = passengers

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)

basketball_team = ['Sue', 'Tina', 'Maya', 'Diana', 'Pat']
bus = TwilightBus(basketball_team)
bus.drop('Tina')
print(basketball_team)

# Fix: make a copy of list
class TwilightBusFix:
    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = list(passengers)
    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)

basketball_team = ['Sue', 'Tina', 'Maya', 'Diana', 'Pat']
bus = TwilightBusFix(basketball_team)
bus.drop('Tina')
print(basketball_team)

# Garbage Collection, del deletes references, not objects


