#!/usr/bin/env python
"""
uncyclopedia.py - Phenny Uncyclopedia Module
Copyright 2008-9, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/

modified from Wikipedia module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import re, urllib.request, urllib.parse, urllib.error
import web

wikiuri = 'http://uncyclopedia.wikia.com/wiki/%s'
wikisearch = 'http://uncyclopedia.wikia.com/wiki/Special:Search?' \
                          + 'search=%s&fulltext=Search'

r_tr = re.compile(r'(?ims)<tr[^>]*>.*?</tr>')
r_paragraph = re.compile(r'(?ims)<p[^>]*>.*?</p>|<li(?!n)[^>]*>.*?</li>')
r_tag = re.compile(r'<(?!!)[^>]+>')
r_whitespace = re.compile(r'[\t\r\n ]+')
r_redirect = re.compile(
    r'(?ims)class=.redirectText.>\s*<a\s*href=./wiki/([^"/]+)'
)

abbrs = ['etc', 'ca', 'cf', 'Co', 'Ltd', 'Inc', 'Mt', 'Mr', 'Mrs', 
            'Dr', 'Ms', 'Rev', 'Fr', 'St', 'Sgt', 'pron', 'approx', 'lit', 
            'syn', 'transl', 'sess', 'fl', 'Op'] \
    + list('ABCDEFGHIJKLMNOPQRSTUVWXYZ') \
    + list('abcdefghijklmnopqrstuvwxyz')
t_sentence = r'^.{5,}?(?<!\b%s)(?:\.(?=[\[ ][A-Z0-9]|\Z)|\Z)'
r_sentence = re.compile(t_sentence % r')(?<!\b'.join(abbrs))

def unescape(s): 
    s = s.replace('&gt;', '>')
    s = s.replace('&lt;', '<')
    s = s.replace('&amp;', '&')
    s = s.replace('&#160;', ' ')
    return s

def text(html): 
    html = r_tag.sub('', html)
    html = r_whitespace.sub(' ', html)
    return unescape(html).strip()

def search(term): 
    try: from . import search
    except ImportError as e: 
        print(e)
        return term

    if not isinstance(term, str): 
        term = term.decode('utf-8')

    term = term.replace('_', ' ')
    try: uri = search.result('site:uncyclopedia.wikia.com %s' % term)
    except IndexError: return term
    if uri: 
        return uri[len('http://uncyclopedia.wikia.com/wiki/'):]
    else: return term

def uncyclopedia(term, last=False): 
    global wikiuri
    if not '%' in term: 
        if isinstance(term, str): 
            t = term
        else: t = term
        q = urllib.parse.quote(t)
        u = wikiuri % q
        bytes = web.get(u)
    else: bytes = web.get(wikiuri % term)
    bytes = r_tr.sub('', bytes)

    if not last: 
        r = r_redirect.search(bytes[:4096])
        if r: 
            term = urllib.parse.unquote(r.group(1))
            return uncyclopedia(term, last=True)

    paragraphs = r_paragraph.findall(bytes)

    if not paragraphs: 
        if not last: 
            term = search(term)
            return uncyclopedia(term, last=True)
        return None

    # Pre-process
    paragraphs = [para for para in paragraphs 
                      if (para and 'technical limitations' not in para 
                                  and 'window.showTocToggle' not in para 
                                  and 'Deletion_policy' not in para 
                                  and 'Template:AfD_footer' not in para 
                                  and not (para.startswith('<p><i>') and 
                                              para.endswith('</i></p>'))
                                  and not 'disambiguation)"' in para) 
                                  and not '(images and media)' in para
                                  and not 'This article contains a' in para 
                                  and not 'id="coordinates"' in para
                                  and not 'class="thumb' in para
                                  and not 'There is currently no text in this page.' in para]
                                  # and not 'style="display:none"' in para]

    for i, para in enumerate(paragraphs): 
        para = para.replace('<sup>', '|')
        para = para.replace('</sup>', '|')
        paragraphs[i] = text(para).strip()

    # Post-process
    paragraphs = [para for para in paragraphs if 
                      (para and not (para.endswith(':') and len(para) < 150))]

    para = text(paragraphs[0])
    m = r_sentence.match(para)

    if not m: 
        if not last: 
            term = search(term)
            return uncyclopedia(term, last=True)
        return None
    sentence = m.group(0)

    maxlength = 275
    if len(sentence) > maxlength: 
        sentence = sentence[:maxlength]
        words = sentence[:-5].split(' ')
        words.pop()
        sentence = ' '.join(words) + ' [...]'

    if (('using the Article Wizard if you wish' in sentence)
     or ('or add a request for it' in sentence)): 
        if not last: 
            term = search(term)
            return uncyclopedia(term, last=True)
        return None

    sentence = '"' + sentence.replace('"', "'") + '"'
    return sentence + ' - ' + (wikiuri % term)

def uncyc(phenny, input): 
    origterm = input.groups()[1]
    if not origterm: 
        return phenny.say('Perhaps you meant ".uncyc Zen"?')
    origterm = origterm

    term = urllib.parse.unquote(origterm)
    term = term[0].upper() + term[1:]
    term = term.replace(' ', '_')

    try: result = uncyclopedia(term)
    except IOError: 
        error = "Can't connect to uncyclopedia.wikia.com (%s)" % (wikiuri % term)
        return phenny.say(error)

    if result is not None: 
        phenny.say(result)
    else: phenny.say('Can\'t find anything in Uncyclopedia for "%s".' % origterm)

uncyc.commands = ['uncyc']
uncyc.priority = 'high'

if __name__ == '__main__': 
    print(__doc__.strip())
