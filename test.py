from akamai.netstorage import Netstorage


ns = Netstorage("astin-nsu.akamaihd.net", "astinastin" ,"key")
res = ns.download("/360949/rtmpplayer110.html")
print(res.text)