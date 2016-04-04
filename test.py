from akamai.netstorage import Netstorage


ns = Netstorage("astin-nsu.akamaihd.net", "astinastin" ,"NIaOox2Z41Qf975MO2v9x78MC75HJA35Y11zF5XSX595cDCsIr")
res = ns.download("/360949/rtmpplayer110.html")
print(res.text)