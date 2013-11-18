#!/usr/bin/python3
"""
bitcoin.py - bitcoin currency conversion
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import decimal
import web


def bitcoin(phenny, input):
    """.bitcoin <amount> <currency> [<output currency]> - Convert an
    arbitrary amount of some currency to or from Bitcoin."""

    amount = input.group(2)
    currency = input.group(3)

    if not amount or not currency:
        phenny.say("You need to need to specify an amount and a currency, "
                   "like .bitcoin 1 EUR")
        return

    if currency.upper() == 'BTC':
        from_btc = True
        currency = input.group(4)
    else:
        from_btc = False
        currency = currency.upper()

    if not currency:
        currency = 'USD'
    currency = currency.strip()[:3].upper()

    try:
        amount = decimal.Decimal(amount)
    except decimal.InvalidOperation:
        phenny.say("Please specify a valid decimal amount to convert.")
        return

    try:
        data = web.get('http://data.mtgox.com/api/2/BTC{}/money/ticker'.format(
            web.quote(currency)))
    except web.HTTPError:
        phenny.say("Sorry, I don't know how to convert those right now.")
        return

    data = web.json(data)
    rate = decimal.Decimal(data['data']['last_local']['value'])

    if from_btc:
        amount2 = amount * rate
        amount2 = round(amount2, 2)
        currency2 = data['data']['last_local']['currency'].strip()[:3]
    else:
        amount2 = amount / rate
        amount2 = round(amount2, 8)
        currency2 = 'BTC'

    phenny.say("{amount} {currency}".format(amount=amount2,
                                            currency=currency2))
bitcoin.rule = (['bitcoin'], r'([\d\.]+)\s(\w+)(\s\w+)?')
