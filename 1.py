import VARIATION
import VARIATION.MODBUS
import VARIATION.OPCUA
data = "48454c465500000000000000ffff0000ffff0000c0ff3f0000020000350000006f70632e7463703a2f2f6c6f63616c686f73743a36323534312f517569636b7374617274732f5265666572656e6365536572766572"
data = bytes.fromhex(data)
# print(VARIATION.MODBUS.GENERAL_FUZZ_CHANGE(data))

# Map = []
# print(Map.count(b'\x123'))
# print(data[:2])
# import socket
# s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# s.connect(("192.168.1.88",4840))
data = VARIATION.OPCUA.GENERAL_FUZZ_CHANGE(data)
# s.send(data)
print(data)