#coding:utf-8
import random
import string
import json
import argparse
import time
import os
'''
usage:
python ss.py -m del  -f ./ss.json -pt 1112
python ss.py -m update  -f ./ss.json -pt 36000 -p test
python ss.py -m add -f ./ss.json -pt 1111 -p test
修改好之后，别忘记重启
'''

parser = argparse.ArgumentParser()
#提供的功能
parser.add_argument("-m","--mode", required=True, choices=["show", "reset","add","addall","remove","removeall"], help="support function(replace: pt and n(new pt))")
#指定修改的配置的json文件
parser.add_argument("-f","--filePath", type=str, default="/etc/shadowsocks/config.json", help="the ss json file path")
#账户所用的端口
parser.add_argument("-pt","--port", type=int,help="port for all mode")
#账户所用的密码
parser.add_argument("-p","--password", type=str, default="test",help="port's password for mode of add or update")
parser.add_argument("-n","--num", type=int, default=1, help="num of the accout for show or add")
a = parser.parse_args()

'''针对json中的所有端口，都进行监控'''
def addPortByJsonPath(path):
    load_f = open(path, 'r')
    load_dict = json.load(load_f)
    passwordDict = load_dict[u'port_password']
    keys = list(passwordDict.keys())

    str1 ="iptables -A INPUT  -p tcp --sport "
    str2 ="iptables -A OUTPUT -p tcp --sport "

    for i in range( len(keys)):
        key = keys[0]
        os.system(str1 + key)
        os.system(str2 + key)
        print("add port for flow : ",key)
    print("finish")
    return


'''删除端口的监控'''
def removeALL(path):
    load_f = open(path, 'r')
    load_dict = json.load(load_f)
    passwordDict = load_dict[u'port_password']
    keys = list(passwordDict.keys())

    str1 = "iptables -D INPUT  -p tcp --sport "
    str2 = "iptables -D OUTPUT -p tcp --sport "

    for i in range(len(keys)):
        key = keys[0]
        os.system(str1 + key)
        os.system(str2 + key)
        print("remove port for flow : ", key)
    print("finish")
    return


'''添加端口，都进行监控'''
def addPort(port):
    str1 ="iptables -A INPUT  -p tcp --sport "
    str2 ="iptables -A OUTPUT -p tcp --sport "
    os.system(str1 + port)
    os.system(str2 + port)
    print("add port for flow : ",port)
    print("finish")
    return

'''删除端口的监控'''
def removePort(port):
    str1 = "iptables -D INPUT  -p tcp --sport "
    str2 = "iptables -D OUTPUT -p tcp --sport "
    key = keys[0]
    os.system(str1 + port)
    os.system(str2 + port)
    print("remove port for flow : ", port)
    print("finish")
    return


'''删除指定端口的账户：修改已知端口的密码'''
def removeALL(path):
    load_f = open(path, 'r')
    load_dict = json.load(load_f)
    passwordDict = load_dict[u'port_password']
    keys = list(passwordDict.keys())

    str1 = "iptables -D INPUT  -p tcp --sport "
    str2 = "iptables -D OUTPUT -p tcp --sport "

    for i in range(len(keys)):
        key = keys[0]
        os.system(str1 + key)
        os.system(str2 + key)
        print("remove port for flow : ", key)
    print("finish")
    return



'''显示所有内容'''
def show():
    os.system("iptables -L -v -n -x")
    t = time.strftime('%Y_%m_%d_%s',time.localtime(time.time()))
    str = "iptables -L -v -n -x > netlog"+t+".txt"
    print("we save the log to nerlog.txt file")
    os.system(str)
    return

def reset():
    str1 = "Iptable -Z INPUT"
    str2 = "Iptable -Z INPUT"
    os.system(str1)
    os.system(str2)
    print('reset the net flow monitor success !')



if a.mode == "show":
    show()
elif a.mode =="addall"
    assert a.filePath
    addPortByJsonPath(a.filePath)
elif a.mode == "add":
    assert a.port
    addPort(a.port)
elif a.mode == "remove":
    assert a.port
    removePort(a.port)
elif a.mode == "removeall":
    assert a.filePath
    removeALL(a.filePath)
elif a.mode == "show":
    show()
