import os

import pytest
import responses

from histmag_to_kindle.histmag_parser import Page, Parser

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
PAGE_1 = os.path.join(BASE_DIR, 'data/websites/page_1.html')


def test_page_exist(page_1):
    assert isinstance(page_1, Page) is True


@responses.activate
def test_parser_parse_page(page_1):
    responses.add(responses.GET, 'http://mock_url', body=open(PAGE_1).read())

    parser = Parser('http://mock.com')
    parsed_page = parser.parse_page(url='http://mock_url')

    assert parsed_page.addr == page_1.addr    
    assert parsed_page.contents == page_1.contents
