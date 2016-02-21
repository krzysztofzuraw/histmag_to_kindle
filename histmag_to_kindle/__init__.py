"""Histmag to kindle main module."""
import logging


logging.basicConfig()
logger = logging.getLogger(__name__)

from .sender import send_email_to_kindle # flake8: noqa
from .generator import generate_mobi # flake8: noqa
from .parser import Parser # flake8: noqa
