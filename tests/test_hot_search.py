# -*- coding: utf-8 -*-
from io import StringIO
import sys

from crawler.crawler import request_weibo_hot_search, parse_weibo_hot_search


def test_response():
    response = request_weibo_hot_search()
    assert response.status_code == 200


def test_get_hot_search():
    out = StringIO()
    sys.stdout = out
    response = request_weibo_hot_search()
    news = parse_weibo_hot_search(response, 2)
    assert len(news) == 2
    assert out.getvalue().strip() == ''

    news = parse_weibo_hot_search(response, 52)
    assert len(news) == 50
    assert out.getvalue().strip() == '热搜最大条数为:50'
