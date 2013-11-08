#-*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
from __future__ import absolute_import
from .processors import staticfileprocessor
from .processors import postprocessor
from .processors import commonpageprocessor
from . import util

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

        if self.deployment == 'local':
            self.logger = util.getbuiltinlogger()
        elif self.deployment == 'BAE':
            self.logger = util.getcustomlogger()

    def build_processors(self):
        self.processors = {}
        self.processors['staticfileprocessor'] = staticfileprocessor.StaticFileProcessor(self)
        self.processors['postprocessor'] = postprocessor.PostProcessor(self)
        self.processors['commonpageprocessor'] = commonpageprocessor.CommonPageProcessor(self)
    
    def generate(self):
        self.build_processors()
        for p in self.processors.values():
            p.run()
        print('gened')
    
"""
EXPORTED FUNCTIONS
=============================================================================

the only one function we really mean to export: pylinden().
"""

def pylinden(*args, **kwargs):
    pl = PyLinden(*args, **kwargs)
    pl.generate()


