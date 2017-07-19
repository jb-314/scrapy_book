# -*- coding:utf-8 -*-
'''
电子书爬取操作
'''

from urllib import request
import time
import logging

logging.basicConfig(format='[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

class Scrapy:
    '''爬取操作类'''
    def __init__(self, url=None):
        if(url):
            __req = request.Request(url)
            __req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
            self._html = request.urlopen(__req)

    def set_Url(self, url):
        self.__url = url
        self.req = request.Request(url)
        self.req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
        try:
            logging.info('开始爬取%s...' % url)
            self._html = request.urlopen(self.req)
        except Exception as e:
            logging.warning('爬取%s失败,再次尝试...' % url)
            time.sleep(1)
            self.set_Url(self.__url)

    def set_sleep(self,num,step=20,time_=1):
        logging.info('爬取第%s页成功！' % str(num))
        if num / step == 0:
            time.sleep(time_)
        else:
            time.sleep(1)



if __name__ == '__main__':
    # scrapy = Scrapy('http://sha1.win/')
    scrapy = Scrapy()
    scrapy.set_Url('http://sha1.win/')
    print(scrapy._html)
    # scrapy.get_a()
