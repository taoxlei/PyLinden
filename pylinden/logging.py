#-*- coding:utf-8 -*-
"""
A wrapper for the builtin Python module 'logging'.

    logging.getLogger(deployment='local')
    
return a original Python logger.

    logging.getLogger(deployment='BAE')
    
return a simple logger for BAE(Baidu App Engine), because
BAE restricted the original Python logging module.
"""

from __future__ import unicode_literals, print_function
from __future__ import absolute_import

import os, json, codecs, fnmatch, md5
from datetime import datetime
import logging

def singleton(cls):
    '''decorator for Singleton Pattern'''
    instances = {}
    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return get_instance

@singleton
class SimpleLogger(object):
    """A simple logger."""
    
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


def getLogger(deployment='local'): # 'local' or 'BAE'
    """
    Get a logger object.

    Keyword arguments:

    * deployment: A string of deployment type.
                  'local' or 'BAE', default is 'local'.

    """
    if deployment=='local':
        logging.getLogger().setLevel(logging.NOTSET)
        logger = logging.getLogger('pylinden')
        logger.setLevel(logging.NOTSET)
        fmt = logging.Formatter('%(levelname)s: %(filename)s(%(lineno)d) - %(message)s')
        sh = logging.StreamHandler()
        sh.setLevel(logging.NOTSET)
        sh.setFormatter(fmt)
        logger.addHandler(sh)
        return logger
    if deployment=='BAE':
        logger = SimpleLogger()
        return logger




