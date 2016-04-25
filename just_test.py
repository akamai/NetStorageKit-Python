import unittest, uuid, os, time
import xml.etree.ElementTree as ET

from akamai.netstorage import Netstorage
from spike import secrets

cpcode_path = "/360949/1.png"

ns = Netstorage("astin-nsu.akamaihd.net", "astinastin", secrets.key)
ns.download(cpcode_path, '1.png')