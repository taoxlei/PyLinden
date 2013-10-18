#-*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
from __future__ import absolute_import

import os, json, codecs, fnmatch, md5
from . import g
from datetime import datetime


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

class SimpleLogger(object):
    def __init__(self):
        self.logs = ['init: ' + str(datetime.now()) + ' - logger init.']
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

            
def singleton(cls):
    '''decorator for Singleton Pattern'''
    instances = {}
    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return get_instance