"""Email sender module."""
import os

import requests

from histmag_to_kindle import logger
from histmag_to_kindle.exceptions import ImproperlyConfigured


def send_email_to_kindle(kindle_email, name='histmag.mobi'):
    """Sending html_article to kindle_email using mailgun api.

    Basic Usage::

    >>>from histmag_to_kindle import send_email_to_kindle
    >>>send_email_to_kindle(kindle_email='your_kindle_email', name=html)
    <Response [200]>

    :param kindle_email: your kindle email
    :param name: path to file to send
    :return: response
    """
    if not os.environ.get('MAILGUN_API_KEY') or not os.environ.get('EMAIL_SERVER'):
        raise ImproperlyConfigured('Either MAILGUN_API_KEY or EMAIL_SERVER variable not found in enviroment variables.')
    api_key = os.environ.get('MAILGUN_API_KEY')
    server = os.environ.get('EMAIL_SERVER')
    logger.debug('Sending html_article to {email}'.format(email=kindle_email))
    return requests.post("https://api.mailgun.net/v3/{server}/messages".format(server=server),
                         auth=("api", api_key),
                         files=[("attachment", open(name, 'rb'))],
                         data={"from": "Excited User <mailgun@{server}>".format(server=server),
                               "to": kindle_email,
                               "subject": "Upload",
                               "text": "send to kidle"})
