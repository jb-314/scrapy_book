# -*- coding:utf-8 -*-

"""
生成epub格式的书
"""

from epub import Epub
from pyh import *
import logging

logging.basicConfig(format='[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

class Creator:

    def __init__(self, filename):
        self.ep = Epub(filename)
        self.lists = []

    def create_Book(self, filename, title, text):
        logging.info('开始创建-'+title+'...')
        try:
            page = PyH(title)
            page.addCSS('stylesheet.css')
            page << h1(title, cl='title')
            page << div(text, cl='content')
            self.ep.create_chapter(filename, page.out().getvalue())
            self.lists.append(filename+ '&' + title)
            logging.info('%s-创建成功' % title)
        except Exception as e:
            logging.error('创建%(filename)s错误->%(e)s' % {'filename':filename,'e':e})

    def create_After(self, creator='epub', language='zh'):
        self.ep.create_content(self.lists, creator, language)
        self.ep.create_ncx(self.lists)
        logging.info('电子书创建完成')

if __name__ == '__main__':
    creator = Creator('demo')
    creator.create_Book('1','1','content')
    creator.create_Book('2','2','content')
    creator.create_After()
