from akamai.netstorage import Netstorage
from spike import secrets

aaa = Netstorage("astin-nsu.akamaihd.net", "astinastin", secrets.key)

ok, _ = aaa.upload('/Users/achoi/Desktop/hello1234.mov', '/360949/astinapi/3312232.mov')
# print(res)
print(ok)

# bbb = Netstorage("astinobj-nsu.akamaihd.net", "astinobj", secrets.key_obj)

# ok, _ = bbb.upload('/Users/achoi/Desktop/hello1234.mov', '/407617/3312232.mov')