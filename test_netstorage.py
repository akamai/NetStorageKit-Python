# from akamai.netstorage import Netstorage
# import unittest


# class TestNetstorage(unittest.TestCase):
    
#     def setUp(self):
#         pass

#     def tearDown(self):
#         pass

#     def test_(self):
#     	pass


# if __name__ == '__main__':
# 	unittest.main()

from akamai.netstorage import Netstorage

ns = Netstorage("astin-nsu.akamaihd.net", "astinastin" ,"key")
res = ns.upload("/Users/achoi/Projects/netstorage-python/spike/mkdir.py", "/360949/abcdef.py")
print(res)