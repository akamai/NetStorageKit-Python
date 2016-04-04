import base64, time, random, hmac
import requests


class Netstorage:
    
    def __init__(self, hostname, keyname, key):
        self.hostname = hostname
        self.keyname = keyname
        self.key = key

        self.acs_action = "version=1&action={}&format=xml"
        self.acs_auth_data = "5, 0.0.0.0, 0.0.0.0, {}, {}, {}"
        self.sign_string = "{}\nx-akamai-acs-action:{}\n"

        self.message = ""

    def dir(self, path):
        self.acs_action = self.acs_action.format("dir")
        self.acs_auth_data = self.acs_auth_data.format(time.time(), str(random.getrandbits(32)), self.keyname)
        self.sign_string = self.sign_string.format(path, self.acs_action)

        message = self.acs_auth_data + self.sign_string

        hash_ = hmac.new(self.key.encode(), message.encode(), "sha256").digest()
        acs_auth_sign = base64.b64encode(hash_)

        request_url = "http://{}{}".format(self.hostname, path)
        headers = { 'X-Akamai-ACS-Action': self.acs_action,
                    'X-Akamai-ACS-Auth-Data': self.acs_auth_data,
                    'X-Akamai-ACS-Auth-Sign': acs_auth_sign }

        response = requests.get(request_url, headers=headers)

        return response

    def download(self, path):
        self.acs_action = self.acs_action.format("download")
        self.acs_auth_data = self.acs_auth_data.format(time.time(), str(random.getrandbits(32)), self.keyname)
        self.sign_string = self.sign_string.format(path, self.acs_action)

        message = self.acs_auth_data + self.sign_string

        hash_ = hmac.new(self.key.encode(), message.encode(), "sha256").digest()
        acs_auth_sign = base64.b64encode(hash_)

        request_url = "http://{}{}".format(self.hostname, path)
        headers = { 'X-Akamai-ACS-Action': self.acs_action,
                    'X-Akamai-ACS-Auth-Data': self.acs_auth_data,
                    'X-Akamai-ACS-Auth-Sign': acs_auth_sign }

        response = requests.get(request_url, headers=headers)

        return response
