"""Tests for parser module."""
import os

import responses

from histmag_to_kindle.parser import Parser

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
PAGE_1 = os.path.join(BASE_DIR, 'data/websites/page_1.html')


@responses.activate
def test_parser_parse_page(page_1):
    """Check if url is properly parsed into `Page` object."""
    responses.add(responses.GET, 'http://mock_url', body=open(PAGE_1).read())

    parser = Parser('http://mock.com')
    parsed_page = parser.parse_page(url='http://mock_url')

    assert parsed_page.addr == page_1.addr
    assert parsed_page.contents == page_1.contents
