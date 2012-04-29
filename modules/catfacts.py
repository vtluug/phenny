#!/usr/bin/env python

import web

def catfacts_ajax():
    uri = 'http://facts.cat/getfact'
    bytes = web.get(uri)
    return web.json(bytes)

def catfacts_get():
    fact = catfacts_ajax()
    try:
        return fact['factoid']
    except IndexError:
        return None
    except TypeError:
        print(fact)
        return False

def catfacts(phenny, input):
    fact = catfacts_get()
    if fact:
        phenny.reply(fact)
catfacts.commands = ['catfacts']
