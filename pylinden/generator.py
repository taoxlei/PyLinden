#-*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
from __future__ import absolute_import

import os, shutil, md5
from .models import Site
from .utils import logger
from . import g, utils

site = Site()

class Generator(object):
    def __init__(self):
        self.source = os.path.abspath(g.SOURCE)
        self.output = os.path.abspath(g.OUTPUT)
        if not os.path.exists(self.output):
            os.mkdir(self.output)
        if not os.path.exists(os.path.join(self.output, 'posts')):
            os.mkdir(os.path.join(self.output, 'posts'))
                              
    def _copy_static(self):
        for ld in os.listdir(self.source):
            if (os.path.isdir(os.path.join(self.source, ld))
                and not ld.startswith('_')
                and not ld.startswith('.')):
                for (path, dirs, files) in os.walk(os.path.join(self.source, ld)):
                    for fn in files:
                        fullfn = os.path.join(path, fn)
                        utils.smartwrite(
                            open(fullfn, 'rb').read(),
                            os.path.join(
                                self.output, 
                                os.path.relpath(fullfn, start=self.source)
                            )
                        )
                            
    def _generate_gallery(self):
        for (path, dirs, files) in os.walk(os.path.join(self.source, '_gallery')):
            for fn in files:
                if fn.endswith('.jpg'):
                    fullfn = os.path.join(path, fn)
                    utils.smartwrite(
                        open(fullfn, 'rb').read(),
                        os.path.join(
                            self.output, 
                            os.path.relpath(fullfn, start=self.source)
                        ).replace('_gallery', 'gallery')
                    )
        
    def _generate_pages(self):
        for page in site.pages:
            dest = os.path.join(
                self.output,
                os.path.basename(page.path)
            )
            data = page.render().encode('utf-8')
            utils.smartwrite(data, dest)
        
    def _generate_posts(self):
        for post in site.posts:
            dest = os.path.join(
                self.output,
                'posts', 
                os.path.basename(post.url)
            )
            data = post.render().encode('utf-8')
            utils.smartwrite(data, dest)
        
    def generate(self):
        self._copy_static()
        self._generate_gallery()
        self._generate_pages()
        self._generate_posts()
        
        
    def reset(self):
        for (path, dirs, files) in os.walk(self.output):
            for fn in files:
                os.remove(os.path.join(path, fn))
                
        #try:
        #    shutil.rmtree(self.output)
        #except:
        #    logger.error('Remove %s failed.' % self.output)
        
        logger.info('Generator.reset() finished.')