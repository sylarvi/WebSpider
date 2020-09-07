# -*-coding:utf-8 -*-
# @Author: lixiao
# Created on: 2020-08-11

import pymysql
from hashlib import md5


class FingerVertify:
    def __init__(self, url):
        self.url = url
        self.db = pymysql.connect('127.0.0.1', 'root', '123456', 'Appinfodb', charset='utf8')
        self.cursor = self.db.cursor()

    def make_fingersign(self):
        s = md5()
        s.update(self.url.encode())
        fingersign = s.hexdigest()

        return fingersign

    def vertify_fingersign(self):
        finger = self.make_fingersign()
        finger_list = []
        sql_bds = 'select finger from request_finger'
        fingers = self.cursor.execute(sql_bds)
        for i in fingers:
            finger_list.append(i[0])

        if finger in finger_list:
            return False
        else:
            sql_bds = 'insert into request_finger value(%s)'
            try:
                self.cursor.execute(sql_bds, finger)
            except Exception as e:
                print('Finger insert failed', e)
            self.db.commit()
            self.cursor.close()
            self.db.close()
            return True


if __name__ == '__main__':
    finger = FingerVertify('http://app.mi.com/categotyAllListApi?page=2&categoryId=5&pageSize=30')
    print(finger.vertify_fingersign())