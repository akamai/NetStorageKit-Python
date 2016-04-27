import unittest, uuid, os, time
import xml.etree.ElementTree as ET

from akamai.netstorage import Netstorage
from spike import secrets


class TestNetstorage(unittest.TestCase):
    
    def setUp(self):
        self.cpcode_path = "360949"
        self.temp_ns_dir = "/{}/{}".format(self.cpcode_path, str(uuid.uuid4()))
        self.temp_file = "{}.txt".format(str(uuid.uuid4()))
        self.temp_ns_file = "{}/{}".format(self.temp_ns_dir, self.temp_file)
        
        self.ns = Netstorage("astin-nsu.akamaihd.net", "astinastin", secrets.key)
        
    def tearDown(self):
        # delete temp files from local
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
        
        if os.path.exists(self.temp_file + '_rename'):
            os.remove(self.temp_file + '_rename')
        
        # delete temp files for netstorage    
        self.ns.delete(self.temp_ns_file)
        self.ns.delete(self.temp_ns_file + '_lnk')
        self.ns.delete(self.temp_ns_file + '_rename')
        self.ns.rmdir(self.temp_ns_dir)
        
    def test_netstorage(self):
        # dir
        res = self.ns.dir("/" + self.cpcode_path)
        self.assertEqual(200, res.status_code)
    
        # mkdir
        res = self.ns.mkdir(self.temp_ns_dir)
        self.assertEqual(200, res.status_code)

        # upload
        with open(self.temp_file, 'wt') as f:
            print("Hello, Netstorage API World!", file=f)
        res = self.ns.upload(self.temp_file, self.temp_ns_file)
        self.assertEqual(200, res.status_code)

        # du
        res = self.ns.du(self.temp_ns_dir)
        self.assertEqual(200, res.status_code)
        xml_tree = ET.fromstring(res.content)
        self.assertEqual(str(os.stat(self.temp_file).st_size), xml_tree[0].get('bytes'))
        
        # mtime
        current_time = int(time.time())
        res = self.ns.mtime(self.temp_ns_file , current_time)
        self.assertEqual(200, res.status_code)

        # stat
        res = self.ns.stat(self.temp_ns_file)
        self.assertEqual(200, res.status_code)
        xml_tree = ET.fromstring(res.text)
        self.assertEqual(str(current_time), xml_tree[0].get('mtime'))

        # symlink
        res = self.ns.symlink(self.temp_ns_file, self.temp_ns_file + "_lnk")
        self.assertEqual(200, res.status_code)

        # rename
        res = self.ns.rename(self.temp_ns_file, self.temp_ns_file + "_rename")
        self.assertEqual(200, res.status_code)
        
        # download
        res = self.ns.download(self.temp_ns_file + "_rename")
        self.assertEqual(200, res.status_code)

        # delete
        res = self.ns.delete(self.temp_ns_file + "_rename")
        self.assertEqual(200, res.status_code)
        res = self.ns.delete(self.temp_ns_file + "_lnk")
        self.assertEqual(200, res.status_code)

        # rmdir
        res = self.ns.rmdir(self.temp_ns_dir)
        self.assertEqual(200, res.status_code)


if __name__ == '__main__':
    unittest.main()