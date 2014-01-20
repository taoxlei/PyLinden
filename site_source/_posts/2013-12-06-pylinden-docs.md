
---
title: "PyLinden的文档"
tags: 
  - PyLinden
  - 文档
---



介绍
====

PyLinden是什么？
---------------

PyLinden是Python实现的一个静态博客生成器

源于对Github Pages的些许不满意（国外服务商，没有相册功能），以及对python的喜爱。

可以轻松部署于BAE（Baidu App Engine），实践云式网络生活方式。

仅使用文件系统，摒弃数据库以及BAE的bucket等存储服务。如果要迁移，也几乎只是拷贝文件而已。

支持（且仅支持）markdown格式书写日志，如果不清楚markdown的优点请度娘谷哥之。

支持代码着色（pygments），兼容Github Pages方式。具体看"日志"里的"代码着色"。

基于简单够用的设计哲学构建。在没有大的思想波动的前提下，仅会实现日志与相册两块。


文件结构
--------

* admin文件夹：包含BAE部署时Web方式的后台实现。
* pygments文件夹：著名的代码高亮项目，BAE自带的有问题。
* pylinden文件夹：本项目主要代码。
* site_source文件夹：供生成站点的原料，你可以修改成自己的风格。
* app.conf：BAE部署配置文件。
* local_run.py：本地部署测试脚本。
* pylinden.wpr和pylinden.wpu：WING IDE项目文件。

BAE部署
-------

 
推荐BAE部署。假定你了解BAE环境，概要步骤如下。
 
新建Web应用，python后台。
创建新版本，上传程序包。
开启NFS功能，上线（非必要，不过可以使url好看点）。
写日志：site_source/_posts目录下新建日志（utf-8 without BOM）即可，格式参考此目录下的示例。
假设你的应用url为example.duapp.com，访问example.duapp.com/admin，点击“生成”。
访问example.duapp.com。

上传程序包时注意：程序包应是直接包含admin、pylinden、site_source等内容的zip格式压缩包，切勿放到一个文件夹里再打包。

 
BAE提供了定时任务Cron功能。登录BAE，找到“Cron（定时任务）”，新建一个。下图是每分钟“生成”一次的示例。

![doc_cron](/static/doc_cron.jpg)

执行URL改成你自己的，类似这样：http://example.duapp.com/admin/do?cmd=generate

由于BAE的分布式NFS服务的原因，“生成”完成之后，一般会有几秒到几分钟的延迟才能访问到最新内容。另外，上图示例中定时任务Cron的时间间隔为一分钟，所以也会有几秒的延迟。


本地部署
--------
 
不推荐本地部署，但提供以下一些依赖信息：

python：版本2.7
pygment：代码高亮
yaml：yaml格式解析
markdown：markdown格式
jinja2：模板引擎


教程
====

在线写作
--------

BAE有比较方便的在线编辑器，在任何地方想写点东西时，打开浏览器登录BAE来写日志也方便至极。

使用git或者svn写作
------------------

也支持git和svn。在自己的常用电脑上必然是优选git或者svn。

文件编码问题

与Github Pages相同，所有的文本文件请使用utf-8 without BOM格式保存。

Windows XP自带的记事本无法保存成这种格式的！

site_source文件结构说明

此文件夹包含了最终被生成的静态博客的原料，是部署完成后使用最频繁的文件夹。 

以<code>_</code>(下划线)或者<code>.</code>(点)开头的文件夹和文件是：特殊文件夹和文件、隐藏文件夹和文件。

* _posts文件夹：此文件夹包含了以markdown格式书写的日志文件。有类似Github Pages一样的文件头；文件后缀不要求.md或者.markdown。
* _gallery文件夹：此文件夹包含了生成相册的原料。
* _base.html文件：全站页面的基本模板(jinja2模板引擎)，方便使所有页面基本布局同意。
* _post.html文件：日志页面模板(jinja2模板引擎)。

模板修改提示
------------

jinja2是所使用的模板引擎，它很方便和简洁。想了解基本的jinja2使用方法的请花几分钟google之，亦或可以直接修改原有的文件（site_source文件夹下的html后缀的文件并非是纯HTML文件）。
 
本静态博客生成器主要提供了两个相关变量供jinja2模板调用：

    site：此变量包含了博客生成过程中的所有内容。
    site.pages: 一些页面，如index.html、about.html等。
    site.pages.html: 最终的HTML格式的内容。
    site.posts: 所有的日志。

    site.post[i].title: 标题。
    site.post[i].date: 日期。
    site.post[i].tags: 标签。
    site.post[i].html: 已经渲染成HTML格式的日志正文。
    site.post[i].url: 日志的URL，如<code>/posts/hello-world.html。
    site.post[i].older: 较旧的一篇日志，即site.posts[i-1]或者site.posts[0]。
    site.post[i].newer: 较新的一篇日志。

    site.tags: 所有日志的标签的集合。
    post：此变量只有在_post.html模板中才可用，包含了此篇日志的相关内容。 参考上面的site.posts[i]。


    
