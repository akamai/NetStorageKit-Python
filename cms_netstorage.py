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
#adding folderUpload support
import os
import ast
import optparse, sys
from akamai.netstorage import Netstorage

class NetstorageParser(optparse.OptionParser):
    def format_epilog(self, formatter):
        return self.epilog

def print_result(response, action):
    print("=== Request Header ===")
    print(response.request.headers)
    print("=== Response Code ===")
    print(response.status_code)
    print("=== Response Header ===")
    print(response.headers)
    if action != 'download':
        print("=== Response Content ===")
        print(response.text)

# Uploads a single file to NetStorage
def upload_file(ns, local_file, remote_file):
    print(f"Uploading {local_file} to {remote_file}")
    
    # If the upload method requires three arguments
    ok, res = ns.upload(local_file, remote_file)
    
    # Check if the upload was successful
    if ok:
        print(f"Upload successful: {local_file} -> {remote_file}")
    else:
        print(f"Upload failed: {local_file} -> {remote_file}")
    
    return ok, res

# Recursively upload directory contents
def upload_directory(ns, local_dir, remote_dir):
    for root, dirs, files in os.walk(local_dir):
        for file in files:
            local_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_file_path, local_dir)  # Preserve directory structure
            remote_file_path = os.path.join(remote_dir, relative_path).replace("\\", "/")  # Ensure remote path uses forward slashes
            ok, response = upload_file(ns, local_file_path, remote_file_path)
            print_result(response, 'upload')

if __name__ == '__main__':
    action_list = '''\
         dir: to list the contents of the directory /123456
            dir /123456
         upload: to upload file.txt or a folder to /123456 directory
            upload file.txt /123456/ or
            upload uploaddir /123456/uploaddir
         stat: to display status of /123456/file.txt
            stat /123456/file.txt
         du: to display disk usage on directory /123456
            du /123456
         download: To download /123456/file.txt
            download /123456/file.txt or
            download /123456/file.txt LOCAL_PATH
         mtime: to set the timestamp of /123456/file.txt to 1463042904 in epoch format)
            mtime /123456/file.txt 1463042904
         quick-delete: to delete /123456/dir1 recursively (quick-delete needs to be enabled on the CP Code):
            quick-delete /123456/dir1
         rename: to rename /123456/file.txt to /123456/newfile.txt
            rename /123456/file.txt /123456/newfile.txt
         symlink: to create a symlink /123456/file.txt_symlink pointing to /123456/file.txt
            symlink /123456/file.txt /123456/file.txt_symlink
         delete: to delete /123456/file.txt
            delete /123456/file.txt
         mkdir: to create /123456/dir1
            mkdir /123456/dir1
         rmdir: to delete /123456/dir1 (directory needs to be empty)
            rmdir /123456/dir1
'''
    usage = 'Usage: python cms_netstorage.py -H [hostname] -k [keyname] -K [key] -a [action_options] ..'
    parser = NetstorageParser(usage=usage, epilog=action_list)

    parser.add_option(
        '-H', '--host', dest='hostname',
        help='Netstorage API hostname ex) xxx-nsu.akamaihd.net')
    parser.add_option(
        '-k', '--keyname', dest='keyname',
        help='Netstorage API keyname ex) xxxxx')
    parser.add_option(
        '-K', '--key', dest='key',
        help='Netstorage API key ex) xxxxxxxxxxxxx')
    parser.add_option(
        '-a', '--action', dest='action')

    (options, args) = parser.parse_args()

    if options.hostname and options.keyname and options.key and options.action:
        ns = Netstorage(options.hostname, options.keyname, options.key)

        try:
            skipFinalLog = False
            res = None
            if options.action == 'delete':
                ok, res = ns.delete(args[0])
            elif options.action == 'dir':
                if len(args) >= 2:
                    ok, res = ns.dir(args[0], ast.literal_eval(args[1]))
                else:
                    ok, res = ns.dir(args[0])
            elif options.action == 'list':
                if len(args) >= 2:
                    ok, res = ns.list(args[0], ast.literal_eval(args[1]))
                else:
                    ok, res = ns.list(args[0])
            elif options.action == 'download':
                ok, res = ns.download(args[0], args[1])
            elif options.action == 'du':
                ok, res = ns.du(args[0])
            elif options.action == 'mkdir':
                ok, res = ns.mkdir(args[0])
            elif options.action == 'mtime':
                ok, res = ns.mtime(args[0], args[1])
            elif options.action == 'quick-delete':
                ok, res = ns.quick_delete(args[0])
            elif options.action == 'rmdir':
                ok, res = ns.rmdir(args[0])
            elif options.action == 'stat':
                ok, res = ns.stat(args[0])
            elif options.action == 'symlink':
                ok, res = ns.symlink(args[0], args[1])
            elif options.action == 'upload':
                local_path = args[0]
                remote_path = args[1]

                if os.path.isdir(local_path):
                    # Upload directory recursively
                    skipFinalLog = True
                    upload_directory(ns, local_path, remote_path)
                elif os.path.isfile(local_path):
                    # Upload single file
                    ok, res = upload_file(ns, local_path, remote_path)
                    
                else:
                    print(f"Invalid path: {local_path}. Must be a file or directory.")
            elif options.action == 'rename':
                ok, res = ns.rename(args[0], args[1])
            else:
                print("Invalid action.\nUse option -h or --help")
                exit()
            if not skipFinalLog:
                print_result(res, options.action)

        except IndexError as e:
            if options.action == 'download' and args[0]:
                ok, res = ns.download(args[0])
                print_result(res, options.action)
            else:
                print("Invalid argument.\n")
                parser.print_help()
    else:
        print("You should input hostname, keyname, key and action.\n")
        parser.print_help()
