#coding=utf-8

import pymysql

def delmysql():
    #数据库配置
    db = pymysql.connect(host='192.168.242.160', user='test',
                         password='123456', db='django', port=3306)
    cursor = db.cursor()
    sql = "truncate auto_statusinfo"

    try:
        cursor.execute(sql)
        print("清空成功！！！")

    except Exception as e:
        print(e)
if __name__ == "__main__":
    delmysql()