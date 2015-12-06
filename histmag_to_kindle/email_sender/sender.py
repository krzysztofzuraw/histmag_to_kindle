import os
import logging
import configparser
import requests

log = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
log.setLevel(logging.INFO)


def config_file_check(func):
    """
    Decorator for checking if config file is present
    """
    def checker(*args, **kwargs):
        log.debug('Checking if config file exists')
        config_file_path = os.path.join(os.path.expanduser('~'), '.histmag_parser_conf')
        if os.path.isfile(config_file_path):
            config = configparser.ConfigParser()
            config.read(config_file_path)
            kwargs['api_key'] = config.get('sender', 'api_key')
            kwargs['server'] = config.get('sender', 'server')

            return func(*args, **kwargs)
        else:
            raise FileNotFoundError('No such file {path}'.format(path=config_file_path))

    return checker


@config_file_check
def send_email_to_kindle(kindle_email, name='histmag.mobi', **kwargs):
    """
    Sending html_article to kindle_email using mailgun api. You need to have histmag_conf properly configured first.
    :param kindle_email: your kindle email
    :param name: path to file to send
    :return: response
    """
    api_key = kwargs.pop('api_key')
    server = kwargs.pop('server')
    log.debug('Sending html_article to {email}'.format(email=kindle_email))
    return requests.post("https://api.mailgun.net/v3/{server}/messages".format(server=server),
                         auth=("api", api_key),
                         files=[("attachment", open(name, 'rb'))],
                         data={"from": "Excited User <mailgun@{server}>".format(server=server),
                               "to": kindle_email,
                               "subject": "Upload",
                               "text": "send to kidle"})
