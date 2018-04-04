NetstorageAPI: Akamai Netstorage API for Python
===============================================

.. image:: https://img.shields.io/pypi/v/netstorageapi.svg
    :target: https://pypi.python.org/pypi/netstorageapi

.. image:: https://travis-ci.org/akamai/NetStorageKit-Python.svg?branch=master
    :target: https://travis-ci.org/akamai/NetStorageKit-Python

.. image:: http://img.shields.io/:license-apache-blue.svg 
    :target: https://github.com/akamai/NetStorageKit-Python/blob/master/LICENSE


NetstorageAPI is Akamai Netstorage (File/Object Store) API for Python and uses `requests <http://docs.python-requests.org>`_.
NetstorageAPI supports Python 2.6–2.7 & 3.3–3.6, and runs great on PyPy as `requests <http://docs.python-requests.org>`_.


Installation
------------

To install Netstorage API for Python:  

.. code-block:: bash

    $ pip install netstorageapi


Example
-------

.. code-block:: python

    from akamai.netstorage import Netstorage, NetstorageError
    
    NS_HOSTNAME = 'astin-nsu.akamaihd.net'
    NS_KEYNAME = 'astinapi'
    NS_KEY = 'xxxxxxxxxx' # Don't expose NS_KEY on public repository.
    NS_CPCODE = '360949'
    
    ns = Netstorage(NS_HOSTNAME, NS_KEYNAME, NS_KEY, ssl=False) # ssl is optional (default: False)
    local_source = 'hello.txt'
    netstorage_destination = '/{0}/hello.txt'.format(NS_CPCODE) # or '/{0}/'.format(NS_CPCODE) is same.
    ok, response = ns.upload(local_source, netstorage_destination)
    # "ok": True means 200 OK; If False, it's not 200 OK
    # "response": <Response [200]> # Response object from requests.get|post|put
    print(response.text)
    # '<HTML>Request Processed</HTML>'

Methods
-------

.. code-block:: python

    >>> ns.delete(NETSTORAGE_PATH)
    >>> dir_option = { 
    ...  'max_entries': INTEGER,
    ...  'start': '/start/path',
    ...  'end': '/end/path/',
    ...  'prefix': 'object-prefix',
    ...  'slash': 'both',
    ...  'encoding': 'utf-8'
    ... }
    >>> ns.dir(NETSTORAGE_PATH, dir_option)
    >>> ns.download(NETSTORAGE_SOURCE, LOCAL_DESTINATION)
    >>> ns.du(NETSTORAGE_PATH)
    >>> list_option = {
    ...  'max_entries': INTEGER,
    ...  'end': '/end/path/',
    ...  'encoding': 'utf-8'
    ... }
    >>> ns.list(NETSTORAGE_PATH, list_option)
    >>> ns.mkdir(NETSTORAGE_PATH + DIRECTORY_NAME)
    >>> ns.mtime(NETSTORAGE_PATH, TIME) # ex) TIME: int(time.time())
    >>> ns.quick_delete(NETSTORAGE_DIR) # needs to be enabled on the CP Code
    >>> ns.rename(NETSTORAGE_TARGET, NETSTORAGE_DESTINATION)
    >>> ns.rmdir(NETSTORAGE_DIR)
    >>> ns.stat(NETSTORAGE_PATH)
    >>> ns.stream_download(NETSTORAGE_SOURCE)
    >>> ns.stream_upload(DATA, NETSTORAGE_DESTINATION)
    >>> ns.symlink(NETSTORAGE_TARGET, NETSTORAGE_DESTINATION)
    >>> ns.upload(LOCAL_SOURCE_PATH, NETSTORAGE_DESTINATION, INDEX_ZIP=False)
    >>> 
    >>>
    >>> # INFO: Return (True/False, Response Object from requests.get|post|put)
    >>> #       True means 200 OK.
    >>> # INFO: Can "upload" Only a single file, not a directory.
    >>> #       To use 'INDEX_ZIP=True',
    >>> #       Must turn on index_zip on your Netstorage configuration 
    >>> # WARN: Can raise NetstorageError at all methods.
    >>>


Test
----

