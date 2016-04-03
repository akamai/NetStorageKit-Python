from akamai.netstorage import Netstorage


ns = Netstorage("astin-nsu.akamaihd.net", "astinastin" ,"key")
res = ns.dir("/360949")
print(res.text)