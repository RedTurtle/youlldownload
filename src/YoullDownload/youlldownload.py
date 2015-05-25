# -*- coding: utf-8 -*-

import re
import sys
from urlparse import urlparse

# @import url(http://host.net/portal_css/theme_name/foo.css);
PATTERN = r""".*\@import url\((?P<url>.*?)\).*"""
# font-face{font-family:'FontAwesome';src:url('../fonts/fontawesome-webfont.eot?v=4.3.0');
CSS_URL_PATTERNS = r"""url\s*\(\s*['"]?\s*(?P<url>[^)'"]+)\s*['"]?\s*\)"""

from pyquery import PyQuery
import requests


def main():
    if len(sys.argv)<1:
        print "Please, provide an URL as parameter"
        sys.exit(1)

    url = sys.argv[1]
    parsed_url = urlparse(url)
    urls = [url, ]

    pq = PyQuery(url=url)
    
    base_urls_parts = urlparse(url)
    base_url = "%s://%s" % (base_urls_parts.scheme, base_urls_parts.netloc)
    try:
        base_url = pq('base')[0].attrib.get('href')
    except IndexError:
        pass
    if base_url.endswith('/'):
        base_url = base_url[:-1]

    def rebase_url(raw_url):
        if raw_url.startswith('http'):
            return raw_url
        if raw_url.startswith('/'):
            raw_url = raw_url[1:]
        return "%s/%s" % (base_url, raw_url)

    def inspect_inner_css_resources(urls):
        results = []
        for url in urls:
            req = requests.get(url)
            if req.status_code<200 and req.status_code>=300:
                continue
            data = req.text
            inner_urls = re.findall(CSS_URL_PATTERNS, data, flags=re.IGNORECASE|re.MULTILINE)
            for inner_url in inner_urls:
                if inner_url.startswith('data:'):
                    continue
                if inner_url.startswith('../'):
                    inner_url = "/".join(url.split('/')[:-1]) + '/' + inner_url
                elif inner_url.startswith('/'):
                    inner_url = inner_url
                elif not inner_url.startswith('http'):
                    inner_url = url + '/../' + inner_url
                results.append(inner_url)
        return results
 
    urls.extend([rebase_url(x.attrib.get('src')) for x in pq('script') if x.attrib.get('src')])
    urls.extend([rebase_url(x.attrib.get('src')) for x in pq('img') if x.attrib.get('src')])
    urls.extend([rebase_url(x.attrib.get('data')) for x in pq('object') if x.attrib.get('data')])
    urls.extend([rebase_url(x.attrib.get('src')) for x in pq('embed') if x.attrib.get('src')])
    urls.extend([rebase_url(x.attrib.get('src')) for x in pq('iframe') if x.attrib.get('src')])
    urls.extend([rebase_url(x.attrib.get('src')) for x in pq('video source') if x.attrib.get('src')])

    # CSS can required additional resources from inside
    # 1. classic link tags
    css_urls = [rebase_url(x.attrib.get('href')) for x in pq('link[rel=stylesheet]') if x.attrib.get('href')]
    urls.extend(css_urls)
    urls.extend(inspect_inner_css_resources(css_urls))
    # 2. style tags
    css_urls = []
    for element in pq('style'):
        if re.match(PATTERN, element.text, re.IGNORECASE):
            css_urls.append(re.match(PATTERN, element.text, re.IGNORECASE).groupdict().get('url'))
    urls.extend(css_urls)
    urls.extend(inspect_inner_css_resources(css_urls))

    # skip urls outside the site host
    urls = [url for url in urls if parsed_url.hostname in url.lower()]

    # clean from achors
    urls = [url[:None if (url.find('#')==-1) else url.find('#')] for url in urls]
    
    for url in sorted(set(urls)):
        print url

if __name__ == '__main__':
    main()