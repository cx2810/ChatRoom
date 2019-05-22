"""
    Chat room
    env:python3.6
    socket fork
    聊天室服务端程序
"""

import os
import sys
from socket import *
from time import sleep

# 服务器地址
ADDR = ('176.215.155.118', 2810)
# 用户信息
user = {}


def main():
    """
        创建网络连接
    :return:
    """
    # 套接字
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(ADDR)

    pid = os.fork()
    if pid < 0:
        return
    # 发送管理员消息
    elif pid == 0:
        while True:
            text = input("管理员消息:")
            msg = "C 管理员消息 " + text
            s.sendto(msg.encode(), ADDR)
            if text == "10秒后服务器关闭.":
                for i in range(9):
                    sleep(1)
                    s.sendto(f"C 管理员消息 {9-i}秒后服务器关闭.".encode(), ADDR)
                for item in user:
                    s.sendto(b"EXIT", user[item])
                sleep(1)
                sys.exit("服务器关闭.")
    else:
        do_request(s)


def do_request(s):
    """
        接收各种客户端的请求
    :param s: 套接字
    :return:
    """
    while True:
        data, addr = s.recvfrom(1024)
        msg = data.decode().split()

        # 区分请求类型
        if msg[0] == "L":
            do_login(s, msg[1], addr)
        elif msg[0] == "C":
            text = ' '.join(msg[2:])
            do_chat(s, msg[1], text)
        elif msg[0] == "Q":
            do_quit(s, msg[1])


def do_login(s, name, addr):
    """
        处理进入聊天室请求
    :param s: 套接字
    :param name: 用户姓名
    :param addr: 用户地址
    :return:
    """
    if name in user or "管理员" in name:
        s.sendto("该用户已存在".encode(), addr)
        return

    s.sendto(b"OK", addr)

    # 通知其他人
    msg_welcom = "欢迎%s进入聊天室" % name
    for key in user:
        s.sendto(msg_welcom.encode(), user[key])

    # 将用户加入
    user[name] = addr


def do_chat(s, name, text):
    """
        聊天过程,
        将用户发送信息发送给其他所有用户
    :param s: 套接字
    :param name: 用户姓名
    :param text: 用户发送信息
    :return:
    """

    msg = "%s : %s" % (name, text)
    for item in user:
        if item != name:
            s.sendto(msg.encode(), user[item])


def do_quit(s, name):
    """
        退出聊天室
    :param s: 套接字
    :param name: 用户姓名
    :return:
    """
    msg = "%s退出聊天室" % name
    for item in user:
        if item != name:
            s.sendto(msg.encode(), user[item])
        else:
            s.sendto(b"EXIT", user[item])
    del user[name]


if __name__ == "__main__":
    main()
