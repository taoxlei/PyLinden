#-*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
from __future__ import absolute_import
import __builtin__
from .processors import staticfileprocessor
from .processors import postprocessor
from .processors import photoprocessor
from .processors import commonpageprocessor
from . import logging

class PyLinden(object):
    option_defaults = {
        'deployment' : 'local', # 'local' or 'BAE'
        'source'     : 'site_source',
        'output'     : 'site_output',
    }
    
    def __init__(self, *args, **kwargs):
        # Loop through kwargs and assign defaults
        for option, default in self.option_defaults.items():
            setattr(self, option, kwargs.get(option, default))

        __builtin__.logger = logging.getLogger(self.deployment)

    def build_processors(self):
        self.processors = []
        self.processors.append(staticfileprocessor.StaticFileProcessor(self))
        self.processors.append(postprocessor.PostProcessor(self))
        self.processors.append(photoprocessor.PhotoProcessor(self))
        self.processors.append(commonpageprocessor.CommonPageProcessor(self))
    
    def generate(self):
        self.build_processors()
        for p in self.processors:
            p.run()
        print('everything is done!')
    
"""
EXPORTED FUNCTIONS
=============================================================================

the only one function we really mean to export: pylinden().
"""

def pylinden(*args, **kwargs):
    pl = PyLinden(*args, **kwargs)
    pl.generate()


