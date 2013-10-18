#-*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
from __future__ import absolute_import

import os, shutil
from .models import Site
from .sitekeeper import SiteKeeper
from .utils import logger
from . import g, utils

site = Site()
sitekeeper = SiteKeeper()

class Generator(object):
    def __init__(self):
        self.source = os.path.abspath(g.SOURCE)
        self.output = os.path.abspath(g.OUTPUT)
        if not os.path.exists(self.output):
            os.mkdir(self.output)
        if not os.path.exists(os.path.join(self.output, 'posts')):
            os.mkdir(os.path.join(self.output, 'posts'))
                              
    def _copy_static(self):
        def copy_file(source, target):
            if not os.path.exists(os.path.dirname(target)):
                os.makedirs(os.path.dirname(target))
            open(target, "wb").write(open(source, "rb").read())
        
        for ld in os.listdir(self.source):
            if (os.path.isdir(os.path.join(self.source, ld))
                and not ld.startswith('_')
                and not ld.startswith('.')):
                for (path, dirs, files) in os.walk(os.path.join(self.source, ld)):
                    for fn in files:
                        fullfn = os.path.join(path, fn)
                        if sitekeeper.shouldupdate(fullfn):
                            copy_file(
                                fullfn, 
                                os.path.join(
                                    self.output, 
                                    os.path.relpath(fullfn, start=self.source)
                                )
                            )
                            logger.info('File Copied: %s' % fullfn)
                            sitekeeper.update(fullfn)
                            
                            
    def _generate_pages(self):
        for page in site.pages:
            if (sitekeeper.shouldupdate(os.path.join(self.source, '_base.html'))
                or sitekeeper.shouldupdate(page.path)):
                dest = os.path.join(
                    os.path.abspath(g.OUTPUT), 
                    os.path.basename(page.path)
                )
                page.render_to(dest)
                logger.info('Page generated: %s' % page.path)
                sitekeeper.update(page.path)
        
    def _generate_posts(self):
        for post in site.posts:
            if (sitekeeper.shouldupdate(os.path.join(self.source, '_base.html'))
                or sitekeeper.shouldupdate(os.path.join(self.source, '_post.html'))
                or sitekeeper.shouldupdate(post.path)):
                dest = os.path.join(
                    os.path.abspath(g.OUTPUT), 
                    'posts', 
                    os.path.basename(post.url)
                )
                post.render_to(dest)
                logger.info('Post generated: %s' % post.path)
                sitekeeper.update(post.path)

        
    def generate(self):
        # output your site
        self._copy_static()
        self._generate_pages()
        self._generate_posts()
        
        sitekeeper.update(os.path.join(self.source, '_base.html'))
        sitekeeper.update(os.path.join(self.source, '_post.html'))
        
        # do NOT forget save the history, inscremental generation depends on this
        sitekeeper.save_records()
        
    def reset(self):
        sitekeeper.reset_records()
        for (path, dirs, files) in os.walk(self.output):
            for fn in files:
                os.remove(os.path.join(path, fn))
        #try:
        #    shutil.rmtree(self.output)
        #except:
        #    logger.error('Remove %s failed.' % self.output)
        
        logger.info('Generator.reset() finished.')