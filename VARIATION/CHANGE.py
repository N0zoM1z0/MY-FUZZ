"""
通用变异策略函数封装
"""
import random
CHANGE_FUNCTIONS = []
def XOR_FF(x):
    """
        x^0xFF
    """
    return x ^ 0xFF
    pass
def XOR_FE(x):
    """
    x^0xFE
    """
    return x ^ 0xFE
    pass

def POW_2(x):
    """
    x**2
    """
    return (x ** 2) & 0xFF
    pass

def ADD_10(x):
    """
    x+0x10
    """
    return (x + 0x10) & 0xFF
    pass

def MUL_17(x):
    """
    x*0x17
    """
    return (x * 0x17) & 0xFF
    pass

def INC(x):
    """
    x++
    """
    return (x + 1) & 0xFF
def RND_BIT(x):
    """
    Reverse random bit of `x`
    """
    p0w = random.randint(0,7)
    _xor = 1 << p0w
    return x ^ _xor



CHANGE_FUNCTIONS = [XOR_FF,XOR_FE,POW_2,ADD_10,MUL_17,RND_BIT,INC]
    
def SINGLE_BYTE_CHANGE(data:bytes,pos:int,func = None):
    """
    只变异一个字节
    """
    if func not in CHANGE_FUNCTIONS: # 没指定 or 指定不存在，我们随机选一个
        func = random.choice(CHANGE_FUNCTIONS)
    if (pos<0 or pos>len(data)-1):
        pos = random.randint(0,len(data)-1)

    x = data[pos]
    newX = func(x)
    hex_str = format(newX, '02x')
    data = data[:pos] + bytes.fromhex(hex_str) + data[pos + 1:]
    return data
    pass

def INC_ONE_BYTE_CHANGE(data:bytes,pos:int,bt=None):
    """
    增加一字节
    """
    if bt == None:
        bt = random.randint(0,255)
    bt = (bt<<3) | (bt>>5)
    bt &= 0xFF
    hex_str = format(bt, '02x')
    newData = data[:pos] + bytes.fromhex(hex_str) + data[pos:]
    return newData
    pass