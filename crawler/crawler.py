# -*- coding: utf-8 -*-
"""Main entrance of the crawler."""

import argparse
import datetime
import requests
import warnings
from bs4 import BeautifulSoup
from typing import List, Dict


def get_weibo_hot_search(num_required: int) -> List[Dict]:
    """
    request for weibo hot search once, get the first num_required results

    Args:
        num_required: an int that specify the hot search number that user requires

    Returns:
        parsed weibo news: A list of Dictionary, each dictionary includes
        the title, the url and the hotness of the news.
    """
    weibo_url = 'https://s.weibo.com/top/summary/'
    r = requests.get(weibo_url)
    # 向链接发送get请求获得页面
    soup = BeautifulSoup(r.text, 'lxml')

    news = []
    urls_titles = soup.select('#pl_top_realtimehot > table > tbody > tr > td.td-02 > a')  # 链接及标题
    hotness = soup.select('#pl_top_realtimehot > table > tbody > tr > td.td-02 > span')   # 热度

    if num_required > len(urls_titles):
        warnings.warn("热搜最大条数为:", len(urls_titles))

    for i in range(min(len(urls_titles), num_required)):
        news_dict = dict()
        news_dict['title'] = urls_titles[i + 1].get_text()
        news_dict['url'] = "https://s.weibo.com" + urls_titles[i]['href']
        news_dict['hotness'] = hotness[i].get_text()
        news.append(news_dict)

    return news


def write_news2csv(news: List[Dict], store_path: str):
    today = datetime.date.today()
    f = open(store_path + '/热搜榜-%s.csv' % today, 'w', encoding='utf-8')
    for i in news:
        f.write(i['title'] + ',' + i['url'] + ',' + i['hotness'] + '\n')


def parse_html(html_content, rule):
    """
    parse the html content according to rule

    Args:
        html_content: html content string crawled by the crawler
        rule: rule string of xpath or css selector

    Returns:
        results: list of parsed result

    """
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_required', type=int, required=True,
                        help='an int that specify the hot search number that user requires')
    parser.add_argument('--output_dir', type=str, required=True,
                        help='Path to the directory to save the results')

    args = parser.parse_args()

    news = get_weibo_hot_search(args.num_required)
    write_news2csv(news, args.output_dir)
