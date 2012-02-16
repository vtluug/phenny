#!/usr/bin/python3
"""
8ball.py - magic 8-ball
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import random

def eightball(phenny, input):
    """.8ball - Magic 8-ball."""

    strong_yes = [
            '45 seconds full throttle',
            'It is certain',
            'It is decidedly so',
            'Without a doubt',
            'Yes--definitely',
            'You may rely on it',
    ]
    tentative_yes = [
            'As I see it, yes',
            'Most likely',
            'Outlook good',
            'Signs point to yes',
            'Yes',
    ]
    negative = [
            'Your request is not bro enough',
            'Reply hazy, try again',
            'Ask again later',
            'Better not tell you now',
            'Cannot predict now',
            'Concentrate and ask again',
    ]
    noncommital = [
            'I am sorry, too high to respond',
            "Don't count on it",
            'My reply is no',
            'My sources say no',
            'Outlook not so good',
            'Very doubtful'
    ]

    # black magic
    quotes = strong_yes + tentative_yes + negative + noncommital
    quote = random.choice(quotes)
    phenny.reply(quote)
eightball.commands = ['8ball']

if __name__ == '__main__':
    print(__doc__.strip())
