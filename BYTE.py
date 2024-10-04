"""
封装一些字节转换相关的函数

便于调用
"""

def i2b(x:int,l:int,byteorder="big"):
    """
    int -> `l` bytes
    """
    return int.to_bytes(x,l,byteorder)
def b2i(x:bytes,byteorder="big"):
    """
    bytes -> int
    """
    return int.from_bytes(x,byteorder)

def h2b(x:str):
    """
    hex str -> bytes
    """
    bytes.fromhex(x)

def b2h(x:bytes):
    """
    bytes -> hex str
    """
    return bytes.hex(x)

print(b2h(b'\x01\x02'))