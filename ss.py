#coding:utf-8
'''
usage:
python ss.py -m del  -f ./ss.json -pt 1112
python ss.py -m update  -f ./ss.json -pt 36000 -p test
python ss.py -m add -f ./ss.json -pt 1111 -p test
修改好之后，别忘记重启
'''

import json
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-m","--mode", required=True, choices=["add", "update","del"])
parser.add_argument("-f","--filePath", type=str, default="/etc/shadowsocks.json", required=True, help="the ss json file path")
parser.add_argument("-pt","--port",  required=True, type=int,help="port for all mode")
parser.add_argument("-p","--password", type=str, help="port's password for mode of add or update")
a = parser.parse_args()

'''添加新的端口和密码'''
#path: ss.json的路径和文件名字
#port : int
#password: string
def addPortPassword(path, port, password):
    load_f = open(path, 'r')
    load_dict = json.load(load_f)
    passwordDict = load_dict[u'port_password']
    uport = unicode(str(port), "utf-8")
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

'''修改已知端口的密码'''
def changePasswordByPort(path, port, password):
    load_f = open(path, 'r')
    load_dict = json.load(load_f)
    passwordDict = load_dict[u'port_password']

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

'''删除端口账户'''
'''修改已知端口的密码'''
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


if a.mode == "add":
    addPortPassword(a.filePath, a.port, a.password);
elif a.mode == "update":
    changePasswordByPort(a.filePath, a.port, a.password);
elif a.mode == "del":
    deleteUser(a.filePath, a.port);
