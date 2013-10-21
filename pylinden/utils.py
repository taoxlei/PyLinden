#-*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
from __future__ import absolute_import

import os, json, codecs, fnmatch, md5
from datetime import datetime
from . import g

def singleton(cls):
    '''decorator for Singleton Pattern'''
    instances = {}
    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return get_instance

if g.DEPLOYMENT=='local':
    import logging
    logging.getLogger().setLevel(logging.NOTSET)
    logger = logging.getLogger('pylinden')
    logger.setLevel(logging.NOTSET)
    fmt = logging.Formatter('%(levelname)s: %(filename)s(%(lineno)d) - %(message)s')
    sh = logging.StreamHandler()
    sh.setLevel(logging.NOTSET)
    sh.setFormatter(fmt)
    logger.addHandler(sh)

@singleton
class SimpleLogger(object):
    def __init__(self):
        self.logs = ['###: ' + str(datetime.now()) + ' - logger initilized.###']
    def debug(self, msg):
        self.logs.append('debug: ' + str(datetime.now()) + ' - ' + msg)
    def info(self, msg):
        self.logs.append('info: ' + str(datetime.now()) + ' - ' + msg)
    def warning(self, msg):
        self.logs.append('warning: ' + str(datetime.now()) + ' - ' + msg)        
    def error(self, msg):
        self.logs.append('error: ' + str(datetime.now()) + ' - ' + msg)
    def critical(self, msg):
        self.logs.append('critical: ' + str(datetime.now()) + ' - ' + msg)
        
if g.DEPLOYMENT=='BAE':
    logger = SimpleLogger()


def smartwrite(data, target):
    if not os.path.exists(target):
        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target))
        open(target, 'wb').write(data)
        logger.info('File writen: %s' % target)
    else:
        oldmd5 = md5.new(open(target, 'rb').read()).hexdigest()
        newmd5 = md5.new(data).hexdigest()
        if oldmd5 != newmd5:
            codecs.open(target, 'wb').write(data)
            logger.info('File writen: %s' % target)

