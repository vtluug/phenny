#!/usr/bin/python3
"""
wadsworth.py - Use Wadsworth's Constant on a string.
https://gist.github.com/1257195
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

def wadsworth(phenny, input):
    """.wadsworth - Use Wadsworth's Constant on a string."""
    text = input.group(2)
    text = text[text.find(' ', int(round(0.3 * len(text)))) + 1:]
    phenny.say(text)
wadsworth.commands = ['wadsworth']

if __name__ == '__main__':
    print(__doc__.strip())
