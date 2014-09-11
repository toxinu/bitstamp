========
Bitstamp
========

Python module for Bitstamp_ API.

Installation
------------

::

    pip install git+https://socketubs@bitbucket.org/socketubs/bitstamp.git
    cd bitstamp
    python setup.py install

Usage
-----

Get your `Bitstamp` module ::

    >>> from bitstamp import Bitstamp
    >>> api = Bitstamp()

Documentation
-------------

You can build the documentation with Sphinx: ::

    cd docs
    make html
    open build/html/index.html

Tests
-----

::

    pip install - requirements-dev.txt
    coverage run -m unittest discover tests
    coverage html


.. _Bitstamp: https://www.bitstamp.net/api/
