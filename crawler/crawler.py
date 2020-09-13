# -*- coding: utf-8 -*-
"""Main entrance of the crawler."""

import re
import time

import requests
from lxml import etree
from bs4 import BeautifulSoup
from constants import headers, base_url, summary_url

def re_scrapper(url):
    res = requests.get(url, headers=headers)
    ranks = re.findall('ranktop">(.*?)</td>',res.text)
    contents = re.findall('target="_blank">(.*?)</a>',res.text)
    if len(ranks)+1 == len(contents):
        contents = contents[1:]

    info = {}

    for rank, content in zip(ranks, contents):
        info[rank] = content

    return info

def bs_scrapper(url):
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text,'html.parser')
    ranks = [rank.text for rank in soup.select('#pl_top_realtimehot > table > tbody > tr > td.td-01.ranktop')]
    contents = [content.text for content in soup.select('#pl_top_realtimehot > table > tbody > tr > td.td-02 > a')]
    if len(ranks)+1 == len(contents):
        contents = contents[1:]

    info = {}

    for rank, content in zip(ranks, contents):
        info[rank] = content

    return info

def lxml_scrapper(url):
    res = requests.get(url, headers=headers)
    selector = etree.HTML(res.text)
    ranks = [rank.xpath('text()')[0] for rank in selector.xpath('//td[@class="td-01 ranktop"]')]
    contents = [content.xpath('a/text()')[0] for content in selector.xpath('//td[@class="td-02"]')]
    if len(ranks)+1 == len(contents):
        contents = contents[1:]

    info = {}

    for rank, content in zip(ranks, contents):
        info[rank] = content

    return info


def get_weibo_hot_search(num_required, scrapper, url):
    """
    request for weibo hot search once, get the first num_required results

    Args:
        num_required: an int that specify the hot search number that user requires

    Returns:
        html_content: the html content string crawled
    """
    info = scrapper(url)
    return ''


def parse_html(html_content, rule):
    """
    parse the html content according to rule

    Args:
        html_content: html content string crawled by the crawler
        rule: rule string of xpath or css selector

    Returns:
        results: list of parsed result

    """
    return []


if __name__ == '__main__':
    for scrapper in [re_scrapper, bs_scrapper, lxml_scrapper]:
        start = time.time()
        html_content = get_weibo_hot_search(50, scrapper, base_url+summary_url)
        end = time.time()
        print(end-start)
    results = parse_html(html_content, '')
