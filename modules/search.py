#!/usr/bin/env python
"""
search.py - Phenny Web Search Module
Copyright 2008-9, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import re
import web


r_google = re.compile(r'href="\/url\?q=(http.*?)&')

def google_search(query): 
    query = web.quote(query)
    uri = 'https://google.co.uk/search?q=%s' % query
    bytes = web.get(uri)
    m = r_google.search(bytes)
    if m:
        result = web.decode(m.group(1))
        return web.unquote(result)

r_google_count = re.compile(r'id="resultStats">About (.*?) ')

def google_count(query): 
    query = web.quote(query)
    uri = 'https://google.co.uk/search?q=%s' % query
    bytes = web.get(uri)
    m = r_google_count.search(bytes)
    if m:
        result = web.decode(m.group(1)).replace(',', '')
        return int(result)
    else: return 0
    
def formatnumber(n): 
    """Format a number with beautiful commas."""
    parts = list(str(n))
    for i in range((len(parts) - 3), 0, -3):
        parts.insert(i, ',')
    return ''.join(parts)

def g(phenny, input): 
    """Queries Google for the specified input."""
    query = input.group(2)
    if not query: 
        return phenny.reply('.g what?')
    uri = google_search(query)
    if uri: 
        phenny.reply(uri)
        if not hasattr(phenny.bot, 'last_seen_uri'):
            phenny.bot.last_seen_uri = {}
        phenny.bot.last_seen_uri[input.sender] = uri
    else: phenny.reply("No results found for '%s'." % query)
g.commands = ['g']
g.priority = 'high'
g.example = '.g swhack'

def gc(phenny, input): 
    """Returns the number of Google results for the specified input."""
    query = input.group(2)
    if not query: 
        return phenny.reply('.gc what?')
    num = formatnumber(google_count(query))
    phenny.say(query + ': ' + num)
gc.commands = ['gc']
gc.priority = 'high'
gc.example = '.gc extrapolate'

r_query = re.compile(
    r'\+?"[^"\\]*(?:\\.[^"\\]*)*"|\[[^]\\]*(?:\\.[^]\\]*)*\]|\S+'
)

def gcs(phenny, input): 
    """Compare the number of Google results for the specified paramters."""
    if not input.group(2):
        return phenny.reply("Nothing to compare.")
    queries = r_query.findall(input.group(2))
    if len(queries) > 6: 
        return phenny.reply('Sorry, can only compare up to six things.')
    results = []
    for i, query in enumerate(queries): 
        query = query.strip('[]')
        n = int((formatnumber(google_count(query)) or '0').replace(',', ''))
        results.append((n, query))
        if i >= 2: __import__('time').sleep(0.25)
        if i >= 4: __import__('time').sleep(0.25)

    results = [(term, n) for (n, term) in reversed(sorted(results))]
    reply = ', '.join('%s (%s)' % (t, formatnumber(n)) for (t, n) in results)
    phenny.say(reply)
gcs.commands = ['gcs', 'comp']
gcs.example = '.gcs Ronaldo Messi'

r_bing = re.compile(r'<h2><a href="([^"]+)"')

def bing_search(query, lang='en-GB'): 
    query = web.quote(query)
    base = 'https://www.bing.com/search?mkt=%s&q=' % lang
    bytes = web.get(base + query)
    m = r_bing.search(bytes)
    if m: return m.group(1)

def bing(phenny, input): 
    """Queries Bing for the specified input."""
    query = input.group(2)
    if query.startswith(':'): 
        lang, query = query.split(' ', 1)
        lang = lang[1:]
    else: lang = 'en-GB'
    if not query:
        return phenny.reply('.bing what?')
    uri = bing_search(query, lang)
    if uri: 
        phenny.reply(uri)
        if not hasattr(phenny.bot, 'last_seen_uri'):
            phenny.bot.last_seen_uri = {}
        phenny.bot.last_seen_uri[input.sender] = uri
    else: phenny.reply("No results found for '%s'." % query)
bing.commands = ['bing']
bing.example = '.bing swhack'

r_duck = re.compile(r'nofollow" class="[^"]+" href=".+?(http.*?)">')

def duck_search(query): 
    query = query.replace('!', '')
    query = web.quote(query)
    uri = 'https://duckduckgo.com/html/?q=%s&kl=uk-en' % query
    bytes = web.get(uri)
    m = r_duck.search(bytes)
    if m:
        result = web.decode(m.group(1))
        return web.unquote(result)

def duck_api(query):
    uri = 'https://api.duckduckgo.com/?q=%s&format=json&no_redirect=1' % query
    bytes = web.get(uri)
    json = web.json(bytes)
    if query[:1] == '!':
        return json['Redirect']
    elif json['Abstract']:
        return json['AbstractURL'] + ' : ' + json['Abstract']
    else: return json['AbstractURL']

def duck(phenny, input):
    """Queries DuckDuckGo for specified input.""" 
    query = input.group(2)
    if not query: return phenny.reply('.ddg what?')
    uri = duck_api(query)
    if not uri:
        uri = duck_search(query)
    if uri: 
        phenny.reply(uri)
        if not hasattr(phenny.bot, 'last_seen_uri'):
            phenny.bot.last_seen_uri = {}
        phenny.bot.last_seen_uri[input.sender] = uri
    else: phenny.reply("No results found for '%s'." % query)
duck.commands = ['duck', 'ddg']
duck.example = '.duck football'

def search(phenny, input): 
    if not input.group(2): 
        return phenny.reply('.search for what?')
    query = input.group(2)
    gu = google_search(query) or '-'
    bu = bing_search(query) or '-'
    du = duck_search(query) or '-'

    if (gu == bu) and (bu == du): 
        result = '%s (g, b, d)' % gu
    elif (gu == bu): 
        result = '%s (g, b), %s (d)' % (gu, du)
    elif (bu == du): 
        result = '%s (b, d), %s (g)' % (bu, gu)
    elif (gu == du): 
        result = '%s (g, d), %s (b)' % (gu, bu)
    else: 
        if len(gu) > 250: gu = '(extremely long link)'
        if len(bu) > 150: bu = '(extremely long link)'
        if len(du) > 150: du = '(extremely long link)'
        result = '%s (g), %s (b), %s (d)' % (gu, bu, du)

    phenny.reply(result)
search.commands = ['search']

if __name__ == '__main__': 
    print(__doc__.strip())
