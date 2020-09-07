# -*-coding:utf-8 -*-
# @Author: lixiao
# Created on: 2020-08-11

from Util.DataBaseInit import *
from Util.FingerSign import *
from Util.GetLink import *
from threading import Thread
from queue import Queue
from time import time


class DataSpider:
    def __init__(self, url):
        self.url_list = GetLink(url).getValidLink()
        self.q = Queue()

    def url_in(self):
        for item in self.url_list:
            for page in range(item['counts']):
                url = item['url'].format(page, item['category_id'])
                self.q.put(url)

    def parse_page(self):
        self.url_in()
        while True:
            if not self.q.empty():
                url = self.q.get()
                if FingerVertify.vertify_fingersign(url):
                    html = GetLink(url).get_html(url).json()
                    for appinfo in html['data']:
                        displayname = appinfo['displayName']
                        category = appinfo['level1CategoryName']
                        packagename = appinfo['packageName']
                        create_time = time.strftime("%Y-%m-%d %H:%M:%S")
                        source_id = '2'
                        author_id = '1'
                        DataBaseInit.insertdata((displayname, category, packagename, create_time, source_id, author_id))
                else:
                    continue
            else:
                break

    def main(self):
        threading_list = []
        for number in range(5):
            t = Thread(target=self.parse_page())
            threading_list.append(t)
            t.start()

        for t in threading_list:
            t.join()


if __name__ == '__main__':
    start_time = time.time()
    spider = DataSpider('http://app.mi.com/')
    spider.main()
    end_time = time.time()
    print('Total Time:%.2f' % (end_time - start_time))



