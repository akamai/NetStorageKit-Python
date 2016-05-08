# -*- coding: utf-8 -*-

import unittest, uuid, os, time
import xml.etree.ElementTree as ET

from netstorageapi import Netstorage


NS_HOSTNAME = "astin-nsu.akamaihd.net"
NS_KEYNAME = "astinastin"
from spike import secrets 
NS_KEY = secrets.key # DO NOT EXPOSE IT
NS_CPCODE = "360949"

class TestNetstorage(unittest.TestCase):
    
    def setUp(self):
        self.cpcode_path = NS_CPCODE
        self.temp_ns_dir = "/{}/{}".format(self.cpcode_path, str(uuid.uuid4()))
        self.temp_file = "{}.txt".format(str(uuid.uuid4()))
        self.temp_ns_file = "{}/{}".format(self.temp_ns_dir, self.temp_file)
        
        self.ns = Netstorage(NS_HOSTNAME, NS_KEYNAME, NS_KEY)
        
    def tearDown(self):
        # delete temp files for local
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
            print("[TEARDOWN] remove {} from local done".format(self.temp_file))
        
        if os.path.exists(self.temp_file + '_rename'):
            os.remove(self.temp_file + '_rename')
            print("[TEARDOWN] remove {} from local done".format(self.temp_file + '_rename'))
        
        # delete temp files for netstorage    
        ok, _ = self.ns.delete(self.temp_ns_file)
        if ok:
            print("[TEARDOWN] delete {} done".format(self.temp_ns_file))    
        ok, _ = self.ns.delete(self.temp_ns_file + '_lnk')
        if ok:
            print("[TEARDOWN] delete {} done".format(self.temp_ns_file + '_lnk'))
        ok, _ = self.ns.delete(self.temp_ns_file + '_rename')
        if ok:
            print("[TEARDOWN] delete {} done".format(self.temp_ns_file + '_rename'))
        ok, _ = self.ns.rmdir(self.temp_ns_dir)
        if ok:
            print("[TEARDOWN] rmdir {} done".format(self.temp_ns_dir))
        
    def test_netstorage(self):
        # dir
        ok, res = self.ns.dir("/" + self.cpcode_path)
        self.assertEqual(True, ok, "dir fail.")
        print("[TEST] dir {} done".format("/" + self.cpcode_path))

        # mkdir
        ok, res = self.ns.mkdir(self.temp_ns_dir)
        self.assertEqual(True, ok, "mkdir fail.")
        print("[TEST] mkdir {} done".format(self.temp_ns_dir))

        # upload
        with open(self.temp_file, 'wt') as f:
            f.write("Hello, Netstorage API World!")
        ok, res = self.ns.upload(self.temp_file, self.temp_ns_file)
        self.assertEqual(True, ok, "upload fail.")
        print("[TEST] upload {} to {} done".format(self.temp_file, self.temp_ns_file))

        # du
        ok, res = self.ns.du(self.temp_ns_dir)
        self.assertEqual(True, ok)
        xml_tree = ET.fromstring(res.content)
        self.assertEqual(str(os.stat(self.temp_file).st_size), xml_tree[0].get('bytes'), "du fail.")
        print("[TEST] du done")

        # mtime
        current_time = int(time.time())
        ok, res = self.ns.mtime(self.temp_ns_file, current_time)
        self.assertEqual(True, ok, "mtime fail.")
        print("[TEST] mtime {} to {} done".format(self.temp_ns_file, current_time))

        # stat
        ok, res = self.ns.stat(self.temp_ns_file)
        self.assertEqual(True, ok, "stat fail.")
        xml_tree = ET.fromstring(res.text)
        self.assertEqual(str(current_time), xml_tree[0].get('mtime'))
        print("[TEST] stat done")

        # symlink
        ok, res = self.ns.symlink(self.temp_ns_file, self.temp_ns_file + "_lnk")
        self.assertEqual(True, ok, "symlink fail.")
        print("[TEST] symlink {} to {} done".format(self.temp_ns_file, self.temp_ns_file + "_lnk"))

        # rename
        ok, res = self.ns.rename(self.temp_ns_file, self.temp_ns_file + "_rename")
        self.assertEqual(True, ok, "rename fail.")
        print("[TEST] rename {} to {} done".format(self.temp_ns_file, self.temp_ns_file + "_rename"))
        
        # download
        ok, res = self.ns.download(self.temp_ns_file + "_rename")
        self.assertEqual(True, ok, "download fail.")
        print("[TEST] download {} done".format(self.temp_ns_file + "_rename"))

        # delete
        ok, res = self.ns.delete(self.temp_ns_file + "_rename")
        self.assertEqual(True, ok, "delete fail.")
        print("[TEST] delete {} done".format(self.temp_ns_file + "_rename"))
        ok, res = self.ns.delete(self.temp_ns_file + "_lnk")
        self.assertEqual(True, ok, "delete fail.")
        print("[TEST] delete {} done".format(self.temp_ns_file + "_lnk"))

        # rmdir
        ok, res = self.ns.rmdir(self.temp_ns_dir)
        self.assertEqual(True, ok, "rmdir fail.")
        print("[TEST] rmdir {} done".format(self.temp_ns_dir))

if __name__ == '__main__':
    unittest.main()