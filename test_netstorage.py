import unittest, uuid, os

from akamai.netstorage import Netstorage
from spike import secrets


class TestNetstorage(unittest.TestCase):
    
    def setUp(self):
        self.cpcode_path = "/360949/"
        self.temp_dir = str(uuid.uuid4())
        self.temp_file = str(uuid.uuid4()) + ".txt"

        self.ns = Netstorage("astin-nsu.akamaihd.net", "astinastin", secrets.key)
        
    def tearDown(self):
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    def test_netstorage(self):
        # mkdir
        res = self.ns.mkdir(self.cpcode_path + self.temp_dir)
        self.assertEqual(200, res.status_code)

        # upload
        with open(self.temp_file, 'wt') as f:
            print("Hello, Netstorage API World!", file=f)
        res = self.ns.upload(self.temp_file, self.cpcode_path + self.temp_dir + "/" + self.temp_file)
        self.assertEqual(200, res.status_code)

        # delete
        res = self.ns.delete(self.cpcode_path + self.temp_dir + "/" + self.temp_file)
        self.assertEqual(200, res.status_code)

        # rmdir
        res = self.ns.rmdir(self.cpcode_path + self.temp_dir)
        self.assertEqual(200, res.status_code)


if __name__ == '__main__':
    unittest.main()

# from akamai.netstorage import Netstorage
# from spike import secrets

# ns = Netstorage("astin-nsu.akamaihd.net", "astinastin" , secrets.key)
# # ns = Netstorage("astin-nsu.akamaihd.net", "astinaspera" , secrets.key)
# res = ns.upload("/Users/achoi/Desktop/1459911370.523473.py.zip", "/360949/abcdef.py.zip")
# print(res)

# mkdir
# upload -> download -> dir -> stat -> symlink -> mtime -> du
# delete -> rmdir