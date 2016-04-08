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
res = ns.upload("/Users/achoi/Desktop/1459911370.523473.py.zip", "/360949/abcdef.zip")
print(res)