You can test all above methods with `unittest script <https://github.com/AstinCHOI/NetStorageKit-Python/blob/master/test/test_netstorage.py>`_
(NOTE: You should input NS_HOSTNAME, NS_KEYNAME, NS_KEY and NS_CPCODE in the script):

.. code-block:: bash

    $ python test/test_netstorage.py
    [TEST] dir /360949 done
    [TEST] mkdir /360949/78fab6cd-f3d8-4fde-a6bf-16dc9c6a22d0 done
    [TEST] upload 2f58618a-cacd-4e03-b3a7-21cc92d1bfe9.txt to /360949/78fab6cd-f3d8-4fde-a6bf-16dc9c6a22d0/2f58618a-cacd-4e03-b3a7-21cc92d1bfe9.txt done
    [TEST] stream_upload /360949/78fab6cd-f3d8-4fde-a6bf-16dc9c6a22d0/stream_2f58618a-cacd-4e03-b3a7-21cc92d1bfe9.txt done
    [TEST] stream_download /360949/78fab6cd-f3d8-4fde-a6bf-16dc9c6a22d0/stream_2f58618a-cacd-4e03-b3a7-21cc92d1bfe9.txt done
    [TEST] du done
    [TEST] mtime /360949/78fab6cd-f3d8-4fde-a6bf-16dc9c6a22d0/2f58618a-cacd-4e03-b3a7-21cc92d1bfe9.txt to 1508482349 done
    [TEST] stat done
    [TEST] symlink /360949/78fab6cd-f3d8-4fde-a6bf-16dc9c6a22d0/2f58618a-cacd-4e03-b3a7-21cc92d1bfe9.txt to /360949/78fab6cd-f3d8-4fde-a6bf-16dc9c6a22d0/2f58618a-cacd-4e03-b3a7-21cc92d1bfe9.txt_lnk done
    [TEST] rename /360949/78fab6cd-f3d8-4fde-a6bf-16dc9c6a22d0/2f58618a-cacd-4e03-b3a7-21cc92d1bfe9.txt to /360949/78fab6cd-f3d8-4fde-a6bf-16dc9c6a22d0/2f58618a-cacd-4e03-b3a7-21cc92d1bfe9.txt_rename done
    [TEST] download /360949/78fab6cd-f3d8-4fde-a6bf-16dc9c6a22d0/2f58618a-cacd-4e03-b3a7-21cc92d1bfe9.txt_rename done
    [TEST] delete /360949/78fab6cd-f3d8-4fde-a6bf-16dc9c6a22d0/stream_2f58618a-cacd-4e03-b3a7-21cc92d1bfe9.txt done
    [TEST] delete /360949/78fab6cd-f3d8-4fde-a6bf-16dc9c6a22d0/2f58618a-cacd-4e03-b3a7-21cc92d1bfe9.txt_rename done
    [TEST] delete /360949/78fab6cd-f3d8-4fde-a6bf-16dc9c6a22d0/2f58618a-cacd-4e03-b3a7-21cc92d1bfe9.txt_lnk done
    [TEST] rmdir /360949/78fab6cd-f3d8-4fde-a6bf-16dc9c6a22d0 done
    [TEARDOWN] remove 2f58618a-cacd-4e03-b3a7-21cc92d1bfe9.txt from local done
    [TEARDOWN] remove 2f58618a-cacd-4e03-b3a7-21cc92d1bfe9.txt_rename from local done
    .

    [TEST] Invalid ns path NetstorageError test done
    [TEST] Invalid local path NetstorageError test done
    [TEST] Download directory path NetstorageError test done
    .
    ----------------------------------------------------------------------
    Ran 2 tests in x.xxxs
    
    OK


Command
-------

You can run the `script <https://github.com/AstinCHOI/NetStorageKit-Python/blob/master/cms_netstorage.py>`_ with command line parameters.

.. code-block:: bash

    $ python cms_netstorage.py -H astin-nsu.akamaihd.net -k astinapi -K xxxxxxxxxx -a dir /360949
    
Use -h or --help option for more detail.


Author
------

Astin Choi (achoi@akamai.com)  


License
-------

Copyright 2016 Akamai Technologies, Inc.  All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at `<http://www.apache.org/licenses/LICENSE-2.0>`_.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.