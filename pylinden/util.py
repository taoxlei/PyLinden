#-*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
from __future__ import absolute_import

import os, json, codecs, fnmatch, md5
from datetime import datetime

def smartwrite(data, target):
    if not os.path.exists(target):
        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target))
        open(target, 'wb').write(data)
        logger.info('File is writen: ' + target)
    else:
        oldmd5 = md5.new(open(target, 'rb').read()).hexdigest()
        newmd5 = md5.new(data).hexdigest()
        if oldmd5 != newmd5:
            codecs.open(target, 'wb').write(data)
            logger.info('File is writen: ' + target)


