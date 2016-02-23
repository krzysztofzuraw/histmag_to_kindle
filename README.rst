Histmag to kindle
=================

Histmag to kindle is simple crawler for
`histmag <http://histmag.org/>`__ web page. Reason I make such crawler
is that I wanted to read historical articles on my kindle ebook reader
but these articles are hard to send in one sane piece.

Installation
------------

::

    $ git clone
    $ cd histmag_to_kindle
    $ python setup.py install

Addtional requirements
----------------------

Right now histmag\_to\_kindle requires
`mailgun <https://www.mailgun.com/>`__ account. Then export your API key
and server to $PATH. Also you need to have KINDLEGEN in your $PATH for generating mobi files.

::

    $ export KINDLEGEN=bin/kindlegen
    $ export MAILGUN_API_KEY=your_api_key
    $ export EMAIL_SERVER=your_email

After this make sure that you add mailgun email to kindle trusted
emails:

Amazon.com -> Your account -> Manage Your Content and Devices -> Log in
-> Settings tab -> Approved Personal Document E-mail List

Usage
-----

.. code:: python

    import os
    from histmag_to_kindle import Parser, HtmlGenerator, send_email_to_kindle

    parser = Parser(http_link_to_desired article)
    articles = parser.get_articles()
    generator = generate_mobi(articles)
    send_email_to_kindle(kindle_email='your_kindle_email', name=os.path.join(generator, 'histmag.mobi'))

Word from author
----------------

`Histmag <http://histmag.org/>`__ is great service but it needs money to
run so disable adblock or buy their books.
