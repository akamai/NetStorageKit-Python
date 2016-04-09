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
from spike import secrets

ns = Netstorage("astin-nsu.akamaihd.net", "astinastin" , secrets.key)
res = ns.upload("/Users/achoi/Desktop/1459911370.523473.py", "/360949/abcdef.py")
print(res)