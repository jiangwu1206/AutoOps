import pymysql
import socket
import datetime
import paramiko

class auto(object):
    def __init__(self):
        self.db = None
        self.results = None
        self.ip = None
        self.port_number = 0
    def mysql(self):
        self.db = pymysql.connect(host='localhost', user='test',
                             password='123456', db='test2', port=3306)

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
        try:
            ssh.connect(hostname=self.ip, port=port, username=self.user, pkey=paivate_key)
        except Exception as e:
            status = e
            status_date = datetime.datetime.now()
            insert_ipdata = ('insert into auto_statusinfo(ip, port, status, status_date) values(%s,%s,%s,%s)')
            ip_data = (self.ip, self.port_number, status, status_date)
            cursor = self.db.cursor()
            cursor.execute(insert_ipdata, ip_data)
            self.db.commit()
            #print("登录成功！")
            #print(self.cmd)
        else:
            stdin, stdout, stderr = ssh.exec_command(self.cmd)
            status = stdout.read().decode()
            status_date = datetime.datetime.now()
            insert_ipdata = ('insert into auto_statusinfo(ip, port, status, status_date) values(%s,%s,%s,%s)')
            ip_data = (self.ip, self.port_number, status, status_date)
            cursor = self.db.cursor()
            cursor.execute(insert_ipdata, ip_data)
            self.db.commit()
    def socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for i in self.results:
            self.ip = i[1]
            self.port_number = i[5]
            self.server_name = i[4]
            self.user = i[2]
            #self.password = i[3]
            self.cmd = i[6]
            re = sock.connect_ex((self.ip, self.port_number))
            if re == 0:
                status = "%s %s port is open" %(self.server_name, self.port_number)
                status_date = datetime.datetime.now()
                print(status_date)
                insert_ipdata = ('insert into auto_statusinfo(ip, port, status, status_date) values(%s,%s,%s,%s)')
                ip_data = (self.ip, self.port_number, status, status_date)
                cursor = self.db.cursor()
                cursor.execute(insert_ipdata, ip_data)
                self.db.commit()
            else:
                self.ssh(self.ip, self.user, self.cmd, self.port_number)
        sock.close()
        self.db.close()
if __name__ == "__main__":
    auto = auto()
    auto.mysql()