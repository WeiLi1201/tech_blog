@[TOC](impyla: python impala 工具类)

#  impyla 工具类 

写了一个工具类，复制粘贴可用，包含权限验证，单SQL执行批量执行的例子，其中自定义批量执行的方法 exec_manyquery_mine() 适用于官方批量sql 无法拼接的问题，希望对你有帮助，关于如何批量执行，以及批量执行的实例网上很多是错误的，在此告诉你正确的示例。

## impala 工具类(权限验证、executemany、自定义批量执行方法)

下面是 `代码`.
```python
// An highlighted block
import unittest
from impala.dbapi import connect
from impala.hiveserver2 import HiveServer2Cursor


class impala_util:
    def __init__(self,host,port,user,pwd,db):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        if not self.db:
            raise(NameError,"没有设置数据库信息")
        self.conn = connect(host=self.host,port=self.port,user=self.user,password=self.pwd,database=self.db)

        cur: HiveServer2Cursor = self.conn.cursor(user="hive")
        if not cur:
            raise(NameError,"连接数据库失败")
        else:
            return cur

    def exec_query(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        #查询完毕后必须关闭连接
        self.conn.close()
        return resList

    def exec_manyquery(self,sql,params):
        cur = self.__GetConnect()
        cur.executemany(sql,params)
        resList = cur.fetchall()

        #查询完毕后必须关闭连接
        self.conn.close()
        return resList


    def ExecNonQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

    def exec_manyquery_mine(self, sql, params):
        cur = self.__GetConnect()
        res_list = []
        for param in params:
            operator = sql % param
            cur.execute(operation=operator)
            res = cur.fetchone()
            res_list.append(res)
        # res_list = cur.fetchmany()
        self.conn.close()

        return res_list


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)

    def test_impala(self):
        impala_cli = impala_util(host='10.x.x.x',port=21050,user='xxxx',pwd='xxxx',db='xxxxx')
        sql = 'show create table xxxx.xxxxx;'
        res_list = impala_cli.exec_query(sql=sql)
        for data in res_list:
            print(data)
            
    def test_impala_many(self):
        impala_cli = impala_util(host='10.x.x.x',port=21050,user='xxxx',pwd='xxxx',db='xxxxx')
        sql = "show create table %s;"
        params = ["xxxxx.xxxxx","xxxxx.xxxxx"]
        res_list = impala_cli.exec_manyquery_mine(sql=sql,params=params)
        for data in res_list:
            print(data)
```
