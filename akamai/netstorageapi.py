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
import base64, hmac, mmap, ntpath, random, sys, time
if sys.version_info[0] >= 3:
    from urllib.parse import quote_plus, quote # python3
else:
    from urllib import quote_plus, quote # python2
    
import requests


class Netstorage:    
    def __init__(self, hostname, keyname, key):
        self.hostname = hostname
        self.keyname = keyname
        self.key = key
        
    def _download_data_from_response(self, response, destination, chunk_size=16*1024):
        if destination and response.status_code == 200:
            with open(destination, 'wb') as f:
                for chunk in response.iter_content(chunk_size):
                    f.write(chunk)
                    f.flush()
    
    def _upload_data_to_request(self, source):
        with open(source, 'rb') as f:
            mmapped_data = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

        return mmapped_data

    def _request(self, **kwargs):
        path = quote(kwargs['path'])
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
        
        request_url = "http://{0}{1}".format(self.hostname, path)
        
        headers = { 'X-Akamai-ACS-Action': acs_action,
                    'X-Akamai-ACS-Auth-Data': acs_auth_data,
                    'X-Akamai-ACS-Auth-Sign': acs_auth_sign }
        
        response = None
        if kwargs['method'] == 'GET':
            response = requests.get(request_url, headers=headers)
            if kwargs['action'] == 'download':
                self._download_data_from_response(response, kwargs['destination'])

        elif kwargs['method'] == 'POST':
            headers['Content-Length'] = 0
            headers['Accept-Encoding'] = 'identity'
            response = requests.post(request_url, headers=headers)

        elif kwargs['method'] == 'PUT':
            mmapped_data = kwargs['data']
            headers['Content-Length'] = kwargs['size']
            headers['Accept-Encoding'] = 'identity'
            response = requests.put(request_url, headers=headers, data=mmapped_data)
            mmapped_data.close()
            
        return response.status_code == 200, response

    def dir(self, path):
        return self._request(action='dir&format=xml', 
                            method='GET', 
                            path=path)

    def download(self, path, destination=''):
        file_name = ntpath.basename(path)
        if path and not destination:
            destination = file_name
        elif path and not ntpath.basename(destination): 
            destination = "{0}{1}".format(destination, file_name)
            
        return self._request(action='download', 
                            method='GET',
                            path=path,
                            destination=destination)

    def du(self, path):
        return self._request(action='du&format=xml',
                            method='GET', 
                            path=path)

    def stat(self, path):
        return self._request(action='stat&format=xml',
                            method='GET',
                            path=path)

    def mkdir(self, path):
        return self._request(action='mkdir',
                            method='POST', 
                            path=path)

    def rmdir(self, path):
        return self._request(action='rmdir',
                            method='POST',
                            path=path)

    def mtime(self, path, mtime):
        return self._request(action='mtime&format=xml&mtime={0}'.format(mtime),
                            method='POST', 
                            path=path)

    def delete(self, path):
        return self._request(action='delete',
                            method='POST', 
                            path=path)

    def quick_delete(self, path):
        return self._request(action='quick-delete&quick-delete=imreallyreallysure',
                            method='POST', 
                            path=path)

    def rename(self, source, destination):
        return self._request(action='rename&destination={0}'.format(quote_plus(destination)),
                            method='POST',
                            path=source)

    def symlink(self, target, destination):
        return self._request(action='symlink&target={0}'.format(quote_plus(target)),
                            method='POST',
                            path=destination)
    
    def upload(self, source, destination):
        if source and not ntpath.basename(destination):
            destination = "{0}{1}".format(destination, ntpath.basename(source))

        data = self._upload_data_to_request(source)
        f_size = len(data)
        sha256_ = sha256(data).hexdigest()
        return self._request(action='upload&size={0}&sha256={1}'.format(f_size, sha256_),
                            method='PUT',
                            size=f_size,
                            data=data,
                            path=destination)