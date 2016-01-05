import os
import logging

from py.xml import html

# import dominate
# from dominate.tags import *

log = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
log.setLevel(logging.INFO)


class HtmlGenerator(object):
    """Class for generating htmls from list of articles

    Basic usage::

    >>>from histmag_to_kindle import HtmlGenerator
    >>>generator = HtmlGenerator(['list_of_articles'])
    >>>generator.generate()
    'abs_path/to/generated_html'
    """

    def __init__(self, page):
        """
        :param page: instance of :class:`histmag_to_kindle.histmag_parser.Page` object from parser
        """
        self.page = page

    def generate(self, html_path='histmag_article'):
        """Generate html.

        :param html_path: path where to save generated html
        :return: absolute path to generated html
        :rtype: string
        """
        html_article = dominate.document(title=self.page[0].title)

        with html_article.head:
            meta(http_equiv="Content-Type", content="text/html; charset=utf-8")

        with html_article:
            with div(id='article'):
                log.debug('Save h1 tag to html')
                h1(self.page[0].author)
                log.debug('Save h2 tag to html')
                h2(','.join(self.page[0].tags))
                log.debug('Save h3 tag to html')
                h3(self.page[0].date)
                for page in self.page:
                    log.debug('Save p tag to html')
                    p(page.text)

        with open(html_path, 'w') as his:
            his.write(str(html_article))
        log.info('Html generated with path: {path}'.format(path=os.path.abspath(his.name)))
        return os.path.abspath(his.name)


def generate_html(pages, output=None):
    doc = html.html(
        html.head(
            get_tile(html, pages),
            html.meta(content="text/html; charset=utf-8", **{"http-equiv": "Content-Type"})  # workaround to that python don't allow keyword args with hypens
        ),
        html.body(
            html.div(id='article'),
            generate_body(html, pages)
        )

    )
    if output is None:
        output = os.path.join(os.getcwd(), 'histmag.html')
    with open(output, 'wb') as out_file:
        out_file.write(doc.unicode(indent=2).encode('utf8'))


def get_tile(html, pages):
    for page in pages:
        title = page.contents[0].value
        tag = page.contents[0].tag
    return html.title(getattr(html, tag)(title))


def generate_body(html, pages):
    list_of_bodies = []
    for page in pages:
        for content in page.contents:
            list_of_bodies.append(getattr(html, content.tag)(content.value))
    return list_of_bodies
