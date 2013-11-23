#-*- coding:utf-8 -*-
"""
As you guess, utils module contains some useful tools.
"""

from __future__ import unicode_literals, print_function
from __future__ import absolute_import

import os, codecs, md5

def smartwrite(data, target):
    """A smart writer. 
    Not going to write if data is equal to target's data. Create folder 
    if target's path is not existed. """
    
    if not os.path.exists(target):
        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target))
        open(target, 'wb').write(data)
        logger.info('Writen: ' + target)
    else:
        oldmd5 = md5.new(open(target, 'rb').read()).hexdigest()
        newmd5 = md5.new(data).hexdigest()
        if oldmd5 != newmd5:
            codecs.open(target, 'wb').write(data)
            logger.info('Writen: ' + target)


