#-*- coding: utf-8 -*


from urllib.parse import urlparse

"""
>>> o = urlparse('http://www.cwi.nl:80/%7Eguido/Python.html')
>>> o
ParseResult(scheme='http', netloc='www.cwi.nl:80', path='/%7Eguido/Python.html',
            params='', query='', fragment='')
>>> o.scheme
'http'
>>> o.port
80
>>> o.netloc
'www.cwi.nl:80'
>>> o.path
'/Eguido/Python.html'
>>> o.geturl()
'http://www.cwi.nl:80/%7Eguido/Python.html'

>>> from urllib.parse import urljoin
>>> urljoin('http://www.cwi.nl/%7Eguido/Python.html', 'FAQ.html')
'http://www.cwi.nl/%7Eguido/FAQ.html'
"""

def parseURL(url):
    result = {}
    result['host'] = urlparse(url).hostname
    result['port'] = urlparse(url).port
    result['scheme'] = urlparse(url).scheme
    return result

if __name__ == "__main__":
    parseURL("http://a.com:80/a.py")