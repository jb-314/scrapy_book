from scrapy import Scrapy
from bs4 import BeautifulSoup
from creator import Creator
import os

def run():
    scrapy = Scrapy()

    num = 1
    while num < 66:
        n = str(num)
        scrapy.set_Url('http://m.136zw.com/wapbook-95_'+n+'/')
        get_lists('http://m.136zw.com', scrapy._html)
        scrapy.set_sleep(num, step=10, time_=2)
        # with open('demo/'+n+'.html', 'wb') as f:
        #     f.write(scrapy._html)
        num += 1

def get_lists(rootUrl, html):
    soup = BeautifulSoup(html)
    lists = soup.find('ul', class_='chapter').find_all('li')

    for list in lists:
        s = str(list.find('a').get_text()) + '&' + rootUrl + str(list.find('a')['href']) + '\n'
        with open('tmp', 'a',encoding='utf-8') as f:
            f.write(s)

def get_content():
    lists = []
    scrapy = Scrapy()
    creator = Creator('九天神龙诀')
    with open('tmp', 'r',encoding='utf-8') as f:
        lists = f.readlines()
    num = 1
    for l in lists:
        title, url = l.replace('\n','').split('&')
        scrapy.set_Url(url)
        soup = BeautifulSoup(scrapy._html)
        content = soup.find('div',id='nr1')
        creator.create_Book(str(num),title,content)
        scrapy.set_sleep(num,time_=3)
        num += 1
        # print(content)
        # print(scrapy._html.read())
        # with open('h.html', 'w', encoding='utf-8') as f:
            # f.write(str(content))
    creator.create_After()


def over():
    os.remove('tmp')


if __name__ == '__main__':
    # over()
    # run()
    get_content()
    over()
