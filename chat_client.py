"""
    聊天室客户端
"""
import os
import sys
from socket import *

# 服务器地址
ADDR = ('176.215.155.118', 2810)


def main():
    """
        创建网络连接
    :return:
    """
    s = socket(AF_INET, SOCK_DGRAM)
    while True:
        name = input("请输入姓名:")
        msg = "L " + name
        s.sendto(msg.encode(), ADDR)
        # 等待回应
        data, addr = s.recvfrom(1024)
        if data.decode() == "OK":
            print("Welcom to the chat room")
            break
        else:
            print(data.decode())

    # 创建新的进程
    pid = os.fork()
    if pid < 0:
        sys.exit("Error!")
    elif pid == 0:
        send_msg(s, name)
    else:
        recv_msg(s)


def send_msg(s, name):
    """
        发送消息
    :param s:字节套
    :param name:用户姓名
    :return:
    """
    while True:
        try:
            text = input("")
        except KeyboardInterrupt:
            text = "quit"
        if text == "quit":
            msg = "Q " + name
            s.sendto(msg.encode(), ADDR)
            sys.exit("退出聊天室")
        msg = "C %s %s" % (name, text)
        s.sendto(msg.encode(), ADDR)


# 接收消息
def recv_msg(s):
    while True:
        data, addr = s.recvfrom(1024)
        # 服务端发送EXIT表示让客户端接收消息进程退出
        if data.decode() == "EXIT":
            sys.exit()
        print(data.decode())


if __name__ == "__main__":
    main()
