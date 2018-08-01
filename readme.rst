================
SMTP Mail Server
================ 

An even easier way to send emails!

------------
Installation
------------

You can install this package using pip (if you have GIT installed):

.. code-block:: batch

    > python -m pip install git+https://github.com/richardhob/mail

-----
Usage
-----

Send an email!

.. code-block:: python

    >>> import mail
    >>> dev = mail.Dev(user='', password='', host='', port=587)
    >>> dev.open()
    >>> dev.send('Hi there!', to='', subject='Test')
    >>> dev.close()

Or, send some attachments:

.. code-block:: python

    >>> import mail
    >>> dev = mail.Dev(...)
    >>> dev.open()
    >>> dev.send('Hi Again', 'path/to/test.csv', 'path/to/another.zip', to='',
        subject='Stuffs')
    >>> dev.close()

