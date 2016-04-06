import base64
import time
import random
import hmac
import requests
import secrets
from hashlib import sha256


key_name = "astinastin"
key = secrets.key
hostname = "astin-nsu.akamaihd.net"

with open('symlink.py', 'r') as f:
    data = f.read()

sha256_ = sha256(data.encode()).hexdigest()
size = len(data)

acs_action = "version=1&action=upload&size={}&sha256={}".format(size, sha256_)

path = "/360949/" + str(time.time()) + ".py"

acs_auth_data = "5, 0.0.0.0, 0.0.0.0, {}, {}, {}".format(time.time(), str(random.getrandbits(32)), key_name)
sign_string = "{}\nx-akamai-acs-action:{}\n".format(path, acs_action)
message = acs_auth_data + sign_string

hash_ = hmac.new(key.encode(), message.encode(), "sha256").digest()
acs_auth_sign = base64.b64encode(hash_)

url = "http://{}{}".format(hostname, path)
headers = { 'X-Akamai-ACS-Action': acs_action,
            'X-Akamai-ACS-Auth-Data': acs_auth_data,
            'X-Akamai-ACS-Auth-Sign': acs_auth_sign,
            'Content-Length': size, 
            'Accept-Encoding': 'identity' }

response = requests.put(url, headers=headers, data=data)

print(response.headers)
print(response.text)