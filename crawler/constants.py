# -*- coding: utf-8 -*-
"""constants file for the crawler"""

from urllib import parse

WEIBO_HOST = 'https://s.weibo.com/'
WEIBO_HOT_SEARCH_URL = parse.urljoin(WEIBO_HOST, '/top/summary/')

