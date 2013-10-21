#-*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function

import os, json
import web
from bae.core.const import APP_DIR

# do this before import other pylinden stuff if your deployment is BAE
from pylinden import g
g.DEPLOYMENT = 'BAE'
g.SOURCE = os.path.join(APP_DIR, 'site_source')
g.OUTPUT = os.path.join(APP_DIR, 'site_output_bae')

from pylinden.generator import Generator
from pylinden.utils import logger

class DoHandler:
    def GET(self):
        cmd = web.input().cmd
            
        if cmd=='resetlogger':
            logger.logs = ['reseted.']
            return json.dumps(logger.logs)
        if cmd=='generate':
            try:
                gen = Generator()
                gen.generate()
            except Exception as e:
                logger.error(e.message + "Maybe, write too much (BAE NFS allows 50times/min)")
            logs = [log.replace(APP_DIR, '') for log in logger.logs]
            return json.dumps(logs)
        if cmd=='listoutput':
            ls = []
            for (path, dirs, files) in os.walk(g.OUTPUT):
                for f in files:
                    ls.append(os.path.relpath(os.path.join(path,f),start=g.OUTPUT))
            return json.dumps(ls)
        if cmd=='reset':
            try:
                gen = Generator()
                gen.reset()
            except Exception as e:
                logger.error("reset failed. ")
            return json.dumps(logger.logs)
        
        return 'nothing happened.'

 
urls = (
    '.*', 'DoHandler' 
)
 
app = web.application(urls, globals()).wsgifunc()
 
from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app)