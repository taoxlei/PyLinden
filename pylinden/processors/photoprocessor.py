#-*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
from __future__ import absolute_import

import os, codecs, re, yaml
from . import Processor

class Photo(object):
    def __init__(self, path):
        self.path = path
        self.url = '/photos/foobar'

class PhotoProcessor(Processor):
    def __init__(self, pylinden_instance):
        self.pi = pylinden_instance

    def run(self):
        photos_dir = os.path.join(os.path.abspath(self.pi.source), '_photos')
        self.pi.photos = []
        for dirpath, dirnames, filenames in os.walk(photos_dir):
        	for fn in filenames:
        	    self.pi.photos.append(Photo(os.path.join(dirpath, fn)))