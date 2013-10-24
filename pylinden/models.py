#-*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
from __future__ import absolute_import

import os, codecs, re, yaml
from .utils import logger
from .parser import Parser
from .utils import singleton
from .renderer import Renderer
from . import g, utils

parser = Parser()
renderer = Renderer()    

class Post(object):
    def __init__(self, path):
        self.path = path
        self.url = '/posts/' + os.path.splitext(os.path.basename(path))[0] + '.html'
        
        if not os.path.exists(path):
            logger.warning('not exists: ' + path)
        
        f = codecs.open(path, encoding='utf-8')
        try:
            self._text = f.read()
        except Exception as e:
            logger.error(e.message)
        finally:
            f.close()
        
        mdate = re.match('\d{4}\-\d{1,2}\-\d{1,2}', os.path.basename(path))
        mtext = re.search('---([\s\S]*?)---([\s\S]*)', self._text)
        try:
            self.date = mdate.group(0)
            head = mtext.group(1).strip()
            yhead = yaml.load(head)
            self.title = yhead.get('title', '')
            self.tags = yhead.get('tags', [])
            body = mtext.group(2).strip()
            self._content = body
        except:
            raise Exception('Bad Post: ' + path)
        
    def render(self):
        self.html = parser.parse(self._content)
        self.html = renderer.render('_post.html', site=Site(), post=self)
        return self.html
    
    def render_to(self, path):
        html = self.render()
        fw = codecs.open(path, 'w', 'utf_8_sig')
        try:
            fw.write(html)
        except Exception as e:
            logger.error(e.message)
        finally:
            fw.close()        

class Posts(object):
    def __init__(self):
        posts_dir = os.path.join(os.path.abspath(g.SOURCE), '_posts')
        self.posts = []
        for p in os.listdir(posts_dir):
            try:
                self.posts.append(Post(os.path.join(posts_dir, p)))
            except Exception as e:
                logger.warning(e.message)
        self.posts.sort(key = lambda one: one.date, reverse = True)
        
        # add 'newer' and 'older' attribute to each post object
        for i in range(len(self.posts)):
            self.posts[i].newer = self.posts[max(i-1,0)]
            self.posts[i].older = self.posts[min(i+1,len(self.posts)-1)]
            
    def __iter__(self):
        return iter(self.posts)
                
    def get_post(self, path):
        for p in self.posts:
            if p._path==path:
                return p
        raise Exception('Not Found: ' + path)

        
class Page(object):
    def __init__(self, path):
        self.path = path
        
    def render(self):
        self.html = renderer.render(os.path.basename(self.path), site=Site())
        return self.html
    
    def render_to(self, path):
        html = self.render()
        fw = codecs.open(path, 'w', 'utf_8_sig')
        try:
            fw.write(html)
        except Exception as e:
            logger.error(e.message)
        finally:
            fw.close()        

            
class Pages(object):
    def __init__(self):
        self.pages = []
        for fn in os.listdir(g.SOURCE):
            path = os.path.join(os.path.abspath(g.SOURCE), fn)
            if (os.path.isfile(path)
                and not fn.startswith('_')
                and not fn.startswith('.')):            
                self.pages.append(Page(path))
                
    def __iter__(self):
        return iter(self.pages)
    
    
class Tag(object):
    def __init__(self):
        self.name = ''
        self.posts = []
    def __str__(self):
        return self.name
    
    
class Tags(object):
    def __init__(self, posts):
        _tags_str = []
        _tags_posts = {}
        for p in posts:
            for t in p.tags:
                if t not in _tags_str:
                    _tags_str.append(t)
                    _tags_posts[t] = [p]
                else:
                    _tags_posts[t].append(p)
        self.tags = []
        for k, v in _tags_posts.iteritems():
            tag = Tag()
            tag.name = k
            tag.posts = v
            self.tags.append(tag)
            
    def __iter__(self):
        return iter(self.tags)
        
    
    
@singleton
class Site(object):
    '''This Singlenton Class contains everything for your site'''
    def __init__(self):
        self.posts = Posts()
        self.tags = Tags(self.posts)
        self.pages = Pages()