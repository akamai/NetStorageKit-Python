NetstorageAPI: Akamai Netstorage API Interface
================================================

NetstorageAPI does interface Akamai Netstorage (File/Object Store) API and uses `requests <https://github.com/kennethreitz/requests>`.
NetstorageAPI supports Python 2.6 — 3.5, and runs great on PyPy like `requests <https://github.com/kennethreitz/requests>`.


Installation
------------

To install netstorage:  

.. code-block:: bash

    $ pip install netstorageapi


Example
-------

.. code-block:: python

    >>> from netstorageapi import Netstorage
    >>> ns = Netstorage('astin-nsu.akamaihd.net', 'astinastin', 'YOUR_KEY')
    >>> local_source = 'hello.txt'
    >>> netstorage_destination = '/YOUR_CPCODE/hello.txt' # or '/YOUR_CPCODE/' is same.
    >>> ok, response = ns.upload(local_source, netstorage_destination)
    >>> ok
    >>> True # means 200 OK ; if False, it's not 200 OK.
    >>> response
    >>> 
    >>> # WARN: Don't expose the KEY which is 'YOUR_KEY' on public repository.

