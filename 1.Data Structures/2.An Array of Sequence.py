"""
These are the main topics this chapter will cover:
• List comprehensions and the basics of generator expressions
• Using tuples as records versus using tuples as immutable lists
• Sequence unpacking and sequence patterns
• Reading from slices and writing to slices
• Specialized sequence types, like arrays and queues
"""
x = 'ABC'
codes = [last := ord(c) for c in x]
print(codes)

# Cartesian Products
colors = ['black', 'white']
sizes = ['S', 'M', 'L']
tshirts = [(color, size) for color in colors for size in sizes]
print(tshirts)

# Generator Expressions
import array

symbols = '$¢£¥€¤'
print(tuple(ord(symbol) for symbol in symbols))
print(array.array('I', (ord(symbol) for symbol in symbols)))

# Tuples used as Immutable Lists
# Tuples used as records
lax_coordinates = (33.9425, -118.408056)
city, year, pop, chg, area = ('Tokyo', 2003, 32_450, 0.66, 8014)
traveler_ids = [('USA', 31195855), ('BRA', 'CE342567'), ('ESP', 'XDA205856')]
for passport in sorted(traveler_ids):
    print('%s/%s' % passport)

# Unpacking Sequences and Iterables
import os

_, filename = os.path.split('/home/luciano/.ssh/id_rsa.pub')
print(filename)

a, b, *rest = range(5)
print(a, b, rest)

# Pattern Matching with Sequences (Python>=3.10)
metro_areas = [
    ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
    ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
    ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
    ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
    ('São Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
]
print(f'{"":15} | {"latitude":>9} | {"longitude":>9}')
for record in metro_areas:
    match record:
        case [name, _, _, (lat, lon)] if lon <= 0:
            print(f'{name:15} | {lat:9.4f} | {lon:9.4f}')

phone_numbers = ['123', '234', '345', '456']


def match_phone_number(phone_number):
    first = phone_number[0]
    match first:
        case '1':
            return "North America and Caribbean"
        case '2':
            return "Africa and some territories"
        case '3' | '4':
            return "Europe"


for number in phone_numbers:
    print(match_phone_number(number))


# using match/case in python>=3.10
class Symbol:
    pass


class Procedure:
    pass


def evaluate(exp, env):
    """Evaluate an expression in an environment."""
    match exp:
        case ['quote', x]:
            return x
        case ['if', test, consequence, alternative]:
            if evaluate(test, env):
                return evaluate(consequence, env)
            else:
                return evaluate(alternative, env)
        case ['lambda', [*parms], *body] if body:
            return Procedure(parms, body, env)
        case ['define', Symbol() as name, value_exp]:
            env[name] = evaluate(value_exp, env)
        case _:
            raise SyntaxError


