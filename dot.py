from pprint import pprint
from functools import reduce
from operator import getitem

users = [
    {'id': 'kng', 'profile': {'login': 'gsroka'}}, 
    {'id': 'you', 'profile': {'login': 'u@zoo'}}
]
keys = ['id', 'profile.login']

def pluck(items, keys):
    new_items = []
    for item in items:
        d = {}
        for key in keys:
            v = item
            for k in key.split('.'):
                v = v[k]
            d[key] = v
        new_items.append(d)
    return new_items

def dot(v, key):
    """dot({a:{b:'c'}}, 'a.b') -> 'c'."""
    for k in key.split('.'):
        v = v[k]
    return v

# v1
pprint(pluck(users, keys))
print()

# v2
pprint([{key: dot(user, key) for key in keys} for user in users])
print()

# v3
pprint([{key: reduce(getitem, key.split('.'), user) for key in keys} for user in users])