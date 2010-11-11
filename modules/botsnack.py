#!/usr/bin/python2
"""
botsnack.py - .botsnack module
author: mutantmonkey <mutantmonkey@gmail.com>
"""

import random

def botsnack(phenny, input):
	msg = input.group(2)

	messages = ["Om nom nom", "Delicious, thanks!"]
	response = random.choice(messages)

	phenny.say(response)
botsnack.commands = ['botsnack']
botsnack.priority = 'low'

if __name__ == '__main__':
	print __doc__.strip()

