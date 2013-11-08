#-*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
from __future__ import absolute_import

import os, codecs, re, yaml
from jinja2 import Environment, FileSystemLoader, TemplateNotFound, Template
from .. import util      

class Page(object):
    def __init__(self, path):
        self.path = path

class CommonPageProcessor(object):
    def __init__(self, pylinden_instance):
        self.pi = pylinden_instance
        self.env = Environment(
            loader=FileSystemLoader(os.path.abspath(self.pi.source))
        )
          
    def run(self):
        self.pi.pages = []
        for fn in os.listdir(self.pi.source):
            path = os.path.join(os.path.abspath(self.pi.source), fn)
            if (os.path.isfile(path)
                and not fn.startswith('_')
                and not fn.startswith('.')):            
                self.pi.pages.append(Page(path))

        for page in self.pi.pages:
            dest = os.path.join(
                self.pi.output,
                os.path.basename(page.path)
            )
            try:
                temp = self.env.get_template(os.path.basename(page.path))
                data = temp.render(site=self.pi).encode('utf-8')
            except Exception as e:
                self.pi.logger.error(e.message)
            util.smartwrite(data, dest)
