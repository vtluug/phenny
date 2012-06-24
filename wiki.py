import json
import re
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
t_sentence = r'^.{5,}?(?<!\b%s)(?:\.(?=[\[ ][A-Z0-9]|\Z)|\Z)'
r_sentence = re.compile(t_sentence % r')(?<!\b'.join(abbrs))


class Wiki(object):
    def __init__(self, api, url, searchurl=""):
        self.api = api
        self.url = url
        self.searchurl = searchurl

    @staticmethod
    def unescape(s): 
        s = s.replace('&gt;', '>')
        s = s.replace('&lt;', '<')
        s = s.replace('&amp;', '&')
        s = s.replace('&#160;', ' ')
        return s

    @staticmethod
    def text(html): 
        html = r_tag.sub('', html)
        html = r_whitespace.sub(' ', html)
        return Wiki.unescape(html).strip()

    def search(self, term, last=False):
        url = self.api.format(term)
        bytes = web.get(url)
        try:
            result = json.loads(bytes)
            result = result['query']['search']
            if len(result) <= 0:
                return None
        except ValueError:
            return None
        term = result[0]['title']
        term = term.replace(' ', '_')
        snippet = self.text(result[0]['snippet'])
        return "{0} - {1}".format(snippet, self.url.format(term))

