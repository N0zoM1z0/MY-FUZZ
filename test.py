"""
用来发协议包 wireshark抓一些数据报文的
"""


import socket
import time
import VARIATION.MODBUS
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
import PACKET_DATA.MODBUS
import VARIATION
import PACKET_DATA.MODBUS
import VARIATION.ETHERNETIP

# s.connect(('192.168.250.2',44818))

data = "63000000000000000000000000000000062ec1be00000000"
data = bytes.fromhex(data)

data = VARIATION.ETHERNETIP.GENERAL_FUZZ_CHANGE(data)
# s.send(data)
print(data)