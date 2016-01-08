import os

from lxml import html

from histmag_to_kindle.html_generator.generator import generate_html

RESULT = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                      'data/websites/article.html')


def test_html_has_authors(page_1, page_2, tmpdir):
    generate_html([page_1, page_2], output=tmpdir.join('histmag.html').strpath)
    assert tmpdir.join('histmag.html').read() == open(RESULT).read()


def test_html_has_proper_encoding(page_2, tmpdir):
    generate_html([page_2], output=tmpdir.join('ecoding.html').strpath)
    tree = html.fromstring(tmpdir.join('ecoding.html').read())
    assert tree.xpath('/html/head/meta')[0].attrib['content'] == 'text/html; charset=utf-8'
    assert tree.xpath('//*[@id="article"]/p/text()')[0] == 'Zażółć gęślą jaźń'




