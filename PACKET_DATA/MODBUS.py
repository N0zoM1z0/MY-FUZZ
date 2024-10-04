"""
MODBUS 502端口 一堆功能码的一堆数据包
短的，长的都收集点
"""

PREFIX = "00010000"
FUNC_0x01 = "0101000b03e8"
FUNC_0x03 = "01030000000a"

FUNC_0x05 = "01050002FF00"
FUNC_0x06 = "010600010003"
# READ_EXCEPTION_STATUS 没有可变点
FUNC_0x07 = "0107"
FUNC_0x08 = "01080000A537"

FUNC_0x0F = "010F0013000A02CD01BF08"
FUNC_0x10 = "01100001000204000A0102"
FUNC_0x11 = "0111"

DATAS = ["",FUNC_0x01,"",FUNC_0x03,"",FUNC_0x05,FUNC_0x06,FUNC_0x07,FUNC_0x08,
         "","","","","","",FUNC_0x0F,FUNC_0x10,FUNC_0x11]
DATAS = [bytes.fromhex(x) for x in DATAS]

def PACK(data:bytes):
    return bytes.fromhex(PREFIX) + int.to_bytes(len(data),2) + data