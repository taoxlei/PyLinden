#-*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
from __future__ import absolute_import

class Processor(object):
    def __init__(self, pylinden_instance=None):
        if pylinden_instance:
            self.pylinden_instance = pylinden_instance

    def run(self):
        pass
