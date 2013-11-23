#-*- coding:utf-8 -*-
"""
PyLinden
========

PyLinden is another static blog generator.

## Basic usage as a module:

    import pylinden
    pylinden.pylinden([deployment='local', # 'BAE': for Baidu App Engine
                       source='site_source',
                       output='site_output'])

See <http://pylinden.duapp.com> for more
information and instructions.(Chinese, 中文)

## Authors and License

Started by [Tao Xiaolei](http://taoxiaolei.cn/). 
Contact: lingyunyumo@gmail.com
Copyright 2013 Tao Xiaolei

License: MIT
"""

from __future__ import unicode_literals, print_function
from __future__ import absolute_import
import __builtin__

from . import logging
from . import preprocessors, mainprocessors, postprocessors

__all__ = ['pylinden',]

class PyLinden(object):
    """The root class for our static blog generator."""

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

    def buildprocessors(self):
        self.preprocessors = []
        self.preprocessors.append(preprocessors.StaticFilesProcessor(self))

        self.mainprocessors = []
        self.mainprocessors.append(mainprocessors.PostsProcessor(self))
        self.mainprocessors.append(mainprocessors.PhotosProcessor(self))
        
        self.postprocessors = []
        self.postprocessors.append(postprocessors.CommonPageProcessor(self))
    
    def generate(self):
        self.buildprocessors()
        for p in self.preprocessors:
            p.run()
        for p in self.mainprocessors:
            p.run()
        for p in self.postprocessors:
            p.run()
        print('everything is done!')
    
"""
EXPORTED FUNCTIONS
=============================================================================

the only one function we really mean to export: pylinden().
"""

def pylinden(*args, **kwargs):
    """
    pylinden.pylinden([deployment='local', # 'BAE': for Baidu App Engine
                       source='site_source',
                       output='site_output'])
    """
    
    pl = PyLinden(*args, **kwargs)
    pl.generate()


