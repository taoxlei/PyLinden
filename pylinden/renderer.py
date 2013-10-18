#-*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
from __future__ import absolute_import

import os
from jinja2 import Environment, FileSystemLoader, TemplateNotFound, Template
from .utils import logger
from . import g

class Renderer(object):
    def __init__(self):
        self.env = Environment(
            loader=FileSystemLoader(os.path.abspath(g.SOURCE))
        )

    def render(self, template, *args, **kwargs):
        try:
            return self.env.get_template(template).render(*args, **kwargs)
        except TemplateNotFound as e:
            logger.warning(e.message)      


    
