import os

import pytest
import responses

from histmag_to_kindle.histmag_parser import Page, Parser


PAGE_1 = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/websites/page_1.html')


def test_page_exist(page_1):
    assert isinstance(page_1, Page) is True


@pytest.mark.parametrize("attr, string_attr", [
    ('addr', 'http://mock_url'),
    ('author', ['Etiam aliquam']),
    ('tags', ['historia', 'dummy tag']),
    ('date', '2015-06-23 19:45'),
    ('text', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'),
    ('title', 'Zażółć gęślą jaźń')
])
def test_page_has(page_1, attr, string_attr):
    assert page_1.__getattribute__(attr) == string_attr


@responses.activate
def test_parser_parse_page(page_1):
    responses.add(responses.GET, 'http://mock_url', body=open(PAGE_1).read())

    parser = Parser('http://mock.com')
    parsed_page = parser.parse_page(url='http://mock_url')

    assert parsed_page.author == page_1.author
    assert parsed_page.addr == page_1.addr
    assert parsed_page.date == [page_1.date]
    assert parsed_page.tags == page_1.tags
    assert parsed_page.title == [page_1.title]
    assert parsed_page.text[0] == page_1.text
