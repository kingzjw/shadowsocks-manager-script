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
parser.add_argument("-m","--mode", required=True, choices=["add", "update","del","show","clearall","randadd","backup"], help="support function")
#指定修改的配置的json文件
parser.add_argument("-f","--filePath", type=str, default="/etc/shadowsocks/config.json", help="the ss json file path")
#账户所用的端口
parser.add_argument("-pt","--port", type=int,help="port for all mode")
#账户所用的密码
parser.add_argument("-p","--password", type=str, default="test",help="port's password for mode of add or update")
parser.add_argument("-n","--num", type=int, default=1, help="num of the accout for show or add")
a = parser.parse_args()

'''添加新账户：端口和密码。 可以不提供密码，系统会生成密码'''
#path: ss.json的路径和文件名字
#port : int
#password: string
def addPortPassword(path, port, password="test"):
    load_f = open(path, 'r')
    load_dict = json.load(load_f)
    passwordDict = load_dict[u'port_password']
    uport = unicode(str(port), "utf-8")

    if(password=="test"):
        passwordList = generate_activation_code(len=8, n=1)
        password = passwordList[0]

    uPassword = unicode(password, "utf-8")

    # judege port
    if passwordDict.has_key(uport):
        print "this file already have this port " + str(port)
        print "do nothing"
        return

    passwordDict[uport] = uPassword;

    print("add:  port " + uport + " ,  password " + uPassword)
    saveF = open(path, "w")
    json.dump(load_dict, saveF,sort_keys = True, indent=0)
    print("save success")

    return

'''修改指定账户的密码：已知端口的密码。可以不提供密码，系统会生成密码'''
def changePasswordByPort(path, port, password="test"):
    load_f = open(path, 'r')
    load_dict = json.load(load_f)
    passwordDict = load_dict[u'port_password']

    if (password == "test"):
        passwordList = generate_activation_code(len=8, n=1)
        password = passwordList[0]

    uport = unicode(str(port), "utf-8")
    uPassword = unicode(password, "utf-8")

    #judege port
    if not passwordDict.has_key(uport):
        print "this file do not have port " + str(port)
        print "do nothing"
        return

    passwordDict[uport] = uPassword;
    print("update:  port "+uport+" ,  password "+uPassword)
    saveF = open(path, "w")
    json.dump(load_dict, saveF ,sort_keys = True, indent=0)
    print("save success")

    return

'''删除指定端口的账户：修改已知端口的密码'''
def deleteUser(path, port):
    load_f = open(path, 'r')
    load_dict = json.load(load_f)
    passwordDict = load_dict[u'port_password']

    uport = unicode(str(port), "utf-8")

    #judege port
    if not passwordDict.has_key(uport):
        print "this file do not have port " + str(port)
        print "do nothing"
        return

    del passwordDict[uport]
    #sort
    #sorted(passwordDict.keys())

    print("delete: port " + uport)
    saveF = open(path, "w")
    json.dump(load_dict, saveF,sort_keys = True, indent=0)
    print("save success")
    return

'''显示某个账户的密码'''
def showUser(path, port, num=1):
    load_f = open(path, 'r')
    load_dict = json.load(load_f)
    passwordDict = load_dict[u'port_password']

    num = min(num, len(passwordDict))
    print("showing...")
    for i in range(num):
        t = port + i
        uport = unicode(str(t), "utf-8")
        if not passwordDict.has_key(uport):
            print "this file do not have port " + str(t)
        else:
            print("port " + uport + " password " + passwordDict[uport])
    print("show success")
    return

'''删除所有的账户'''
def clearALL(path):
    load_f = open(path, 'r')
    load_dict = json.load(load_f)
    passwordDict = load_dict[u'port_password']

    # clear all account
    num = len(passwordDict)
    passwordDict.clear()
    print( "clear all account: "+ str(num))
    saveF = open(path, "w")
    json.dump(load_dict, saveF, sort_keys=True, indent=0)
    return

'''添加num个账户，密码随机生成'''
#添加的端口号，包含startPort在内开始的num个，默认是一个
def addAccoutByNumRandomPassword(path, startPort, num=1):
    assert startPort>=1 and startPort <=65535
    assert startPort+num >= 1 and startPort + num<= 65535

    load_f = open(path, 'r')
    load_dict = json.load(load_f)
    passwordDict = load_dict[u'port_password']

    #generator password
    passwordList = generate_activation_code(len = 8, n = num)
    for i in range(num):
        port = startPort+i
        password = passwordList[i]
        uport = unicode(str(port), "utf-8")
        uPassword = unicode(password, "utf-8")
        # judege port
        if passwordDict.has_key(uport):
            print "this file already have this port " + str(port)
        else:
            passwordDict[uport] = uPassword;
            print("add:  port " + uport + " ,  password " + uPassword)

    saveF = open(path, "w")
    json.dump(load_dict, saveF, sort_keys=True, indent=0)
    print("save success")
    return
'''生成n个长度为len的随机序列码'''
#len: 密码长度
#n: 个数
#return: 返回的是一个n个密码的列表
def generate_activation_code(len=16, n=200):
    random.seed()
    #chars: 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    chars = string.ascii_letters + string.digits
    return [''.join([random.choice(chars) for _ in range(len)]) for _ in range(n)]

'''备份指定文件'''
def backupConfig(path):
    if os.path.isfile(path):  # 判断该路径的是否是文件
        # 截取文件名，重组文件名
        seek_num = path.rfind('.')
        str = time.strftime("_%Y_%m_%d", time.localtime())
        new_file_name = path[:seek_num] + '_backup'+str + path[seek_num:]
        # 打开源文件
        old_file = open(path, 'rb')
        # 读取文件信息
        old_file_content = old_file.read()
        # 创建新文件
        new_file = open(new_file_name, 'wb')
        # 将原始文件信息写入
        new_file.write(old_file_content)
        # 关闭文件
        old_file.close()
        new_file.close()
        print "backup the file to "+ new_file_name
    else:
        print('there is no such file')
    return

if a.mode == "add":
    addPortPassword(a.filePath, a.port, a.password);
elif a.mode == "update":
    changePasswordByPort(a.filePath, a.port, a.password);
elif a.mode == "del":
    deleteUser(a.filePath, a.port);
elif a.mode == "show":
    showUser(path=a.filePath,port=a.port,num=a.num)
elif a.mode == "clearall":
    clearALL(path = a.filePath)
elif a.mode == "randadd":
    addAccoutByNumRandomPassword(path=a.filePath,startPort=a.port,num=a.num)
elif a.mode == "backup":
    backupConfig(path=a.filePath)
