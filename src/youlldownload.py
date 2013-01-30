# -*- coding: utf-8 -*-

import re
import sys
from urlparse import urlparse

# @import url(http://host.net/portal_css/theme_name/foo.css);
PATTERN = r""".*\@import url\((?P<url>.*?)\).*"""

from pyquery import PyQuery

def main():
    if len(sys.argv)<1:
        print "Please, provide an URL as parameter"
        sys.exit(1)

    url = sys.argv[1]
    parsed_url = urlparse(url)
    urls = [url, ]

    pq = PyQuery(url=url)
    
    base_url = pq('base')[0].attrib.get('href')
    if base_url.endswith('/'):
        base_url = base_url[:-1]

    def rebase_url(raw_url):
        if raw_url.startswith('http'):
            return raw_url
        if raw_url.startswith('/'):
            raw_url = raw_url[1:]
        return "%s/%s" % (base_url, raw_url)

    urls.extend([rebase_url(x.attrib.get('src')) for x in pq('script') if x.attrib.get('src')])
    urls.extend([rebase_url(x.attrib.get('href')) for x in pq('link[rel=stylesheet]') if x.attrib.get('href')])
    urls.extend([rebase_url(x.attrib.get('src')) for x in pq('img') if x.attrib.get('src')])
    urls.extend([rebase_url(x.attrib.get('data')) for x in pq('object') if x.attrib.get('data')])
    urls.extend([rebase_url(x.attrib.get('src')) for x in pq('embed') if x.attrib.get('src')])

    for element in pq('style'):
        if re.match(PATTERN, element.text, re.IGNORECASE):
            urls.append(re.match(PATTERN, element.text, re.IGNORECASE).groupdict().get('url'))
    
    # skip urls outside the site host
    urls = [url for url in urls if parsed_url.hostname in url.lower()]
    
    for url in urls:
        print url

#    print " ".join(urls)   

if __name__ == '__main__':
    main()