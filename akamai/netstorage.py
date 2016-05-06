from hashlib import sha256
import base64, hmac, mmap, ntpath, random, time
try:
    from urllib import quote_plus # python2
except ImportError:
    from urllib.parse import quote_plus # python3
    
import requests


class Netstorage:    
    def __init__(self, hostname, keyname, key):
        self.hostname = hostname
        self.keyname = keyname
        self.key = key
        
    def _download_data_from_response(self, response, destination, chunk_size=16*1024):
        if destination and response.status_code == 200:
            with open(destination, 'bw') as f:
                for chunk in response.iter_content(chunk_size):
                    f.write(chunk)
                    f.flush()
    
    def _upload_data_to_request(self, source):
        with open(source, 'br') as f:
            mmapped_data = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

        return mmapped_data

    def _request(self, **kwargs):
        acs_action = "version=1&action={}".format(kwargs['action'])
        acs_auth_data = "5, 0.0.0.0, 0.0.0.0, {}, {}, {}".format(
            int(time.time()), 
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
            destination = "{}{}".format(destination, file_name)
            
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
        return self._request(action='mtime&format=xml&mtime={}'.format(mtime),
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
        return self._request(action='rename&destination={}'.format(quote_plus(destination)),
                            method='POST',
                            path=source)

    def symlink(self, target, destination):
        return self._request(action='symlink&target={}'.format(quote_plus(target)),
                            method='POST',
                            path=destination)
    
    def upload(self, source, destination):
        data = self._upload_data_to_request(source)
        f_size = len(data) # os.stat(source).st_size
        sha256_ = sha256(data).hexdigest()
        return self._request(action='upload&size={}&sha256={}'.format(f_size, sha256_),
                            method='PUT',
                            size=f_size,
                            data=data,
                            path=destination)