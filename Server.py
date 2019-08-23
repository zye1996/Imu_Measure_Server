# coding=utf-8
from socket import *
import time
import signal
import os


TYPE = "FALLING"
dir = "./" + TYPE

# get the largest file name
if os.path.exists(dir):
    filenames = os.listdir(dir)
    if len(filenames):
        names = [int(n.split('.')[0]) for n in filenames]
        file_extention = max(names) + 1
    else:
        file_extention = 1
else:
    os.mkdir(dir)
    file_extention = 1


tcpSocket = socket(AF_INET, SOCK_STREAM)

# 重复使用绑定信息,不必等待2MSL时间
tcpSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

address = ('', 9999)
tcpSocket.bind(address)

tcpSocket.listen(5)


def exit_gracefully():
    tcpSocket.close()


signal.signal(signal.SIGINT, exit_gracefully)
signal.signal(signal.SIGTERM, exit_gracefully)



while True:
    time.sleep(0.01)
    print('开启等待')
    newData, newAddr = tcpSocket.accept()
    print('%s客户端已经连接，准备处理数据' % newAddr[0])
    data = ''

    try:
        cmd = input("Type in cmd")
        #time.sleep(5)
        newData.send(cmd.encode())
        data_count = 0
        while True:
            recvData = newData.recv(1024).decode()
            data_count = recvData.count('\n') + data_count
            data = data + recvData

            if len(recvData) > 0:
                print(recvData)
            else:
                print('%s客户端已经关闭' % newAddr[0])
                break
            if data_count == 128:
                newData.send('e'.encode())
                break
        filename = str(file_extention)+".txt"
        with open(dir+"/"+filename, 'w') as f:
            f.write(data)
            file_extention = file_extention + 1
    finally:
        newData.close()
