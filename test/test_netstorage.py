# -*- coding: utf-8 -*-

# Original author: Astin Choi <achoi@akamai.com>

# Copyright 2016 Akamai Technologies http://developer.akamai.com.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import sys
import time
import unittest
import uuid
import xml.etree.ElementTree as ET

sys.path.append("akamai/netstorage"); sys.path.append("../akamai/netstorage")
from netstorage import Netstorage, NetstorageError

if os.environ.get('TEST_MODE') == 'TRAVIS':
    NS_HOSTNAME = os.environ['NS_HOSTNAME']
    NS_KEYNAME = os.environ['NS_KEYNAME']
    NS_KEY = os.environ['NS_KEY']
    NS_CPCODE = os.environ['NS_CPCODE']
else:
    import secret
    NS_HOSTNAME = secret.NS_HOSTNAME
    NS_KEYNAME = secret.NS_KEYNAME
    NS_KEY = secret.NS_KEY
    NS_CPCODE = secret.NS_CPCODE


class TestNetstorage(unittest.TestCase):
    
    def setUp(self):
        self.cpcode_path = NS_CPCODE
        self.temp_ns_dir = "/{0}/{1}".format(self.cpcode_path, str(uuid.uuid4()))
        self.temp_file = "{0}.txt".format(str(uuid.uuid4()))
        self.temp_ns_file = "{0}/{1}".format(self.temp_ns_dir, self.temp_file)
        self.temp_ns_stream_file = "{0}/stream_{1}".format(self.temp_ns_dir, self.temp_file)
        
        self.ns = Netstorage(NS_HOSTNAME, NS_KEYNAME, NS_KEY)
        
    def tearDown(self):
        # delete temp files for local
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
            print("[TEARDOWN] remove {0} from local done".format(self.temp_file))
        
        if os.path.exists(self.temp_file + '_rename'):
            os.remove(self.temp_file + '_rename')
            print("[TEARDOWN] remove {0} from local done".format(self.temp_file + '_rename'))
        
        # delete temp files for netstorage    
        ok, _ = self.ns.delete(self.temp_ns_file)
        if ok:
            print("[TEARDOWN] delete {0} done".format(self.temp_ns_file))    
        ok, _ = self.ns.delete(self.temp_ns_file + '_lnk')
        if ok:
            print("[TEARDOWN] delete {0} done".format(self.temp_ns_file + '_lnk'))
        ok, _ = self.ns.delete(self.temp_ns_file + '_rename')
        if ok:
            print("[TEARDOWN] delete {0} done".format(self.temp_ns_file + '_rename'))
        ok, _ = self.ns.rmdir(self.temp_ns_dir)
        if ok:
            print("[TEARDOWN] rmdir {0} done".format(self.temp_ns_dir))
        
    def test_netstorage(self):
        # dir
        ok, _ = self.ns.dir("/" + self.cpcode_path)
        self.assertEqual(True, ok, "dir fail.")
        print("[TEST] dir {0} done".format("/" + self.cpcode_path))

        # mkdir
        ok, _ = self.ns.mkdir(self.temp_ns_dir)
        self.assertEqual(True, ok, "mkdir fail.")
        print("[TEST] mkdir {0} done".format(self.temp_ns_dir))

        # upload
        with open(self.temp_file, 'wt') as f:
            f.write("Hello, Netstorage API World!")
        ok, res = self.ns.upload(self.temp_file, self.temp_ns_file)
        self.assertEqual(True, ok, "upload fail.")
        print("[TEST] upload {0} to {1} done".format(self.temp_file, self.temp_ns_file))

        # stream_upload
        stream_upload_text = 'Stream Upload!'
        ok, res = self.ns.stream_upload(stream_upload_text, self.temp_ns_stream_file)
        self.assertEqual(True, ok, "stream upload fail")
        print("[TEST] stream_upload {0} done".format(self.temp_ns_stream_file))
        
        # stream_download
        ok, res = self.ns.stream_download(self.temp_ns_stream_file)
        self.assertEqual(True, ok, "stream download fail")
        self.assertEqual(stream_upload_text, res.text, "stream download fail")
        print("[TEST] stream_download {0} done".format(self.temp_ns_stream_file))

        # du
        ok, res = self.ns.du(self.temp_ns_dir)
        self.assertEqual(True, ok)
        # xml_tree = ET.fromstring(res.text)
        # self.assertEqual(str(os.stat(self.temp_file).st_size), xml_tree[0].get('bytes'), "du fail.")
        print("[TEST] du done")

        # mtime
        current_time = int(time.time())
        ok, _ = self.ns.mtime(self.temp_ns_file, current_time)
        self.assertEqual(True, ok, "mtime fail.")
        print("[TEST] mtime {0} to {1} done".format(self.temp_ns_file, current_time))

        # stat
        ok, res = self.ns.stat(self.temp_ns_file)
        self.assertEqual(True, ok, "stat fail.")
        xml_tree = ET.fromstring(res.text)
        self.assertEqual(str(current_time), xml_tree[0].get('mtime'))
        print("[TEST] stat done")

        # symlink
        ok, _ = self.ns.symlink(self.temp_ns_file, self.temp_ns_file + "_lnk")
        self.assertEqual(True, ok, "symlink fail.")
        print("[TEST] symlink {0} to {1} done".format(self.temp_ns_file, self.temp_ns_file + "_lnk"))

        # rename
        ok, _ = self.ns.rename(self.temp_ns_file, self.temp_ns_file + "_rename")
        self.assertEqual(True, ok, "rename fail.")
        print("[TEST] rename {0} to {1} done".format(self.temp_ns_file, self.temp_ns_file + "_rename"))
        
        # download
        ok, _ = self.ns.download(self.temp_ns_file + "_rename")
        self.assertEqual(True, ok, "download fail.")
        print("[TEST] download {0} done".format(self.temp_ns_file + "_rename"))

        # delete
        ok, _ = self.ns.delete(self.temp_ns_stream_file)
        self.assertEqual(True, ok, "delete fail.")
        print("[TEST] delete {0} done".format(self.temp_ns_stream_file))
        ok, _ = self.ns.delete(self.temp_ns_file + "_rename")
        self.assertEqual(True, ok, "delete fail.")
        print("[TEST] delete {0} done".format(self.temp_ns_file + "_rename"))
        ok, _ = self.ns.delete(self.temp_ns_file + "_lnk")
        self.assertEqual(True, ok, "delete fail.")
        print("[TEST] delete {0} done".format(self.temp_ns_file + "_lnk"))

        # rmdir
        ok, _ = self.ns.rmdir(self.temp_ns_dir)
        self.assertEqual(True, ok, "rmdir fail.")
        print("[TEST] rmdir {0} done".format(self.temp_ns_dir))

    def test_netstorage_exception(self):
        print(os.linesep)
        if not (sys.version_info[0] == 2 and sys.version_info[1] <= 6):
            with self.assertRaises(NetstorageError):
                self.ns.dir("Invalid ns path")
            print("[TEST] Invalid ns path NetstorageError test done")

            with self.assertRaises(NetstorageError):
                self.ns.upload("Invalid local path", self.temp_ns_file)
            print("[TEST] Invalid local path NetstorageError test done")

            with self.assertRaises(NetstorageError):
                self.ns.download("/123456/directory/", self.temp_file)
            print("[TEST] Download directory path NetstorageError test done")


if __name__ == '__main__':
    unittest.main()