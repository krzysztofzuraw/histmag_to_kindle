import logging
import os
from collections import deque
from lxml import html
import requests

log = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
log.setLevel(logging.INFO)


class Parser(object):
    """Histmag.org articles parser.

    Basic Usage::

    >>> from histmag_to_kindle import Parser
    >>> parser = Parser('http_link_to_desired_article')
    >>> articles = parser.get_articles()
    [Page with http_link_to_desired_article url, ...]
    """
    def __init__(self, addr):
        """
        :param addr: url address.
        :type addr: string.
        """
        self.addr = addr
        self.xpath_root = '//div[@id="article"]'
        self.session = requests.Session()

    def get_articles(self):
        """Gets full article with subpages for `self.addr`.

        :return: all subpages in form of :class:`Page`
        :rtype: list
        """
        urls_queue = deque([self.addr])
        found_urls = {self.addr}
        articles = []

        while len(urls_queue):
            url = urls_queue.popleft()
            log.debug('Found url: {url}'.format(url=url))
            current_page = self.parse_page(url)
            link = self.get_first_link(url)
            if link:
                found_urls.add(link)
                urls_queue.append(link)
            articles.append(current_page)

        log.info('Articles has been extracted')
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
            log.debug('No link found for word: {word}'.format(word=word))
            return None

    def parse_page(self, url):
        """Get author, tags, date and text from page.

        :param url: webpage address with 'http://'.
        :type url: string.
        :return: Page object with author, tags, date and text.
        :rtype: :class:`Page`
        """
        log.debug('Started parsing page with url: {url}'.format(url=url))
        response = requests.get(url)
        parsed_page = html.fromstring(response.content)
        title_xpath = self.xpath_root + '/h2/text()'
        author_xpath = self.xpath_root + '//a[contains(@href, "author")]//text()'
        tags_xpath = self.xpath_root + '//p[contains(@class, "article-tags")]//a//text()'
        date_xpath = self.xpath_root + '//p[contains(@class, "article-info")]/text()'
        text_xpath = self.xpath_root + '/child::p[not(contains(@class, "article-tags")) ' \
                                       'and not(contains(@class, "article-info"))]/text()'
        return Page(addr=url, title=parsed_page.xpath(title_xpath),
                    authors=parsed_page.xpath(author_xpath),
                    tags=parsed_page.xpath(tags_xpath),
                    date=parsed_page.xpath(date_xpath),
                    images=self.extract_images(page=parsed_page),
                    text=parsed_page.xpath(text_xpath))

    def extract_images(self, page):
        image_xpath = self.xpath_root + '/child::p/span/a/img/@src'
        # //div[@id="article"]/child::p//text() | //div[@id="article"]/child::p/span/a/img/@src
        image_paths = []
        for url in page.xpath(image_xpath):
            with open(os.path.basename(url), 'wb') as jpg:
                data = self.session.get(url).content
                jpg.write(data)
                image_paths.append(os.path.basename(url))
        return image_paths


class Page(object):
    """Class representing one page of article"""
    def __init__(self, addr, title=None, authors=None, tags=None, date=None, text=None, images=None):
        """
        :param addr: url address.
        :type addr: str.
        :param authors: page authors
        :type authors: list.
        :param tags: page tags.
        :type tags: list.
        :param date: article creation date in format YYYY-MM-DD HH:MM.
        :type date: string.
        :param text: article text.
        :type text: string.
        :param images: page images with full paths
        :type images: list
        """
        self.addr = addr
        self.title = title
        self.author = authors
        self.tags = tags
        self.date = date
        self.text = text
        self.images = images

    def __repr__(self):
        return "Page with {} url".format(self.addr)
