import os.path

import pytest

from histmag_to_kindle.email_sender import sender


def test_if_sender_checks_for_configfile(monkeypatch, tmpdir):
    def mockreturn(path):
        return '.no_such_file'
    monkeypatch.setattr(os.path, 'expanduser', mockreturn)

    p = tmpdir.join("hello.txt")
    p.write("content")

    with pytest.raises(FileNotFoundError):
        sender.send_email_to_kindle('dummy@email.com', name=p.strpath)


def test_if_sender_reads_configfile(monkeypatch, tmpdir):
    def mockreturn(path):
        return tmpdir.strpath
    monkeypatch.setattr(os.path, 'expanduser', mockreturn)

    config_file = tmpdir.join('.histmag_parser_conf')
    config_file.write('[sender]\napi_key=abc\nserver=placehold.com')

    p = tmpdir.join("hello.txt")
    p.write("content")
    response = sender.send_email_to_kindle('dummy@email.com', name=p.strpath)
    assert response.status_code == 401