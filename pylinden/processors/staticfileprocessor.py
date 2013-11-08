#-*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
from __future__ import absolute_import

import os, codecs, re, yaml
from .. import util      

class StaticFileProcessor(object):
    def __init__(self, pylinden_instance):
        self.pi = pylinden_instance
            
    def run(self):
        for ld in os.listdir(self.pi.source):
            if (os.path.isdir(os.path.join(self.pi.source, ld))
                and not ld.startswith('_')
                and not ld.startswith('.')):
                for (path, dirs, files) in os.walk(os.path.join(self.pi.source, ld)):
                    for fn in files:
                        fullfn = os.path.join(path, fn)
                        util.smartwrite(
                            open(fullfn, 'rb').read(),
                            os.path.join(
                                self.pi.output, 
                                os.path.relpath(fullfn, start=self.pi.source)
                            )
                        )


