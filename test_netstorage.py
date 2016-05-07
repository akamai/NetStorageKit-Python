# -*- coding: utf-8 -*-

import unittest, uuid, os, time
import xml.etree.ElementTree as ET

from netstorageapi import Netstorage
from spike import secrets


YOUR_CPCODE = "360949"
YOUR_HOSTNAME = "astin-nsu.akamaihd.net"
YOUR_KEYNAME = "astinastin"
YOUR_KEY = secrets.key


class TestNetstorage(unittest.TestCase):
    
    def setUp(self):
        self.cpcode_path = YOUR_CPCODE
        self.temp_ns_dir = "/{}/{}".format(self.cpcode_path, str(uuid.uuid4()))
        self.temp_file = "{}.txt".format(str(uuid.uuid4()))
        self.temp_ns_file = "{}/{}".format(self.temp_ns_dir, self.temp_file)
        
        self.ns = Netstorage(YOUR_HOSTNAME, YOUR_KEYNAME, YOUR_KEY)
        
    def tearDown(self):
        # delete temp files for local
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
        ok, res = self.ns.dir("/" + self.cpcode_path)
        self.assertEqual(True, ok)
    
        # mkdir
        ok, res = self.ns.mkdir(self.temp_ns_dir)
        self.assertEqual(True, ok)

        # upload
        with open(self.temp_file, 'wt') as f:
            f.write("Hello, Netstorage API World!")
        ok, res = self.ns.upload(self.temp_file, self.temp_ns_file)
        self.assertEqual(True, ok)

        # du
        ok, res = self.ns.du(self.temp_ns_dir)
        self.assertEqual(True, ok)
        xml_tree = ET.fromstring(res.content)
        self.assertEqual(str(os.stat(self.temp_file).st_size), xml_tree[0].get('bytes'))
        
        # mtime
        current_time = int(time.time())
        ok, res = self.ns.mtime(self.temp_ns_file , current_time)
        self.assertEqual(True, ok)

        # stat
        ok, res = self.ns.stat(self.temp_ns_file)
        self.assertEqual(True, ok)
        xml_tree = ET.fromstring(res.text)
        self.assertEqual(str(current_time), xml_tree[0].get('mtime'))

        # symlink
        ok, res = self.ns.symlink(self.temp_ns_file, self.temp_ns_file + "_lnk")
        self.assertEqual(True, ok)

        # rename
        ok, res = self.ns.rename(self.temp_ns_file, self.temp_ns_file + "_rename")
        self.assertEqual(True, ok)
        
        # download
        ok, res = self.ns.download(self.temp_ns_file + "_rename")
        self.assertEqual(True, ok)

        # delete
        ok, res = self.ns.delete(self.temp_ns_file + "_rename")
        self.assertEqual(True, ok)
        ok, res = self.ns.delete(self.temp_ns_file + "_lnk")
        self.assertEqual(True, ok)

        # rmdir
        ok, res = self.ns.rmdir(self.temp_ns_dir)
        self.assertEqual(True, ok)


if __name__ == '__main__':
    unittest.main()