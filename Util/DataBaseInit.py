# -*-coding:utf-8 -*-
# @Author: lixiao
# Created on: 2020-08-11

import pymysql
import time


class DataBaseInit:
    """初始化数据库操作，向appinfo表中插入爬取数据"""

    def __init__(self):
        self.host = '127.0.0.1'
        self.port = '3306'
        self.dbName = 'Appinfodb'
        self.username = 'root'
        self.password = '123456'
        self.charset = 'utf8'

    def insertdatas(self, datalist):
        """插入多条数据,留作后面优化使用"""
        try:
            conn = pymysql.connect(
                host=self.host,
                port=self.port,
                db=self.dbName,
                user=self.username,
                passwd=self.password,
                charset=self.charset
            )
            cur = conn.cursor()
            # 向测试表中插入多条测试数据
            sql = "insert into appinfo(appname, category, packagename, create_time, source_id, author_id) values(%s," \
                  "%s,%s,%s,%s,%s); "
            cur.executemany(sql, datalist)
        except pymysql.Error as e:
            raise e
        else:
            conn.commit()
        cur.close()
        conn.close()

    def insertdata(self, data):
        """插入单条数据"""
        try:
            conn = pymysql.connect(
                host=self.host,
                port=self.port,
                db=self.dbName,
                user=self.username,
                passwd=self.password,
                charset=self.charset
            )
            cur = conn.cursor()
            sql = "insert into appinfo(appname, category, packagename, create_time, source_id, author_id) values(%s," \
                  "%s,%s,%s,%s,%s); "
            cur.execute(sql, data)
        except pymysql.Error as e:
            raise e
        else:
            conn.commit()
        cur.close()
        conn.close()

    def selectbydate(self):
        """按日期查询已插入数据，以list形式返回"""
        try:
            conn = pymysql.connect(
                host=self.host,
                port=self.port,
                db=self.dbName,
                user=self.username,
                passwd=self.password,
                charset=self.charset
            )
            cur = conn.cursor()
            cur.execute("select appname from appinfo t where t.create_time like '{0}%';".format(
                time.strftime("%Y-%m-%d %H:%M:%S")))
            dataExistsList = []
            for i in cur.fetchall():
                # print (i)
                dataExistsList.append(i[0])
            cur.close()
            conn.close()
            return dataExistsList
        except pymysql.Error as e:
            raise e

    def selectalldata(self):
        "查询已插入的数据"
        try:
            conn = pymysql.connect(
                host=self.host,
                port=self.port,
                db=self.dbName,
                user=self.username,
                passwd=self.password,
                charset=self.charset
            )
            cur = conn.cursor()
            cur.execute("select * from appinfo")
            for i in cur.fetchall():
                print(i)
        except pymysql.Error as e:
            raise e
        else:
            cur.close()
            conn.close()

    def deletealldata(self):
        "删除所有数据"
        try:
            conn = pymysql.connect(
                host=self.host,
                port=self.port,
                db=self.dbName,
                user=self.username,
                passwd=self.password,
                charset=self.charset
            )
            cur = conn.cursor()
            cur.execute("delete from appinfo")
        except pymysql.Error as e:
            raise e
        else:
            conn.commit()
            cur.close()
            conn.close()


if __name__ == "__main__":
    db = DataBaseInit()
    datalist = [("和平精英", "动作枪战", "com.tencent.tmgp.pubgmhd", time.strftime("%Y-%m-%d %H:%M:%S"), 2, 1),
                ("红心自由麻将", "棋牌桌游", "com.k3k.qp.ziyou.mi", time.strftime("%Y-%m-%d %H:%M:%S"), 2, 1)]
    db.insertdatas(datalist)
    print(db.selectbydate())
    db.selectalldata()
    db.deletealldata()
