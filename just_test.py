from akamai.netstorage import Netstorage
from spike import secrets

aaa = Netstorage("astin-nsu.akamaihd.net", "astinastin", secrets.key)

ok, res = aaa.upload('/Users/achoi/Desktop/3-18.mp4', '/360949/3-12232.mp4')
print(res)
print(ok)