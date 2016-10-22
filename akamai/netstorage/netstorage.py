# -*- coding: utf-8 -*-

# Original author: Astin Choi <achoi@akamai.com>

# Copyright 2016 Akamai Technologies http://developer.akamai.com.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from hashlib import sha256
import base64, hmac, mmap, ntpath, os, random, sys, time
if sys.version_info[0] >= 3:
    from urllib.parse import quote_plus, quote # python3
else:
    from urllib import quote_plus, quote # python2
    
import requests


class NetstorageError(Exception):
    """Base-class for all exceptions raised by Netstorage Class"""


class Netstorage:
    def __init__(self, hostname, keyname, key, ssl=False):
        if not (hostname and keyname and key):
            raise NetstorageError('[NetstorageError] You should input netstorage hostname, keyname and key all')

        self.hostname = hostname
        self.keyname = keyname
        self.key = key
        self.ssl = 's' if ssl else ''
        
        
    def _download_data_from_response(self, response, ns_path, local_destination, chunk_size=16*1024):
        if not local_destination:
            local_destination = ntpath.basename(ns_path)
        elif os.path.isdir(local_destination):
            local_destination = os.path.join(local_destination, ntpath.basename(ns_path)) 

        if response.status_code == 200:
            try:
                with open(local_destination, 'wb') as f:
                    for chunk in response.iter_content(chunk_size):
                        f.write(chunk)
                        f.flush()
            except Exception as e:
                raise NetstorageError(e)
    
    def _upload_data_to_request(self, source):
        mmapped_data = None
        try:
            with open(source, 'rb') as f:
                mmapped_data = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        except Exception as e:
            if mmapped_data: mmapped_data.close()
            raise NetstorageError(e)
        
        return mmapped_data

    def _request(self, **kwargs):
        path = kwargs['path']
        if not path.startswith('/'):
            raise NetstorageError('[NetstorageError] Invalid netstorage path')

        path = quote(path)
        acs_action = "version=1&action={0}".format(kwargs['action'])
        acs_auth_data = "5, 0.0.0.0, 0.0.0.0, {0}, {1}, {2}".format(
            int(time.time()), 
            str(random.getrandbits(32)), 
            self.keyname)
        sign_string = "{0}\nx-akamai-acs-action:{1}\n".format(path, acs_action)
        message = acs_auth_data + sign_string
        if sys.version_info[0] >= 3:
            hash_ = hmac.new(self.key.encode(), message.encode(), "sha256").digest()
        else:
            hash_ = hmac.new(self.key.encode(), message.encode(), sha256).digest()
            
        acs_auth_sign = base64.b64encode(hash_)
        
        request_url = "http{0}://{1}{2}".format(self.ssl, self.hostname, path)
        
        headers = { 'X-Akamai-ACS-Action': acs_action,
                    'X-Akamai-ACS-Auth-Data': acs_auth_data,
                    'X-Akamai-ACS-Auth-Sign': acs_auth_sign,
                    'Accept-Encoding': 'identity'
        }
        
        response = None
        if kwargs['method'] == 'GET':
            response = requests.get(request_url, headers=headers)
            if kwargs['action'] == 'download':
                self._download_data_from_response(response, kwargs['path'], kwargs['destination'])

        elif kwargs['method'] == 'POST':
            response = requests.post(request_url, headers=headers)

        elif kwargs['method'] == 'PUT': # Use only upload
            mmapped_data = self._upload_data_to_request(kwargs['source'])
            response = requests.put(request_url, headers=headers, data=mmapped_data)
            mmapped_data.close()
            
        return response.status_code == 200, response

    def dir(self, ns_path):
        return self._request(action='dir&format=xml', 
                            method='GET', 
                            path=ns_path)

    def download(self, ns_source, local_destination=''):
        if ns_source.endswith('/'):
            raise NetstorageError("[NetstorageError] Nestorage download path shouldn't be a directory: {0}".format(ns_source))
        return self._request(action='download', 
                            method='GET',
                            path=ns_source,
                            destination=local_destination)

    def du(self, ns_path):
        return self._request(action='du&format=xml',
                            method='GET', 
                            path=ns_path)

    def stat(self, ns_path):
        return self._request(action='stat&format=xml',
                            method='GET',
                            path=ns_path)

    def mkdir(self, ns_path):
        return self._request(action='mkdir',
                            method='POST', 
                            path=ns_path)

    def rmdir(self, ns_path):
        return self._request(action='rmdir',
                            method='POST',
                            path=ns_path)

    def mtime(self, ns_path, mtime):
        return self._request(action='mtime&format=xml&mtime={0}'.format(mtime),
                            method='POST', 
                            path=ns_path)

    def delete(self, ns_path):
        return self._request(action='delete',
                            method='POST', 
                            path=ns_path)

    def quick_delete(self, ns_path):
        return self._request(action='quick-delete&quick-delete=imreallyreallysure',
                            method='POST', 
                            path=ns_path)

    def rename(self, ns_target, ns_destination):
        return self._request(action='rename&destination={0}'.format(quote_plus(ns_destination)),
                            method='POST',
                            path=ns_target)

    def symlink(self, ns_target, ns_destination):
        return self._request(action='symlink&target={0}'.format(quote_plus(ns_target)),
                            method='POST',
                            path=ns_destination)
    
    def upload(self, local_source, ns_destination):
        if os.path.isfile(local_source):
            if ns_destination[-1] == '/':
                ns_destination = "{0}{1}".format(ns_destination, ntpath.basename(local_source))
        else:
          raise NetstorageError("[NetstorageError] {0} doesn't exist or is directory".format(local_source))  

        return self._request(action='upload',
                            method='PUT',
                            source=local_source,
                            path=ns_destination)