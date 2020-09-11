# -*- coding: utf-8 -*-
"""Main entrance of the crawler."""

from bs4 import BeautifulSoup
import requests
import re


base_url = r'https://s.weibo.com/'
url = r'https://s.weibo.com/top/summary'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}
all_links = []

r = requests.get(url, headers = headers)
print(r.text)
soup = BeautifulSoup(r.text, features='lxml')
all_iterms = soup.find_all('a', {'href' or 'hrdf_to': re.compile(r'^/weibo.')})
for iterm in all_iterms:
    all_links.append({iterm.get_text():base_url + iterm['href']})


#len(all_links)  in principle there should be 51 iterms, however, one or two iterms has atrrbute "href_to" not "href"
# for refreshing every minute, I think it does not matter


def get_weibo_hot_search(num_required):
    """
    request for weibo hot search once, get the first num_required results

    Args:
        num_required: an int that specify the hot search number that user requires

    Returns:
        html_content: the html content string crawled
    """
    all_links = all_links[:num_required]
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
    html_content = get_weibo_hot_search(50)
    results = parse_html(html_content, '')
