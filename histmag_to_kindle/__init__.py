import logging

from .histmag_parser import Parser
from .html_generator import HtmlGenerator
from .email_sender import send_email_to_kindle

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())