from urllib.parse import quote_plus
from hashlib import sha256
import base64, time, random, hmac, os

import requests


class Netstorage:    
    def __init__(self, hostname, keyname, key):
        self.hostname = hostname
        self.keyname = keyname
        self.key = key
        
    def download_data_from_response(self, response, destination):
        f_size = -1
        if destination and response.status_code == 200:
            with open(destination, 'bw') as f:
                f_size = f.write(response.content)
        
        return f_size
    
    def upload_data_to_request(self, source):
        data = b''
        f = os.open(source, os.O_RDONLY)
        try:
            while True:
                chunk = os.read(f, 1024*1024)
                if chunk:
                    data += chunk
                else:
                    break
        finally:
            os.close(f)
        
        return data

    def request(self, **kwargs):
        acs_action = "version=1&action={}".format(kwargs['action'])
        acs_auth_data = "5, 0.0.0.0, 0.0.0.0, {}, {}, {}".format(
            time.time(), 
            str(random.getrandbits(32)), 
            self.keyname)
        sign_string = "{}\nx-akamai-acs-action:{}\n".format(kwargs['path'], acs_action)
        message = acs_auth_data + sign_string

        hash_ = hmac.new(self.key.encode(), message.encode(), "sha256").digest()
        acs_auth_sign = base64.b64encode(hash_)
        
        request_url = "http://{}{}".format(self.hostname, kwargs['path'])
        
        headers = { 'X-Akamai-ACS-Action': acs_action,
                    'X-Akamai-ACS-Auth-Data': acs_auth_data,
                    'X-Akamai-ACS-Auth-Sign': acs_auth_sign }
        response = None
        if kwargs['method'] == 'GET':
            response = requests.get(request_url, headers=headers)
            if kwargs['action'] == 'download':
                self.download_data_from_response(response, kwargs['destination'])

        elif kwargs['method'] == 'POST':
            headers['Content-Length'] = 0
            headers['Accept-Encoding'] = 'identity'
            response = requests.post(request_url, headers=headers)

        elif kwargs['method'] == 'PUT':
            headers['Content-Length'] = kwargs['size']
            headers['Accept-Encoding'] = 'identity'
            response = requests.put(request_url, headers=headers, data=kwargs['data'])

        return response

    def dir(self, path):
        return self.request(action='dir&format=xml', 
                            method='GET', 
                            path=path)

    def download(self, path, destination=''):
        return self.request(action='download', 
                            method='GET',
                            path=path,
                            destination=destination)

    def du(self, path):
        return self.request(action='du&format=xml',
                            method='GET', 
                            path=path)

    def stat(self, path):
        return self.request(action='stat&format=xml',
                            method='GET',
                            path=path)

    def mkdir(self, path):
        return self.request(action='mkdir',
                            method='POST', 
                            path=path)

    def rmdir(self, path):
        return self.request(action='rmdir',
                            method='POST',
                            path=path)

    def mtime(self, path, mtime):
        return self.request(action='mtime&format=xml&mtime={}'.format(mtime),
                            method='POST', 
                            path=path)

    def delete(self, path):
        return self.request(action='delete',
                            method='POST', 
                            path=path)

    def quick_delete(self, path):
        return self.request(action='quick-delete&quick-delete=imreallyreallysure',
                            method='POST', 
                            path=path)

    def rename(self, source, destination):
        return self.request(action='rename&destination={}'.format(quote_plus(destination)),
                            method='POST',
                            path=source)

    def symlink(self, target, destination):
        return self.request(action='symlink&target={}'.format(quote_plus(target)),
                            method='POST',
                            path=destination)
    
    def upload(self, source, destination):        
        data = self.upload_data_to_request(source)
        f_size = len(data) # os.stat(source).st_size
        sha256_ = sha256(data).hexdigest()
        
        return self.request(action='upload&upload-type=binary&size={}&sha256={}'.format(f_size, sha256_),
                            method='PUT',
                            size=f_size,
                            data=data,
                            path=destination)