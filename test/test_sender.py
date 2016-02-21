"""Tests for sender module."""
import os.path

import pytest

from histmag_to_kindle import send_email_to_kindle


def test_if_sender_checks_for_configfile(monkeypatch, tmpdir):
    """Test for preventing users from using sender without first configured it."""
    def mockreturn(path):
        return '.no_such_file'
    monkeypatch.setattr(os.path, 'expanduser', mockreturn)

    p = tmpdir.join("hello.txt")
    p.write("content")

    with pytest.raises(FileNotFoundError):
        send_email_to_kindle('dummy@email.com', name=p.strpath)
