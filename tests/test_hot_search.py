# -*- coding: utf-8 -*-
from io import StringIO
import sys

from crawler.crawler import get_weibo_hot_search


def test_get_hot_search():
    out = StringIO()
    sys.stdout = out
    news = get_weibo_hot_search(2)
    assert len(news) == 2
    assert out.getvalue().strip() == ''

    news = get_weibo_hot_search(52)
    assert len(news) == 50
    assert out.getvalue().strip() == '热搜最大条数为:50'
