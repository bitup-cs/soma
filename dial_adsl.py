import os
import time
import socket
import json

g_adsl_account = {"name": "adsl",
                  "username": "08527385031",
                  "password": "731632"}


class Adsl(object):
    # ==============================================================================
    # __init__ : name: adsl名称
    # ==============================================================================
    def __init__(self, username, password):
        self.name = 'adsl'
        self.username = username
        self.password = password

    # ==============================================================================
    # set_adsl : 修改adsl设置
    # ==============================================================================
    def set_adsl(self, account):
        self.name = account["name"]
        self.username = account["username"]
        self.password = account["password"]

    # ==============================================================================
    # connect : 宽带拨号
    # ==============================================================================
    def connect(self):
        cmd_str = "rasdial %s %s %s" % (self.name, self.username, self.password)
        os.system(cmd_str)
        time.sleep(5)

    # ==============================================================================
    # disconnect : 断开宽带连接
    # ==============================================================================
    def disconnect(self):
        cmd_str = "rasdial /disconnect "
        os.system(cmd_str)
        time.sleep(5)

    # ==============================================================================
    # reconnect : 重新进行拨号
    # ==============================================================================
    def reconnect(self):
        self.disconnect()
        self.connect()

    def getip(self):
        myname = socket.getfqdn(socket.gethostname())
        myaddr = socket.gethostbyname(myname)
        print("IP : ", myaddr)
        return myaddr

    def dial(self):
        ips = {}
        self.connect()
        with open("ip.json", 'r+') as f:
            ips = json.load(f)
            cur_ip = self.getip()
            while cur_ip in ips.keys():
                ips[cur_ip] += 1
                self.reconnect()
                cur_ip = self.getip()
            ips[cur_ip] = 1

        with open("ip.json", 'w') as fw:
            json.dump(ips, fw, indent= 4)



if __name__ == "__main__":
    adsl = Adsl()
    adsl.connect()
    adsl.getip()
    for x in range(1000):
        time.sleep(5)
        adsl.reconnect()
        adsl.getip()
