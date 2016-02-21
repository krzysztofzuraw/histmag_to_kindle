# -*- coding: utf-8 -*-
"""Test setup module."""
import pytest
import collections

from histmag_to_kindle.parser import Page


@pytest.fixture()
def fake_element_namedtuple():
    """Helper function for marking `Element` tuple."""
    def make(tuple_to_fake):
        Element = collections.namedtuple('Elements', ['tag', 'value'])
        return Element(tag=tuple_to_fake[0], value=tuple_to_fake[1])
    return make


@pytest.fixture
def page_1(fake_element_namedtuple):
    """Faked page."""
    return Page(
        addr='http://mock_url',
        contents=[
            fake_element_namedtuple(('p', 'Zażółć gęślą jaźń')),
            fake_element_namedtuple(('a', 'Etiam aliquam')),
            fake_element_namedtuple(('p', '')),
            fake_element_namedtuple(('p', '')),
            fake_element_namedtuple(('p', '\n\t\t')),
            fake_element_namedtuple(('span', 'Lorem ipsum dolor sit amet.')),
            fake_element_namedtuple(('img', 'http://placehold.it/350x150')),
            fake_element_namedtuple(('p', 'placeholder')),
            fake_element_namedtuple(('p', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'))
        ]
    )


@pytest.fixture
def page_2(fake_element_namedtuple):
    """Second faked page."""
    return Page(addr='http://mock_url',
                contents=[fake_element_namedtuple(('p', 'Zażółć gęślą jaźń')),
                          fake_element_namedtuple(('a', 'Etiam aliquam')),
                          fake_element_namedtuple(('p', '')),
                          fake_element_namedtuple(('p', '')),
                          fake_element_namedtuple(('p', '')),
                          fake_element_namedtuple(('p', 'Another place'))])
