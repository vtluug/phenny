#!/usr/bin/python2
"""
chillmeter.py - .chill measures chill level of the channel
author: Casey Link <unnamedrambler@gmail.com>

so chill bro.
"""
import random, time


# chill decay rate per minute
chill_decay_rate = 5

# words that make the place chill
chill_words = [
    "chill",
    "bro",
    "fist bump",
    "fistbump",
    "natty",
    "natties",
    "head nod",
    "she said",
    "keystone",
    "smirnoff",
    "sandwhich",
    "lax",
    "lacrosse",
    "pinny",
    "a bowl"
]

# all things chill
chill_things = [
    ("natty", "natties"),
    ("smirnoff ice", "smirnoffs"),
    ("bong hit", "bong hits"),
    ("case of keystone", "cases of keystone"),
    ("fist bump", "fist bumps"),
    ("head nod", "head nods"),
    ("bro", "bros")
]

# keeps a finger on the pulse of the chillness
def measure(phenny, input):
    now = time.time()
    if now - measure.last_tick > 60:
        measure.last_tick = now
        measure.chill -= chill_decay_rate
        measure.chill = max(0, measure.chill)

    if ".chill" in input:
        return # dont self count

    for w in chill_words:
        if w in input.lower():
            measure.chill += 1

measure.rule = r'.*'
measure.priority = 'low'
measure.chill = 0
measure.last_tick = time.time()

def chill(phenny, input):
    level = measure.chill

    n = random.randint(1,2)
    items = []
    for i in range(n):
        if level == 0:
            amount = random.randint(5, 10)
        else:
            amount = random.randint(1, level)
        item = random.choice(chill_things)
        if amount == 1:
            item = item[0] # singular
        else:
            item  = item[1] # plural
        items.append("%s %s" % (amount, item))

    item_str = ", ".join(items)
    print level, item_str

    if level == 0:
        message = "WARNING: CHILL LEVEL IS DANGEROUSLY LOW. RECOMMEND %s" % (item_str.upper())
    else:
        message = "chill level is currently: %s" % (item_str)

    phenny.say(message)


chill.commands = ['chill']
chill.priority = 'low'

if __name__ == '__main__':
	print __doc__.strip()
