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


if __name__ == '__main__':
    action_list = '''\
         dir: to list the contents of the directory /123456
            dir /123456
         upload: to upload file.txt to /123456 directory
            upload file.txt /123456/ or
            upload file.txt /123456/file.txt
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
    usage = 'Usage: python cms_netstorage.py -H [hostname] -k [keyname] -K [key] -t [timeout] -s [use ssl] -a [action_options] ..'
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
    parser.add_option(
        '-s', '--ssl', dest='ssl')
    parser.add_option(
        '-t', '--timeout', dest='timeout')

    (options, args) = parser.parse_args()

    if options.hostname and options.keyname and options.key and options.action:
        ssl = options.ssl if hasattr(options, 'ssl') else False
        ns = Netstorage(options.hostname, options.keyname, options.key, ssl)

        def _arg(key, default=None):
            return args[key] if key in args else default

        try:
            res = None
            if options.action == 'delete':
                ok, res = ns.delete(args[0], _arg(1))
            elif options.action == 'dir':
                if len(args) >= 2:
                    ok, res = ns.dir(args[0], ast.literal_eval(args[1]), _arg(2))
                else:
                    ok, res = ns.dir(args[0])
            elif options.action == 'list':
                if len(args) >= 2:
                    ok, res = ns.list(args[0], ast.literal_eval(args[1]), _arg(2))
                else:
                    ok, res = ns.list(args[0])
            elif options.action == 'download':
                ok, res = ns.download(args[0], args[1], _arg(2))
            elif options.action == 'du':
                ok, res = ns.du(args[0], _arg(1))
            elif options.action == 'mkdir':
                ok, res = ns.mkdir(args[0], _arg(1))
            elif options.action == 'mtime':
                ok, res = ns.mtime(args[0], args[1], _arg(2))
            elif options.action == 'quick-delete':
                ok, res = ns.quick_delete(args[0], _arg(1))
            elif options.action == 'rmdir':
                ok, res = ns.rmdir(args[0], _arg(1))
            elif options.action == 'stat':
                ok, res = ns.stat(args[0], _arg(1))
            elif options.action == 'symlink':
                ok, res = ns.symlink(args[0], args[1], _arg(2))
            elif options.action == 'upload':
                if len(args) >= 3:
                    ok, res = ns.upload(args[0], args[1], args[2], _arg(3))
                else:
                    ok, res = ns.upload(args[0], args[1])
            elif options.action == 'rename':
                ok, res = ns.rename(args[0], args[1], _arg(1))
            else:
                print("Invalid action.\nUse option -h or --help")
                exit()
            
            print_result(res, options.action)
                
        except IndexError as e:
            if options.action == 'download' and args[0]:
                ok, res = ns.download(args[0], '', _arg(1))
                print_result(res, options.action)
            else:
                print("Invalid argument.\n")
                parser.print_help()
    else:
        print("You should input hostname, keyname, key and action.\n")
        parser.print_help()
