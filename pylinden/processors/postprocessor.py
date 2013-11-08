#-*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
from __future__ import absolute_import

import os, codecs, re, yaml
from markdown import Markdown
from markdown.preprocessors import Preprocessor
from jinja2 import Environment, FileSystemLoader, TemplateNotFound, Template
from . import Processor
from .. import util

class HighlightPreprocessor(Preprocessor):
    def run(self, lines):
        new_lines = []
        # {% highlight 'html' %} someting {% endhighlight %}
        isInner = False
        for line in lines:
            mhead = re.match('^{%[ ]*highlight(.*)%}', line)
            mtail = re.match('^{%[ ]*endhighlight([ ]*)%}', line)
            if mhead:
                isInner = True
                new_lines.append("    :::" + mhead.group(1).strip())
                continue
            if mtail:
                new_lines.append("    ")
                isInner = False
                continue
            if isInner:
                new_lines.append('    ' + line)
            else:
                new_lines.append(line)
        return new_lines

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
        
    def render(self, pylinden_instance):
        self.pi = pylinden_instance
        
        md = Markdown(extensions=['codehilite(noclasses=True)'])
        md.preprocessors.insert(0, 'HighlightPreprocessor', HighlightPreprocessor())
        self.html = md.convert(self._content)

        self.env = Environment(
            loader=FileSystemLoader(os.path.abspath(self.pi.source))
        )
        try:
            temp = self.env.get_template('_post.html')
            self.html = temp.render(site=self.pi, post=self)
        except Exception as e:
            self.pi.logger.error(e.message)
        
        return self.html     

class PostProcessor(Processor):
    def __init__(self, pylinden_instance):
        self.pi = pylinden_instance

    def run(self):
        posts_dir = os.path.join(os.path.abspath(self.pi.source), '_posts')
        self.pi.posts = []
        for p in os.listdir(posts_dir):
            try:
                self.pi.posts.append(Post(os.path.join(posts_dir, p)))
            except Exception as e:
                self.pi.logger.warning(e.message)
        self.pi.posts.sort(key = lambda one: one.date, reverse = True)
        
        # add 'newer' and 'older' attribute to each post object
        for i in range(len(self.pi.posts)):
            self.pi.posts[i].newer = self.pi.posts[max(i-1,0)]
            self.pi.posts[i].older = self.pi.posts[min(i+1,len(self.pi.posts)-1)]

        for post in self.pi.posts:
            dest = os.path.join(
                self.pi.output,
                'posts', 
                os.path.basename(post.url)
            )
            data = post.render(self.pi).encode('utf-8')
            util.smartwrite(data, dest)

