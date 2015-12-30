import pytest
import os
from histmag_to_kindle.histmag_parser import Page


@pytest.fixture
def page_1():
    return Page(addr='http://mock_url',
                contents=[('p', 'Zażółć gęślą jaźń'),
                          ('a', 'Etiam aliquam'),
                          ('p', None),
                          ('p', None),
                          ('p', None),
                          ('img', 'http://placehold.it/350x150'),
                          ('p', 'placeholder'),
                          ('p', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.')])


@pytest.fixture
def page_2():
    return Page(addr='http://mock_url',
                title='Zażółć gęślą jaźń',
                authors=['Etiam aliquam'],
                tags=['tag'],
                date='2015-06-23 19:45',
                text='Zażółć gęślą jaźń')