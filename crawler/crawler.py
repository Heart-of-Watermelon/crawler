# -*- coding: utf-8 -*-
"""Main entrance of the crawler."""


def get_weibo_hot_search(num_required):
    """
    request for weibo hot search once, get the first num_required results

    Args:
        num_required: an int that specify the hot search number that user requires

    Returns:
        html_content: the html content string crawled
    """
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
