# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 17:23:22 2024

@author: 2305004
"""

import paramiko
from datetime import datetime
#import time
import pty
import os
def ssh_and_write_log(host, username, private_key_path, command):
    try:
        # 创建 SSH 客户端对象
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # 指定私钥文件路径
        private_key = paramiko.RSAKey.from_private_key_file(private_key_path)

        # 连接远程主机
        ssh_client.connect(hostname=host, username=username, pkey=private_key)

        # 打开一个交互式shell会话
        shell = ssh_client.invoke_shell()

        # 发送sudo命令
        shell.send(f'sudo {command}\n')

        # 使用pty模块创建伪终端
        master, slave = pty.openpty()

        # 将伪终端的输入和输出重定向到远程主机的shell会话
        os.dup2(master, shell.fileno())
        os.dup2(master, shell.fileno())

        # 等待一段时间以确保命令执行完成
        while not shell.recv_ready():
            pass

        # 读取输出
        output = ''
        while shell.recv_ready():
            output += shell.recv(4096).decode()

        # 获取当前时间
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # 创建日志文件名
        log_filename = f"log_{current_time}.txt"

        # 写入日志文件
        with open(log_filename, 'w') as f:
            f.write(output)

        print(f"日志已保存至 {log_filename}")

    except Exception as e:
        print(f"连接失败: {e}")

    finally:
        # 关闭连接
        ssh_client.close()
# 示例用法

#host = '10.237.7.22'
host = '172.24.116.46'
username = 'logcheck'

private_key_path = 'id_rsa'

#command = 'sudo ls -l /var/log/IISI-PA820/'
command = 'sudo ls -l /var/log/'
ssh_and_write_log(host, username, private_key_path, command)