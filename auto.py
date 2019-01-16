#coding=utf-8

import pymysql
import socket
import datetime
import paramiko
from pytz import utc
from email.header import Header
from email.mime.text import MIMEText
import smtplib

class auto(object):
    def __init__(self):
        self.db = None
        self.results = None
        self.ip = None
        self.port_number = 0
    def mysql(self):
        self.db = pymysql.connect(host='172.16.255.219', user='django',
                             password='123456', db='django', port=3306)

        cursor = self.db.cursor()
        sql = "select * from auto_hostinfo"
        try:
            cursor.execute(sql)
            self.results = cursor.fetchall()
            #print(self.results)

        except Exception as e:
            raise e

        else:
            #self.db.close()
            self.socket()

    def ssh(self, ip, user, cmd, port_number):
        self.ip = ip
        self.user = user
        #self.password = password
        paivate_key = paramiko.RSAKey.from_private_key_file('/root/.ssh/id_rsa')
        self.cmd = cmd
        self.port_number = port_number
        port = 22
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.ip, port=port, username=self.user, pkey=paivate_key)
        stdin, stdout, stderr = ssh.exec_command(self.cmd)
        status = stdout.read().decode()
        now_date = datetime.datetime.now()
        status_date = now_date.astimezone(utc)
        isDelete = 0
        insert_ipdata = ('insert into auto_statusinfo(ip, port, status, status_date, isDelete) values(%s,%s,%s,%s,%s)')
        ip_data = (self.ip, self.port_number, status, status_date, isDelete)
        cursor = self.db.cursor()
        cursor.execute(insert_ipdata, ip_data)
        self.db.commit()

    #主机异常邮箱发送异常信息
    def sendmail(self, content, title):
        #邮件内容
        self.content = content
        #主题
        self.title = title

        #发送邮箱配置信息
        mail_host = "smtp.exmail.qq.com"
        mail_user = "guohui.zou@atkj6666.com"
        mail_pass = "5201314Zgh"

        sender = "guohui.zou@atkj6666.com"
        receivers = ["194462792@qq.com"]

        message = MIMEText(self.content, 'plain', 'utf-8')
        message['From'] = sender
        message['To'] = ",".join(receivers)
        message['Subject'] = Header(self.title, 'utf-8')

        try:
            smtpObj = smtplib.SMTP_SSL(mail_host, 465)
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(sender, receivers, message.as_string())
            print("发送成功！")
        except Exception as e:
            print(e)

    def socket(self):
        for i in self.results:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.ip = i[1]
            self.port_number = i[4]
            self.server_name = i[3]
            self.user = i[2]
            #self.password = i[3]
            self.cmd = i[5]
            re = sock.connect_ex((self.ip, self.port_number))
            print(re)
            if re == 0:
                status = "%s %s port is open" %(self.server_name, self.port_number)
                now_date = datetime.datetime.now()
                status_date = now_date.astimezone(utc)
                isDelete = 0
                print(now_date)
                insert_ipdata = ('insert into auto_statusinfo(ip, port, status, status_date, isDelete) values(%s,%s,%s,%s,%s)')
                ip_data = (self.ip, self.port_number, status, status_date, isDelete)
                cursor = self.db.cursor()
                cursor.execute(insert_ipdata, ip_data)
                self.db.commit()
            else:
                try:
                    self.ssh(self.ip, self.user, self.cmd, self.port_number)

                except Exception as e:
                    e = str(e)
                    now_date = datetime.datetime.now()
                    status_date = now_date.astimezone(utc)
                    isDelete = 0
                    print(now_date)
                    insert_ipdata = ('insert into auto_statusinfo(ip, port, status, status_date, isDelete) values(%s,%s,%s,%s,%s)')
                    ip_data = (self.ip, self.port_number, e, status_date, isDelete)
                    cursor = self.db.cursor()
                    cursor.execute(insert_ipdata, ip_data)
                    self.db.commit()
                    title_text = self.ip + "主机异常"
                    e = "主机告警信息：" + e
                    self.sendmail(e, title_text)
        sock.close()
        self.db.close()
if __name__ == "__main__":
    auto = auto()
    auto.mysql()
