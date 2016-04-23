import unittest, uuid, os, time
import xml.etree.ElementTree as ET

from akamai.netstorage import Netstorage
from spike import secrets

# TODO:
# download
# dir with refactoring
class TestNetstorage(unittest.TestCase):
    
    def setUp(self):
        self.cpcode_path = "/360949/"
        self.temp_dir = str(uuid.uuid4())
        self.temp_file = str(uuid.uuid4()) + ".txt"

        self.ns = Netstorage("astin-nsu.akamaihd.net", "astinastin", secrets.key)
        
    def tearDown(self):
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    def is_file_exist(self, name):
        pass

    def is_dir_exist(self, name):
        pass

    def test_netstorage(self):
        # mkdir
        res = self.ns.mkdir(self.cpcode_path + self.temp_dir)
        self.assertEqual(200, res.status_code)

        # upload
        with open(self.temp_file, 'wt') as f:
            print("Hello, Netstorage API World!", file=f)
        res = self.ns.upload(self.temp_file, self.cpcode_path + self.temp_dir + "/" + self.temp_file)
        self.assertEqual(200, res.status_code)

        # du
        res = self.ns.du(self.cpcode_path + self.temp_dir)
        self.assertEqual(200, res.status_code)
        xml_tree = ET.fromstring(res.text)
        self.assertEqual(str(os.stat(self.temp_file).st_size), xml_tree[0].get('bytes'))
        
        # mtime
        current_time = int(time.time())
        res = self.ns.mtime(self.cpcode_path + self.temp_dir + "/" + self.temp_file , current_time)
        self.assertEqual(200, res.status_code)

        # stat
        res = self.ns.stat(self.cpcode_path + self.temp_dir + "/" + self.temp_file)
        self.assertEqual(200, res.status_code)
        xml_tree = ET.fromstring(res.text)
        self.assertEqual(str(current_time), xml_tree[0].get('mtime'))

        # symlink
        res = self.ns.symlink(self.cpcode_path + self.temp_dir + "/" + self.temp_file, self.cpcode_path + self.temp_dir + "/" + self.temp_file + "_lnk")
        self.assertEqual(200, res.status_code)

        # rename
        res = self.ns.rename(self.cpcode_path + self.temp_dir + "/" + self.temp_file, self.cpcode_path + self.temp_dir + "/" + self.temp_file + "_rename")
        self.assertEqual(200, res.status_code)

        # delete
        res = self.ns.delete(self.cpcode_path + self.temp_dir + "/" + self.temp_file + "_rename")
        self.assertEqual(200, res.status_code)
        res = self.ns.delete(self.cpcode_path + self.temp_dir + "/" + self.temp_file + "_lnk")
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
# upload -> download -> dir -> stat -> symlink -> mtime -> du -> rename
# delete -> rmdir