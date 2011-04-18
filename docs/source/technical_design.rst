================
Technical Design
================

**************************
Technology for Server-side
**************************

Python [#f1]_, in combination with the web framework Django [#f2]_, seems to be
an excellent choice.

The Python programming language offers a vast amount of libraries to facilitate
certain tasks hugely, and Django offers a robust framework allowing to access
the application via the browser securely without the need to install additional
software on the client side.

*******************************
Web Server and Database Backend
*******************************

This depends entirely on the Django web framework. Django is able to run under
various environments with different web servers and database backends.

*************************
Client-Server Interaction
*************************

The server will run a single host holding all information, and listen on a port
to accept client interaction via the browser (over HTTP).

The client requirements are simple; the only thing needed is a browser with
JavaScript and HTML5 support. In today's world getting both isn't very hard to
get so requirements are relatively low compared to existing solutions.

**********************************
Asynchronous Source Code Compiling
**********************************

The compile process of source code will run on the same server asynchronously.
Django doesn't provide tools for this by default, but celery [#f3]_ is the
seemingly best tool for that, with excellent support for Django. [#f4]_

.. rubric:: Footnotes

.. [#f1] http://www.python.org
.. [#f2] http://www.djangoproject.org
.. [#f3] http://www.celeryproject.org
.. [#f4] https://github.com/ask/django-celery 
