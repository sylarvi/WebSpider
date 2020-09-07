# -*-coding:utf-8 -*-
# @Author: lixiao
# Created on: 2020-08-11

import requests
from lxml import etree
from Util.UserAgent import get_headers


class GetLink:
    def __init__(self, url):
        self.url = url
        self.headers = get_headers()

    def get_html(self, url):
        html = requests.get(url=url, headers=self.headers)
        return html

    def __get_categoryid(self):
        """获取页面app类别id列表用于拼接url"""
        html = self.get_html(self.url).text
        # 使用xpath解析页面提取category_id
        parse_obj = etree.HTML(html)
        li_list = parse_obj.xpath('//ul[@class="category-list"]/li')

        return li_list

    def __get_counts(self, val):
        """获取某一应用类别总数计算得到总页数用于拼接url"""
        url = self.url + 'categotyAllListApi?page={}&categoryId={}&pageSize=30'.format(1, val)
        html = self.get_html(url).json()
        app_counts = html['count'] // 30 + 1

        return app_counts

    def getValidLink(self):
        url_list = []
        li_list = self.__get_categoryid()
        for li in li_list:
            item = {}
            category_name = li.xpath('./a/text()')[0]
            category_id = li.xpath('./a/@href')[0].split('/')[-1]
            app_counts = self.__get_counts(category_id)
            item['category_name'] = category_name
            item['category_id'] = category_id
            item['url'] = self.url + 'categotyAllListApi?page={}&categoryId={}&pageSize=30'
            item['counts'] = app_counts
            url_list.append(item)

        return url_list


if __name__ == '__main__':
    spider = GetLink('http://app.mi.com/')
    url_lst = spider.getValidLink()
    for url in url_lst:
        print(url)


