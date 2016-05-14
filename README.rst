NetstorageAPI: Akamai Netstorage API for Python
===============================================

.. image:: https://img.shields.io/pypi/v/netstorageapi.svg
    :target: https://pypi.python.org/pypi/netstorageapi

NetstorageAPI is Akamai Netstorage (File/Object Store) API for Python and uses `requests <http://docs.python-requests.org>`_.
NetstorageAPI supports Python 2.6 — 3.5, and runs great on PyPy as `requests <http://docs.python-requests.org>`_.


Installation
------------

To install NetstorageAPI:  

.. code-block:: bash

    $ pip install netstorageapi


Example
-------

.. code-block:: python

    >>> from akamai.netstorageapi import Netstorage
    >>>
    >>> NS_HOSTNAME = 'astin-nsu.akamaihd.net'
    >>> NS_KEYNAME = 'astinastin'
    >>> NS_KEY = 'xxxxxxxxxx' # Don't expose NS_KEY on public repository.
    >>> NS_CPCODE = '360949'
    >>>
    >>> ns = Netstorage(NS_HOSTNAME, NS_KEYNAME, NS_KEY)
    >>> local_source = 'hello.txt'
    >>> netstorage_destination = '/{0}/hello.txt'.format(NS_CPCODE) # or '/{0}/'.format(NS_CPCODE) is same.
    >>> ok, response = ns.upload(local_source, netstorage_destination)
    >>> ok
    True # means 200 OK; If False, it's not 200 OK
    >>> response
    <Response [200]> # Response object from requests.get|post|put
    >>> response.status_code
    200
    >>> response.content # response.content.decode() for python3
    '<HTML>Request Processed</HTML>\n'
    >>>
    >>> response.encoding 
    'ISO-8859-1' # requests makes educated guesses about the encoding of the response based on the HTTP headers.
    >>> response.encoding = 'utf-8' # You can change the response encoding.
    >>>

Methods
-------

.. code-block:: python

    >>> ns.delete(NETSTORAGE_PATH)
    >>> ns.dir(NETSTORAGE_PATH)
    >>> ns.download(NETSTORAGE_SOURCE, LOCAL_DESTINATION)
    >>> ns.du(NETSTORAGE_PATH)
    >>> ns.list(NETSTORAGE_PATH)
    >>> ns.mkdir(NETSTORAGE_PATH + DIRECTORY_NAME)
    >>> ns.mtime(NETSTORAGE_PATH, TIME) # ex) TIME: int(time.time())
    >>> ns.rmdir(NETSTORAGE_PATH)
    >>> ns.stat(NETSTORAGE_PATH)
    >>> ns.symlink(NETSTORAGE_SOURCE, NETSTORAGE_TARGET)
    >>> ns.upload(LOCAL_SOURCE, NETSTORAGE_DESTINATION)
    >>>
    >>>
    >>> # INFO: Return (True/False, Response Object from requests.get|post|put)
    >>> #       True means 200 OK.
    >>> # INFO: Can "upload" Only a single file, not directory.
    >>> # WARN: Can raise FILE related error in "download" and "upload".
    >>>


Test
----

You can test all above methods with `unittest script <https://github.com/AstinCHOI/netstorage-python/blob/master/test_netstorage.py>`_
(NOTE: You should input NS_HOSTNAME, NS_KEYNAME, NS_KEY and NS_CPCODE in the script):

.. code-block:: bash

    $ python test_netstorage.py
    [TEST] dir /360949 done
    [TEST] mkdir /360949/048a30de-e6af-45d0-81e6-fc38bf985fb9 done
    [TEST] upload 6ae30c1a-289a-42a7-9d3d-f634357098b3.txt to /360949/048a30de-e6af-45d0-81e6-fc38bf985fb9/6ae30c1a-289a-42a7-9d3d-f634357098b3.txt done
    [TEST] du done
    [TEST] mtime /360949/048a30de-e6af-45d0-81e6-fc38bf985fb9/6ae30c1a-289a-42a7-9d3d-f634357098b3.txt to 1462674018 done
    [TEST] stat done
    [TEST] symlink /360949/048a30de-e6af-45d0-81e6-fc38bf985fb9/6ae30c1a-289a-42a7-9d3d-f634357098b3.txt to /360949/048a30de-e6af-45d0-81e6-fc38bf985fb9/6ae30c1a-289a-42a7-9d3d-f634357098b3.txt_lnk done
    [TEST] rename /360949/048a30de-e6af-45d0-81e6-fc38bf985fb9/6ae30c1a-289a-42a7-9d3d-f634357098b3.txt to /360949/048a30de-e6af-45d0-81e6-fc38bf985fb9/6ae30c1a-289a-42a7-9d3d-f634357098b3.txt_rename done
    [TEST] download /360949/048a30de-e6af-45d0-81e6-fc38bf985fb9/6ae30c1a-289a-42a7-9d3d-f634357098b3.txt_rename done
    [TEST] delete /360949/048a30de-e6af-45d0-81e6-fc38bf985fb9/6ae30c1a-289a-42a7-9d3d-f634357098b3.txt_rename done
    [TEST] delete /360949/048a30de-e6af-45d0-81e6-fc38bf985fb9/6ae30c1a-289a-42a7-9d3d-f634357098b3.txt_lnk done
    [TEST] rmdir /360949/048a30de-e6af-45d0-81e6-fc38bf985fb9 done
    [TEARDOWN] remove 6ae30c1a-289a-42a7-9d3d-f634357098b3.txt from local done
    [TEARDOWN] remove 6ae30c1a-289a-42a7-9d3d-f634357098b3.txt_rename from local done
    .
    ----------------------------------------------------------------------
    Ran 1 test in 3.705s

    OK


Command
-------

You can run the `script <https://github.com/AstinCHOI/netstorage-python/blob/master/cms_netstorage.py>`_ with command line parameters.

.. code-block:: bash

    $ python cms_netstorage.py -H astin-nsu.akamaihd.net -k astinastin -K xxxxxxxxxx -a dir /360949
    
Use -h or --help option for more detail.