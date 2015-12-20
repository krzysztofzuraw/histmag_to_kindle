import pytest
import os
from histmag_to_kindle.histmag_parser import Page


@pytest.fixture
def page_1():
    return Page(addr='http://mock_url',
                authors=['Etiam aliquam'],
                title='Zażółć gęślą jaźń',
                date='2015-06-23 19:45',
                tags=['historia', 'dummy tag'],
                images=[os.path.join(os.path.dirname(os.path.realpath(__file__)), 'text.png')],
                text='Lorem ipsum dolor sit amet, consectetur adipiscing elit.')


@pytest.fixture
def page_2():
    return Page(addr='http://mock_url',
                title='Zażółć gęślą jaźń',
                authors=['Etiam aliquam'],
                tags=['tag'],
                date='2015-06-23 19:45',
                text='Zażółć gęślą jaźń')