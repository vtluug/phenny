#!/usr/bin/python2
"""
botsnack.py - .botsnack module
author: mutantmonkey <mutantmonkey@gmail.com>
"""

import random

def botsnack(phenny, input):
	messages = ["Om nom nom", "Delicious, thanks!"]
	response = random.choice(messages)

	botsnack.snacks += 1

	if botsnack.snacks % 7 == 0:
		phenny.say("Too much food!")
		phenny.do("explodes")
	else:
		phenny.say(response)
botsnack.commands = ['botsnack']
botsnack.priority = 'low'
botsnack.snacks = 0

if __name__ == '__main__':
	print __doc__.strip()

