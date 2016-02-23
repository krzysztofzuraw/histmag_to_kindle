"""Tests for sender module."""
import pytest

from histmag_to_kindle import send_email_to_kindle
from histmag_to_kindle.exceptions import ImproperlyConfigured


def test_if_sender_checks_for_env_variables(tmpdir):
    """Test for preventing users from using sender without first configured it.

    GIVEN not properly configured application
    AND sending email using external API
    THEN exception should be thrown
    """
    p = tmpdir.join("hello.txt")
    p.write("content")

    with pytest.raises(ImproperlyConfigured):
        send_email_to_kindle('dummy@email.com', name=p.strpath)
