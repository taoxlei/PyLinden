#-*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function

import os, json
import web
from bae.core.const import APP_DIR
import pylinden

class DoHandler:
    def GET(self):
        cmd = web.input().cmd
        if cmd=='hello':
            return 'hello world!'
        if cmd=='pylinden':
            try:
                pylinden.pylinden(
                    deployment='BAE',
                    source=os.path.join(APP_DIR, 'site_source'),
                    output=os.path.join(APP_DIR, 'site_output_bae')
                    )
                return 'OK'
            except Exception as e:
                return e.message
        if cmd=='resetlogger':
            pass
        if cmd=='generate':
            try:
                pylinden.pylinden(
                    deployment='BAE',
                    source=os.path.join(APP_DIR, 'site_source'),
                    output=os.path.join(APP_DIR, 'site_output_bae')
                    )
                return 'OK'
            except Exception as e:
                return e.message
        if cmd=='listoutput':
            ls = []
            for (path, dirs, files) in os.walk(g.OUTPUT):
                for f in files:
                    ls.append(os.path.relpath(os.path.join(path,f),start=g.OUTPUT))
            return json.dumps(ls)
        if cmd=='reset':
            #try:
            #    gen = Generator()
            #    gen.reset()
            #except Exception as e:
            #    logger.error("reset failed. ")
            #return json.dumps(logger.logs)
            return 'not imp'
        
        return 'nothing happened.'

 
urls = (
    '.*', 'DoHandler' 
)
 
app = web.application(urls, globals()).wsgifunc()
 
from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app)
