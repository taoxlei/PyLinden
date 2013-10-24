#-*- coding:utf-8 -*-

from __future__ import unicode_literals, print_function
from __future__ import absolute_import

import sys, cmd
from .generator import Generator


class CLI(cmd.Cmd):
    def __int__(self):
        cmd.Cmd.__int__(self)
        self.prompt='(aaa)'
        self.intro='''PyCDC0.5 使用说明
                      dir 目录名   #指定保存和搜索的目录，默认是'CDC'
                      walk 文件名  #指定光盘信息文件名，使用'*.cdc'
                      find 关键词   #使用在保存和搜索目录中遍历所有.cdc文件，输出含有关键词的行
                      ？          #查询
                      EOF         #退出系统
                      '''
    def help_EOF(self):
        print('退出程序')
    def do_EOF(self,line):
        sys.exit
    
    def do_generate(self, line):
        gen = Generator()
        gen.generate()
    def help_generate(self, line):
        print('help for generate')
        
CLI().cmdloop()