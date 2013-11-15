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
            for (path, dirs, files) in os.walk(os.path.join(APP_DIR, 'site_output_bae')):
                for f in files:
                    ls.append(os.path.relpath(os.path.join(path,f),
                                              start=os.path.join(APP_DIR, 'site_output_bae')
                                              )
                              )
            return json.dumps(ls)
        
        return 'nothing happened.'

 
urls = (
    '.*', 'DoHandler' 
)
 
app = web.application(urls, globals()).wsgifunc()
 
from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app)
