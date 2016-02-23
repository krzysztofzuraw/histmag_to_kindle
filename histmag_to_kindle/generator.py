"""HTML generator module."""
import os
import subprocess
import tempfile

import requests
from py.xml import html

from histmag_to_kindle import logger
from histmag_to_kindle.exceptions import ImproperlyConfigured, GenerateMobiError


def generate_mobi(pages, output='histmag.mobi'):  # pragma: no cover
    """Generate mobi file using kindlegen binary from histmag_to_kindle/bin/kindlegen.

    Basic Usage::

    >>> from histmag_to_kindle import generate_mobi
    >>> generator = generate_mobi(articles)
    '/tmp/path_to_directory_with_mobi'

    :param pages: list with `Page.class`.
    :type pages: list.
    :param output: name of file, default histmag.mobi.
    :type output: string.
    :return: path to directory with generated html.
    :rtype: string.
    """
    if not os.environ.get('KINDLEGEN'):
        raise ImproperlyConfigured('No kindlegen library in env variables.')
    html_dir_path = _generate_html(pages)
    proc = subprocess.Popen(
        [
            os.environ.get('KINDLEGEN'),
            os.path.join(html_dir_path, 'histmag.html'),
            '-o',
            output
        ],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    stdout = proc.communicate()[0].decode()
    for line in stdout.split('\n'):
        if line.startswith('Error'):
            raise GenerateMobiError(line)
    logger.info('Mobi generated')
    return html_dir_path


def _generate_html(pages):
    """Generate html for given pages.

    :param pages: list of `Page.class`
    :return: path to tempdir.
    :rtype: string.
    """
    tempdir = tempfile.mkdtemp()

    doc = html.html(
        html.head(
            # python don't allow keyword args with hypens
            html.meta(content="text/html; charset=utf-8", **{"http-equiv": "Content-Type"}),
            _get_tile(html, pages)
        ),
        html.body(
            html.div(_generate_body(html, pages, tempdir), id='article'),
        )
    )

    with open(os.path.join(tempdir, 'histmag.html'), 'wb') as out_file:
        logger.debug(
            'Saving generated html to {file}'.format(file=os.path.join(tempdir, 'histmag.html'))
        )
        out_file.write(doc.unicode(indent=2).encode('utf8'))

    return tempdir


def _get_tile(html, pages):
    """Get title for given py.xml html.

    :param html: `Py.xml` html object.
    :param pages: list of `Page.class`.
    :return: title.
    :rtype: string.
    """
    for page in pages:
        title = page.contents[0].value
        tag = page.contents[0].tag
    return html.title(getattr(html, tag)(title))


def _generate_body(html, pages, tempdir):
    """Generate html body.

    :param html: `Py.xml` html object.
    :param pages: list of `Page.class`.
    :param tempdir: `tempfile` tempdir object.
    :return: `Py.xml` html objects.
    :rtype: list.
    """
    list_of_bodies = []
    for page in pages:
        for content in page.contents:
            if content.value not in [i[0] for i in list_of_bodies if i.xmlname != 'img']:
                if content.tag == 'img':
                    content = _download_images(content, tempdir)
                    list_of_bodies.append(getattr(html, content.tag)(src=content.value))
                else:
                    list_of_bodies.append(getattr(html, content.tag)(content.value))
    logger.debug('Html body generated')
    return list_of_bodies


def _download_images(content, tempdir):
    """Download images from given html content.

    :param content: `Element` namedtuple.
    :param tempdir: `tempfile` tempdir object.
    :return: path to downloaded image.
    :rtype: string.
    """
    with open(os.path.join(tempdir, os.path.basename(content.value)), 'wb') as jpg:
        data = requests.get(content.value).content
        jpg.write(data)
    return content._replace(value=os.path.join('.', os.path.basename(content.value)), tag='img')
