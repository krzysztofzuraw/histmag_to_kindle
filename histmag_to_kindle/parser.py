# -*- coding: utf-8 -*-
"""Histmag to kindle website crawler and parser."""
from collections import deque, namedtuple

import requests
from lxml import html

from histmag_to_kindle import logger


class Parser(object):
    """Histmag.org articles parser.

    Basic Usage::

    >>> from histmag_to_kindle import Parser
    >>> parser = Parser('http_link_to_desired_article')
    >>> articles = parser.get_articles()
    [Page with http_link_to_desired_article url, ...]
    """

    def __init__(self, addr):
        """Constructor.

        :param addr: url address.
        :type addr: string.
        """
        self.addr = addr
        self.xpath_root = '//div[@id="article"]'
        self.session = requests.Session()

    def get_articles(self):
        """Get full article with subpages for `self.addr`.

        :return: all subpages in form of :class:`Page`
        :rtype: list
        """
        urls_queue = deque([self.addr])
        found_urls = {self.addr}
        articles = []

        while len(urls_queue):
            url = urls_queue.popleft()
            logger.debug('Found url: {url}'.format(url=url))
            current_page = self.parse_page(url)
            link = self.get_first_link(url)
            if link:
                found_urls.add(link)
                urls_queue.append(link)
            articles.append(current_page)

        logger.info('Articles has been extracted')
        return articles

    def get_first_link(self, url, word='następna'):
        """Get first link that contains given word.

        :param url: webpage address with 'http://'.
        :type url: string.
        :param word: word that is in <a> tag.
        :type word: string.
        :return: link with full path.
        ":rtype: string.
        """
        response = requests.get(url)
        parsed_page = html.fromstring(response.content)
        link_xpath = '//a[contains(.,"' + word + '")]/@href)[1]'
        try:
            return parsed_page.xpath('(' + self.xpath_root + link_xpath)[0]
        except IndexError:
            logger.debug('No link found for word: {word}'.format(word=word))
            return None

    def parse_page(self, url):
        """Parse page and retrive its contents.

        :param url: webpage address with 'http://'.
        :type url: string.
        :return: Page object with addr and contents
        :rtype: :class:`Page`
        """
        logger.debug('Started parsing page with url: {url}'.format(url=url))
        response = requests.get(url)
        parsed_page = html.fromstring(response.content)
        page_contents = []
        Element = namedtuple('Elements', ['tag', 'value'])
        for elem in parsed_page.xpath('{root}//child::p[not(contains(@class, "article-tags")) '
                                      'and not(contains(@class, "article-info"))] '
                                      '| {root}//a[contains(@href, "author")]'
                                      '| {root}//em '
                                      '| {root}//img '
                                      '| {root}//span'.format(root=self.xpath_root)):
            if elem.tag == 'img':
                page_contents.append(Element(elem.tag, elem.attrib['src']))
            elif elem.tag == 'span':
                page_contents.append(Element(elem.tag, elem.text_content() or ''))
            else:
                page_contents.append(Element(elem.tag, elem.text or ''))

        return Page(url, contents=page_contents)


class Page(object):
    """Class representing one page of article."""

    def __init__(self, addr, contents=None):
        """Constructor.

        :param addr: url address.
        :type addr: str.
        :param contents: contents of webpage with tags e.g [('p','paragraph', 'img','img_src'), ...].
        :type contents: list.
        """
        self.addr = addr
        self.contents = contents

    def __repr__(self):  # pragma: no cover
        """Page representation."""
        return "Page with {} url".format(self.addr)
