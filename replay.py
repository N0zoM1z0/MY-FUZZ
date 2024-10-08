"""
用来重放测试某些可疑数据包
"""
import socket
import time
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("192.168.6.6",502))

datas = ["000100000006000300fe0074000100000006000300ff0064000100000006170300000064",
         ""
         ]

# for data in datas:
    # packet = bytes.fromhex(data)
    # s.send(packet)
    # time.sleep(1)
# 
filename = r"D:\N0zoM1z0\Sec-Learning\Fuzz\PythonModbusFuzz\ModbusProtocol\raw_data"
filename = r"D:\N0zoM1z0\Sec-Learning\ICS\INOVANCE\INOVANCE汇川\id^%000001_last_messages,sig^%00,src^%000000,op^%havoc,rep^%64"
filename = r"D:\N0zoM1z0\Sec-Learning\Fuzz\id^%000000,sig^%00,src^%000000,op^%havoc,rep^%2"
filename = r"D:\N0zoM1z0\Sec-Learning\Fuzz\id^%000000,sig^%00,src^%000000,op^%havoc,rep^%4"
data = open(filename,"rb+").read()
# for i in range(10):
#     s.send(data)
#     time.sleep(1)

s.send(data)