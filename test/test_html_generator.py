import os

from lxml import html

from histmag_to_kindle.html_generator.generator import HtmlGenerator

RESULT = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                      'data/websites/article.html')


def test_html_has_authors(page_1, page_2, tmpdir):
    pure_html = HtmlGenerator([page_1, page_2])
    assert open(pure_html.generate(os.path.join(tmpdir.strpath, 'histmag.html'))).read() == open(RESULT).read()


def test_html_has_proper_encoding(page_2, tmpdir):
    generated_html = HtmlGenerator([page_2])
    tree = html.fromstring(open(generated_html.generate(os.path.join(tmpdir.strpath, 'encoding.html'))).read())
    assert tree.xpath('/html/head/meta')[0].attrib['content'] == 'text/html; charset=utf-8'
    assert tree.xpath('//*[@id="article"]/p/text()')[0] == 'Zażółć gęślą jaźń'




