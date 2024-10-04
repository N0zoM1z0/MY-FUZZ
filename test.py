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

s.connect(('192.168.1.88',502))
PACK = PACKET_DATA.MODBUS.PACK
data = "010F0013000A02CD01BF08"
data = "0111"
data = "010600010003"
data = "01080000A537"
data = "02100001000204000A0102"
data = "010F0013000A02CD0108BF"
data = "01100001000204000A0102"
# data = "01080000A537"
# data = "010F0013000A0200000000"

# data = bytes.fromhex(data)
# data = b'\x01\x00\x01\x04\x00\x00'
# PACK = PACKET_DATA.MODBUS.PACK
# packet = PACK(data)
# s.send(packet)
# for i in range(10):
#     packet = (PREFIX + data)
#     s.send(packet)
#     data = VARIATION.MODBUS.CHANGE_0x08((data))
#     time.sleep(0.5)
# data = "01080000A537"
data = bytes.fromhex(data)
# data = VARIATION.MODBUS.CHANGE_0x08(data)
s.send(PACK(data))
print(PACK(data))
# queue = []
# MAX_LEN = 65536
# cur = 0
# queue.append(data)
# while True:
#     if (cur==200):break
#     if (cur % 100 == 0):
#         print(f"[-] {cur}")
#     top = queue[cur]
#     s.send(PACK(top))
#     for i in range(16):
#         newX = VARIATION.MODBUS.CHANGE_0x08(top)
#         queue.append(newX)
#     cur = (cur + 1) % MAX_LEN
#     time.sleep(0.1)


# import VARIATION.MODBUS as MODBUS

# print(VARIATION.MODBUS.CHANGE_0x08(bytes.fromhex(data)))