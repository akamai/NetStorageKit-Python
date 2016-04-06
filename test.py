from akamai.netstorage import Netstorage


ns = Netstorage("astin-nsu.akamaihd.net", "astinastin" ,"key")
res = ns.stat("/360949")
print(res.text)