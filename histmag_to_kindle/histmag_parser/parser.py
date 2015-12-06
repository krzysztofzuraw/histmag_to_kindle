import logging
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
    """Histmag.org article parser.
       It parses many pages to one for better reading in Kindle"""
    def __init__(self, addr):
        """
        :param addr: url address.
        :type addr: str.
        """
        self.addr = addr
        self.xpath_root = '//div[@id="article"]'
        self.session = requests.Session()

    def get_articles(self):
        """Gets full article with subpages for given address.

        :return: all subpages
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
        :type url: str.
        :param word: word that is in <a> tag.
        :type word: str.
        :param prefix: string needed when url on the page is relative.
        :type prefix: str.
        :return: link with full path.
        ":rtype: str.
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
        :type url: str.
        :return: Page object with author, tags, date and text.
        :rtype: object.
        """
        log.debug('Started parsing page with url: {url}'.format(url=url))
        response = requests.get(url)
        parsed_page = html.fromstring(response.content)
        title_xpath = self.xpath_root + '/h2/text()'
        author_xpath = self.xpath_root + '//a[contains(@href, "author")]//text()'
        tags_xpath = self.xpath_root + '//p[contains(@class, "article-tags")]//a//text()'
        date_xpath = self.xpath_root + '//p[contains(@class, "article-info")]/text()'
        text_xpath = self.xpath_root + '/child::p/text() | //div[@id="article"]/p[3]/strong/text()'

        return Page(addr=url, title=parsed_page.xpath(title_xpath),
                    authors=parsed_page.xpath(author_xpath),
                    tags=parsed_page.xpath(tags_xpath),
                    date=parsed_page.xpath(date_xpath),
                    #TODO: rework how this is done
                    text=parsed_page.xpath(text_xpath)[5:])


class Page(object):
    """Class representing one page of article"""
    def __init__(self, addr, title=None, authors=None, tags=None, date=None, text=None):
        """
        :param addr: url address.
        :type addr: str.
        :param authors: page authors
        :type authors: list.
        :param tags: page tags.
        :type tags: list.
        :param date: article creation date in format YYYY-MM-DD HH:MM.
        :type date: str.
        :param text: article text.
        :type text: str.
        """
        self.addr = addr
        self.title = title
        self.author = authors
        self.tags = tags
        self.date = date
        self.text = text

    def __repr__(self):
        return "Page with {} url".format(self.addr)
