import json
import lxml.html
import re
from requests.exceptions import HTTPError
from urllib.parse import quote, unquote
import web


r_tr = re.compile(r'(?ims)<tr[^>]*>.*?</tr>')
r_paragraph = re.compile(r'(?ims)<p[^>]*>.*?</p>|<li(?!n)[^>]*>.*?</li>')
r_tag = re.compile(r'<(?!!)[^>]+>')
r_whitespace = re.compile(r'[\t\r\n ]+')
r_redirect = re.compile(
    r'(?ims)class=.redirectText.>\s*<a\s*href=./wiki/([^"/]+)'
)

abbrs = ['etc', 'ca', 'cf', 'Co', 'Ltd', 'Inc', 'Mt', 'Mr', 'Mrs', 
         'Dr', 'Ms', 'Rev', 'Fr', 'St', 'Sgt', 'pron', 'approx', 'lit', 
         'syn', 'transl', 'sess', 'fl', 'Op', 'Dec', 'Brig', 'Gen'] \
   + list('ABCDEFGHIJKLMNOPQRSTUVWXYZ') \
   + list('abcdefghijklmnopqrstuvwxyz')
no_abbr = ''.join('(?<! ' + abbr + ')' for abbr in abbrs)
breaks = re.compile('({})+'.format('|'.join([
    no_abbr + '[.!?](?:[ \n]|\[[0-9]+\]|$)',
    '。', '｡', '．', '！', '？',
])))

def format_term(term):
    term = term.replace(' ', '_')
    term = term[0].upper() + term[1:]
    return term

def deformat_term(term):
    term = term.replace('_', ' ')
    return term

def format_section(section):
    section = section.replace(' ', '_')
    section = quote(section)
    section = section.replace('%', '.')
    section = section.replace(".3A", ":")
    return section

def parse_term(origterm):
    if "#" in origterm:
        term, section = origterm.split("#")[:2]
        term, section = term.strip(), section.strip()
    else:
        term = origterm.strip()
        section = None

    return (term, section)

def good_content(text, content):
    if text.tag not in ['p', 'ul', 'ol']:
        return False

    if not content.strip():
        return False

    if not breaks.search(content):
        return False

    if text.find(".//span[@id='coordinates']") is not None:
        return False

    return True

def search_content(text):
    if text is None:
        return None

    content = text.text_content()

    while not good_content(text, content):
        text = text.getnext()

        if text is None:
            return None

        content = text.text_content()

    return content

def extract_snippet(match, origsection=None):
    html, url = match
    page = lxml.html.fromstring(html)
    article = page.get_element_by_id('mw-content-text')

    if origsection:
        section = format_section(origsection)
        text = article.find(".//span[@id='{0}']".format(section))
        url += "#" + unquote(section)

        if text is None:
            return ("No '{0}' section found.".format(origsection), url)

        text = text.getparent().getnext()
        content = search_content(text)

        if text is None:
            return ("No section text found.", url)
    else:
        text = article.find('./p')

        if text is None:
            text = article.find('./div/p')

        content = search_content(text)

        if text is None:
            return ("No introduction text found.", url)

    sentences = [x.strip() for x in breaks.split(content)]
    return (sentences[0], url)

class Wiki(object):
    def __init__(self, endpoints):
        self.endpoints = endpoints

    @staticmethod
    def unescape(s): 
        s = s.replace('&gt;', '>')
        s = s.replace('&lt;', '<')
        s = s.replace('&amp;', '&')
        s = s.replace('&#160;', ' ')
        s = s.replace('&quot;', '"')
        return s

    @staticmethod
    def text(html): 
        html = r_tag.sub('', html)
        html = r_whitespace.sub(' ', html)
        return Wiki.unescape(html).strip()

    def search(self, term):
        try:
            exactterm = format_term(term)
            exactterm = quote(exactterm)
            exacturl = self.endpoints['url'].format(exactterm)
            html = web.get(exacturl)
            return (html, exacturl)
        except HTTPError:
            pass

        term = deformat_term(term)
        term = quote(term)
        apiurl = self.endpoints['api'].format(term)

        try:
            result = json.loads(web.get(apiurl))
        except ValueError:
            return None

        result = result['query']['search']

        if not result:
            return None

        term = result[0]['title']
        term = format_term(term)
        term = quote(term)

        url = self.endpoints['url'].format(term)
        html = web.get(url)
        return (html, url)
