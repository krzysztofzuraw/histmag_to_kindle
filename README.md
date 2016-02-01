Histmag to kindle
=================

Histmag to kindle is simple crawler for [histmag](http://histmag.org/) web page.
Reason I make such crawler is that I wanted to read historical articles on my kindle ebook reader but these articles
are hard to send in one sane piece.

Installation
------------
```
$ git clone
$ cd histmag_to_kindle
$ python setup.py install
```

Addtional requirements
----------------------
Right now histmag_to_kindle requires [mailgun](https://www.mailgun.com/) account.
Then add your Api key and server to .histmag_conf in your home directory
```
$ cat ~/.histmag_conf
```
>[sender]
>
>api_key = YOUR_MAILGUN_API_KEY
>
>server = YOUR_MAIL_SERVER

After this make sure that you add mailgun email to kindle trusted emails:

Amazon.com -> Your account -> Manage Your Content and Devices -> Log in -> Settings tab -> Approved Personal Document E-mail List

Usage
-----

```python
import os
from histmag_to_kindle import Parser, HtmlGenerator, send_email_to_kindle

parser = Parser(http_link_to_desired article)
articles = parser.get_articles()
generator = generate_mobi(articles)
send_email_to_kindle(kindle_email='your_kindle_email', name=os.path.join(generator, 'histmag.mobi'))
```


Word from author
----------------

[Histmag](http://histmag.org/) is great service but it needs money to run so disable adblock or buy their books.
