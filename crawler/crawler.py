# -*- coding: utf-8 -*-
"""Main entrance of the crawler."""

import argparse
import datetime
import time
from typing import List, Dict
from urllib import parse

from bs4 import BeautifulSoup
import requests
import schedule

from crawler import constants


def request_weibo_hot_search() -> requests.Response:
    """
    request for weibo hot search once, get the first num_required results

    Returns:
        r: requests Response object
    """
    r = requests.get(constants.WEIBO_HOT_SEARCH_URL)
    return r


def parse_weibo_hot_search(response: requests.Response, num_required: int) -> List[Dict]:
    """parse the beautfiful soup object

    Args:
        response: requests Response object
        num_required: an int that specify the hot search number that user requires

    Returns:
        news: A list of Dictionary, each dictionary includes
        the title, the url and the hotness of the news.

    """
    soup = BeautifulSoup(response.text, features='lxml')
    url_and_title_results = soup.select('#pl_top_realtimehot > table > tbody > tr > td.td-02 > a',
                                        limit=num_required + 1)
    url_and_title_results = url_and_title_results[1:]  # 第一条置顶非热搜，无热度数据
    hotness_results = soup.select('#pl_top_realtimehot > table > tbody > tr > td.td-02 > span', limit=num_required)

    if num_required > len(url_and_title_results):
        print("热搜最大条数为:{}".format(len(url_and_title_results)))

    news = []
    for url_title, hotness in zip(url_and_title_results, hotness_results):
        news_dict = {'title': url_title.get_text(),
                     'url': parse.urljoin(constants.WEIBO_HOST, url_title['href']),
                     'hotness': hotness.get_text(), }
        news.append(news_dict)
    return news


def write_news2csv(news: List[Dict], store_path: str):
    ts = int(time.time())
    f = open(store_path + '/热搜榜-%s.csv' % ts, 'w', encoding='utf-8')
    for i in news:
        f.write(i['title'] + ',' + i['url'] + ',' + i['hotness'] + '\n')


def hot_search_job():
    response = request_weibo_hot_search()
    news = parse_weibo_hot_search(response, args.num_required)
    write_news2csv(news, args.output_dir)
    print('finish hot search crawling on {}'.format(datetime.datetime.now()))


def _check_positive(value):
    int_value = int(value)
    if int_value <= 0:
        raise argparse.ArgumentTypeError("{} is an invalid positive int value".format(value))
    return int_value


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--num_required', type=_check_positive, default=50,
                        help='an int that specify the hot search number that user requires')
    parser.add_argument('-o', '--output_dir', type=str, default='.',
                        help='Path to the directory to save the results')
    args = parser.parse_args()

    schedule.every().minutes.do(hot_search_job)
    while True:
        schedule.run_pending()
        time.sleep(1)
