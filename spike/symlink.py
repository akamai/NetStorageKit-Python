import base64
import time
import random
import hmac
import requests
import secrets

key_name = "astinastin"
key = secrets.key
hostname = "astin-nsu.akamaihd.net"
acs_action = "version=1&action=symlink&target=%2F360949%2Frtmpplayer11.html"
path = "/360949/rtmpplayer11.html_lnk"

acs_auth_data = "5, 0.0.0.0, 0.0.0.0, {}, {}, {}".format(time.time(), str(random.getrandbits(32)), key_name)
sign_string = "{}\nx-akamai-acs-action:{}\n".format(path, acs_action)
message = acs_auth_data + sign_string

hash_ = hmac.new(key.encode(), message.encode(), "sha256").digest()
acs_auth_sign = base64.b64encode(hash_)

url = "http://{}{}".format(hostname, path)
headers = { 'X-Akamai-ACS-Action': acs_action,
            'X-Akamai-ACS-Auth-Data': acs_auth_data,
            'X-Akamai-ACS-Auth-Sign': acs_auth_sign,
            'Content-Length': 0, 
            'Accept-Encoding': 'identity' }

response = requests.post(url, headers=headers)

print(response.headers)
print(response.text)
print(response.status_code)