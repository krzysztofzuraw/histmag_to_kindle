"""Tests for html generator."""
import os
import tempfile

from lxml import html

from histmag_to_kindle.generator import _generate_html

RESULT = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'data/websites/article.html'
)


def test_html_has_authors(page_1, page_2, tmpdir, monkeypatch):
    """Check if authors are properly generated in html."""
    def mockreturn():
        return tmpdir.strpath
    monkeypatch.setattr(tempfile, 'mkdtemp', mockreturn)
    _generate_html([page_1, page_2])
    assert tmpdir.join('histmag.html').read() == open(RESULT).read()


def test_html_has_proper_encoding(page_2, tmpdir, monkeypatch):
    """Test is document is encoded to have utf-8 chars."""
    def mockreturn():
        return tmpdir.strpath
    monkeypatch.setattr(tempfile, 'mkdtemp', mockreturn)
    _generate_html([page_2])
    tree = html.fromstring(tmpdir.join('histmag.html').read())
    assert tree.xpath('/html/head/meta')[0].attrib['content'] == 'text/html; charset=utf-8'
    assert tree.xpath('//*[@id="article"]/p/text()')[0] == 'Zażółć gęślą jaźń'
