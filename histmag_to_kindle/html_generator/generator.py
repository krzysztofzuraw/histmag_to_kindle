import os
import logging
import tempfile
import requests
import subprocess
from py.xml import html


log = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
log.setLevel(logging.INFO)


class GenerateMobiError(Exception):
    pass


def generate_mobi(pages, output='histmag.html'):
    html_dir_path = generate_html(pages)
    proc = subprocess.Popen(['bin/kindlegen', os.path.join(html_dir_path, 'histmag.html'), '-o', output],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout = proc.communicate()[0].decode()
    for line in stdout.split('\n'):
        if line.startswith('Error'):
            raise GenerateMobiError(line)
    return html_dir_path


def generate_html(pages):
    tempdir = tempfile.mkdtemp()

    doc = html.html(
            html.head(
                    html.meta(content="text/html; charset=utf-8", **{"http-equiv": "Content-Type"}),  # workaround to that python don't allow keyword args with hypens
                    get_tile(html, pages)
            ),
            html.body(
                    html.div(generate_body(html, pages, tempdir), id='article'),
            )

    )

    with open(os.path.join(tempdir, 'histmag.html'), 'wb') as out_file:
        out_file.write(doc.unicode(indent=2).encode('utf8'))

    return tempdir


def get_tile(html, pages):
    for page in pages:
        title = page.contents[0].value
        tag = page.contents[0].tag
    return html.title(getattr(html, tag)(title))


def generate_body(html, pages, tempdir):
    list_of_bodies = []
    for page in pages:
        for content in page.contents:
            if content.value not in [i[0] for i in list_of_bodies if i.xmlname != 'img']:
                if content.tag == 'img':
                    content = download_images(content, tempdir)
                    list_of_bodies.append(getattr(html, content.tag)(src=content.value))
                else:
                    list_of_bodies.append(getattr(html, content.tag)(content.value))
    return list_of_bodies


def download_images(content, tempdir):
    with open(os.path.join(tempdir, os.path.basename(content.value)), 'wb') as jpg:
        data = requests.get(content.value).content
        jpg.write(data)
    return content._replace(value=os.path.join('.', os.path.basename(content.value)), tag='img')
