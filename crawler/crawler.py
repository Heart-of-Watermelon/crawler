# -*- coding: utf-8 -*-
"""Main entrance of the crawler."""

import argparse
import datetime
from typing import List, Dict
from urllib import parse

from bs4 import BeautifulSoup
import requests


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
    soup = BeautifulSoup(r.text, features='lxml')

    url_and_title_results = soup.select('#pl_top_realtimehot > table > tbody > tr > td.td-02 > a', limit=num_required + 1)
    url_and_title_results = url_and_title_results[1:]  # 第一条置顶非热搜，无热度数据
    hotness_results = soup.select('#pl_top_realtimehot > table > tbody > tr > td.td-02 > span', limit=num_required)

    if num_required > len(url_and_title_results):
        print("热搜最大条数为:{}".format(len(url_and_title_results)))

    news = []
    for url_title, hotness in zip(url_and_title_results, hotness_results):
        news_dict = {'title': url_title.get_text(),
                     'url': parse.urljoin("https://s.weibo.com", url_title['href']),
                     'hotness': hotness.get_text(), }
        news.append(news_dict)

    return news


def write_news2csv(news: List[Dict], store_path: str):
    today = datetime.date.today()
    f = open(store_path + '/热搜榜-%s.csv' % today, 'w', encoding='utf-8')
    for i in news:
        f.write(i['title'] + ',' + i['url'] + ',' + i['hotness'] + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_required', type=int, required=True,
                        help='an int that specify the hot search number that user requires')
    parser.add_argument('--output_dir', type=str, required=True,
                        help='Path to the directory to save the results')

    args = parser.parse_args()

    news = get_weibo_hot_search(args.num_required)
    write_news2csv(news, args.output_dir)
