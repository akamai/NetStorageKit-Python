import base64, time, random, hmac
import requests


class Netstorage:
    
    def __init__(self, hostname, keyname, key):
        self.hostname = hostname
        self.keyname = keyname
        self.key = key
        
        self.METHODS = {'GET': 0, 'POST': 1, 'PUT': 2}


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

        response = None
        if kwargs['method'] == self.METHODS['GET']:
            headers = { 'X-Akamai-ACS-Action': acs_action,
                        'X-Akamai-ACS-Auth-Data': acs_auth_data,
                        'X-Akamai-ACS-Auth-Sign': acs_auth_sign }
            response = requests.get(request_url, headers=headers)

        elif kwargs['method'] == self.METHODS['POST']:
            headers = { 'X-Akamai-ACS-Action': acs_action,
                        'X-Akamai-ACS-Auth-Data': acs_auth_data,
                        'X-Akamai-ACS-Auth-Sign': acs_auth_sign,
                        'Content-Length': 0,
                        'Accept-Encoding': 'identity' }
            response = requests.post(request_url, headers=headers)
        elif kwargs['method'] == self.METHODS['PUT']:
            headers = { 'X-Akamai-ACS-Action': acs_action,
                        'X-Akamai-ACS-Auth-Data': acs_auth_data,
                        'X-Akamai-ACS-Auth-Sign': acs_auth_sign,
                        'Content-Length': kwargs['size'],
                        'Accept-Encoding': 'identity' }
            response = requests.put(request_url, headers=headers, data=kwargs['data'])

        print(headers)
        return response


    def dir(self, path):
        return self.request(action='dir&format=xml', 
                            method=self.METHODS['GET'], 
                            path=path)

    def download(self, path):
        return self.request(action='download', 
                            method=self.METHODS['GET'], 
                            path=path)

    def du(self, path):
        return self.request(action='du&format=xml',
                            method=self.METHODS['GET'], 
                            path=path)

    def stat(self, path):
        return self.request(action='stat&format=xml',
                            method=self.METHODS['GET'],
                            path=path)

    def mkdir(self, path):
        return self.request(action='mkdir',
                            method=self.METHODS['POST'], 
                            path=path)

    def rmdir(self, path):
        return self.request(action='rmdir',
                            method=self.METHODS['POST'],
                            path=path)

    def mtime(self, path, mtime):
        return self.request(action='mtime&format=xml&mtime={}'.format(mtime),
                            method=self.METHODS['POST'], 
                            path=path)

    def delete(self, path):
        return self.request(action='delete',
                            method=self.METHODS['POST'], 
                            path=path)

    def quick_delete(self, path):
        return self.request(action='quick-delete&quick-delete=imreallyreallysure',
                            method=self.METHODS['POST'], 
                            path=path)

    def rename(self, source, destination):
        from urllib.parse import quote_plus
        return self.request(action='rename&destination={}'.format(quote_plus(destination)),
                            method=self.METHODS['POST'],
                            path=source)

    def upload(self, source, destination):
        import os
        data = None
        try:
            f = os.open(source, os.O_RDONLY)
            data = os.read(f, 0)
        except Exception as e:
            return e

        from hashlib import sha256
        sha256_ = sha256(data).hexdigest()
        f_size = len(data)
        
        return self.request(action='upload&upload-type=binary&size={}&sha256={}'.format(f_size, sha256_),
                            method=self.METHODS['PUT'],
                            size=f_size,
                            data=data,
                            path=destination)
