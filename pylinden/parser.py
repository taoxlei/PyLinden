#-*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
from __future__ import absolute_import

import os, re
from .utils import logger
from markdown import Markdown
from markdown.preprocessors import Preprocessor
from markdown.postprocessors import Postprocessor


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
    
class HighlightPostprocessor(Postprocessor):
    def run(self, text):
        text = re.sub("<pre><code>{%[ ]highlight", "{% highlight", text)
        text = re.sub("endhighlight[ ]%}[\s]</code></pre>", "endhighlight %}", text)
        text = re.sub("{% highlight[\s\S]*endhighlight %}", func, text)
        return text

def func(m):
    text = m.group()
    #logger.info(text)
    return text.replace("&lt;","<").replace("&gt;",">")

class Parser(Markdown):
    def __init__(self):
        Markdown.__init__(self, extensions=['codehilite(noclasses=True)'])
        self.preprocessors.insert(0, 'HighlightPreprocessor', HighlightPreprocessor())
        #self.postprocessors.insert(0, 'HighlightPostprocessor', HighlightPostprocessor())
        
    def parse(self, source):
        return self.convert(source)

