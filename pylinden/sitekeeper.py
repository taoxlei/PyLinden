#-*- coding:utf-8 -*-

'''
this module manages files status in your SOURCE
'''

from __future__ import unicode_literals, print_function
from __future__ import absolute_import

import os, json, codecs, md5
from . import g
from .utils import logger
from .utils import singleton


@singleton
class SiteKeeper(object):
    def __init__(self):
        self.source = os.path.abspath(g.SOURCE)
        self.output = os.path.abspath(g.OUTPUT)
        self.file_path = os.path.join(self.source, '_misc', 'md5_records.json')
        if os.path.exists(self.file_path):
            self.records = json.loads(open(self.file_path).read())
        else:
            self.records = {}
            self.save_records()
            
        #for k, v in self.records.iteritems():
        #    print("%s%s: %s" % (' '*(100-len(k)-len(v)),k,v))
        
    def save_records(self):
        f = codecs.open(self.file_path, 'w', encoding='utf-8')
        try:
            text = json.dumps(self.records, ensure_ascii=False, indent=4)
            f.write(text)
        except Exception as e:
            logger.error(e.message)
        finally:
            f.close()
            
    def load_records(self):
        self.records = json.loads(open(self.file_path).read())
        
    def reset_records(self):
        try:
            os.remove(self.file_path)
        except:
            raise 'reset records failed.'
        
    def get_md5(self, path):
        with open(path) as fr:
            md5hex = md5.new(fr.read()).hexdigest()
        return md5hex
    
    def create_records(self):
        self.records = {}
        for (path, dirs, files) in os.walk(self.source):
            for f in files:
                absp = os.path.join(path, f)
                relp = os.path.normpath(os.path.relpath(absp, start=self.source))
                self.records[relp] = self.get_md5(absp)
    
    def shouldupdate(self, path):
        '''"should update": new created, modified, not generated'''
        relpath = os.path.relpath(path, start=self.source)

        md5history = self.records.get(relpath, '')
        md5file = self.get_md5(path)
        
        if not md5history: # there's no histroy
            return True   # not generated (new created, not generated)
        
        if not md5history==md5file: # modified
            return True
        
        return False
    
    def update(self, path):
        md5record = self.get_md5(path)
        relpath = os.path.relpath(path, start=self.source)
        self.records[relpath] = md5record

