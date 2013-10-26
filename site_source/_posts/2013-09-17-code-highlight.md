---
layout: post
title: "代码着色（pygments）"
tags: 
  - Python
  - 代码着色
  - pygments
---

测试代码着色1(与Githbu Pages兼容方式)：

{% highlight python %}
#-*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
from __future__ import absolute_import

import os, re
from .utils import logger
from markdown import Markdown

def func(m):
    text = m.group()
    #logger.info(text)
    return text.replace("&lt;","<").replace("&gt;",">")

class Parser(Markdown):
    def __init__(self):
        Markdown.__init__(self)
        self.preprocessors.insert(0, 'HighlightPreprocessor', HighlightPreprocessor())
        #self.postprocessors.insert(0, 'HighlightPostprocessor', HighlightPostprocessor())
        
    def parse(self, source):
        return self.convert(source)
{% endhighlight %}

测试代码着色2：

	:::python
	#-*- coding:utf-8 -*-

	from __future__ import unicode_literals, print_function
	from __future__ import absolute_import

	import os, re
	from .utils import logger
	from markdown import Markdown

	def func(m):
	    text = m.group()
	    #logger.info(text)
	    return text.replace("&lt;","<").replace("&gt;",">")

	class Parser(Markdown):
	    def __init__(self):
	        Markdown.__init__(self)
	        self.preprocessors.insert(0, 'HighlightPreprocessor', HighlightPreprocessor())
	        #self.postprocessors.insert(0, 'HighlightPostprocessor', HighlightPostprocessor())
	        
	    def parse(self, source):
	        return self.convert(source)