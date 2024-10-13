"""
通用变异策略函数封装
"""
import random
CHANGE_FUNCTIONS = []
def XOR_FF(x,pd):
    """
    x^0xFF
    x^0xFFFF
    x^0xFFFFFFFF
    """
    if pd == 1:
        return x ^ 0xFF
    elif pd == 2:
        return x ^ 0xFFFF
    elif pd == 4:
        return x ^ 0xFFFFFFFF
    pass
def XOR_FE(x,pd):
    """
    x^0xFE
    x^0xFEFE
    x^0xFEFEFEFE
    """
    if pd == 1:
        return x ^ 0xFE
    elif pd == 2:
        return x ^ 0xFEFE
    elif pd == 4:
        return x ^ 0xFEFEFEFE
    pass

def POW_2(x,pd):
    """
    x**2
    """
    if pd == 1:
        return (x**2) & 0xFF
    elif pd == 2:
        return (x**2) & 0xFFFF
    elif pd == 4:
        return (x**2) & 0xFFFFFFFF
    pass

def ADD_10(x,pd):
    """
    x+0x10
    """
    if pd == 1:
        return (x+0x10) & 0xFF
    elif pd == 2:
        return (x+0x1010) & 0xFFFF
    elif pd == 4:
        return (x+0x10101010) & 0xFFFFFFFF
    pass

def MUL_17(x,pd):
    """
    x*0x17
    """
    if pd == 1:
        return (x**0x17) & 0xFF
    elif pd == 2:
        return (x**0x17) & 0xFFFF
    elif pd == 4:
        return (x**0x17) & 0xFFFFFFFF
    pass

def INC(x,pd):
    """
    x++
    """
    if pd == 1:
        inc = random.randint(0,256)
        return (x+inc) & 0xFF
    elif pd == 2:
        inc = random.randint(0,16**4)
        return (x+inc) & 0xFFFF
    elif pd == 4:
        inc = random.randint(0,16**8)
        return (x+inc) & 0xFFFFFFFF
def RND_SINGLE_BIT(x,pd):
    """
    Reverse random bit of `x`
    """
    if pd == 1:
        p0w = random.randint(0,7)
        _xor = 1 << p0w
        return (x ^ _xor) & 0xFF
    elif pd == 2:
        p0w = random.randint(0,15)
        _xor = 1 << p0w
        return (x ^ _xor) & 0xFFFF
    elif pd == 3:
        p0w = random.randint(0,31)
        _xor = 1 << p0w
        return (x ^ _xor) & 0xFFFFFFFF
        

def RND_MULTI_BIT(x,pd):
    """
    Reverse random bits of `x`
    先2bit
    """
    if pd == 1:
        p0w1 = random.randint(0,7)
        p0w2 = random.randint(0,7)
        while p0w1 == p0w2:
            p0w2 = random.randint(0,7)
        _xor = (1 << p0w1) ^ (1 << p0w2)
        return x ^ _xor
    elif pd == 2:
        p0w1 = random.randint(0,15)
        p0w2 = random.randint(0,15)
        while p0w1 == p0w2:
            p0w2 = random.randint(0,15)
        _xor = (1 << p0w1) ^ (1 << p0w2)
        return x ^ _xor     
    elif pd == 4:
        p0w1 = random.randint(0,31)
        p0w2 = random.randint(0,31)
        while p0w1 == p0w2:
            p0w2 = random.randint(0,31)
        _xor = (1 << p0w1) ^ (1 << p0w2)
        return x ^ _xor

CHANGE_FUNCTIONS = [XOR_FF,XOR_FE,POW_2,ADD_10,MUL_17,RND_SINGLE_BIT,RND_MULTI_BIT,INC]
    
def SINGLE_BYTE_CHANGE(data:bytes,pos:int,func = None):
    """
    只变异一个字节
    """
    if func not in CHANGE_FUNCTIONS: # 没指定 or 指定不存在，我们随机选一个
        func = random.choice(CHANGE_FUNCTIONS)
    if (pos<0 or pos>len(data)-1):
        pos = random.randint(0,len(data)-1)

    x = data[pos]
    newX = func(x,1)
    hex_str = format(newX, '02x')
    data = data[:pos] + bytes.fromhex(hex_str) + data[pos + 1:]
    return data
    pass

def SINGLE_WORD_CHANGE(data:bytes,pos:int,func = None):
    """
    变异一个字(4B)
    """
    try:
        if func not in CHANGE_FUNCTIONS: # 没指定 or 指定不存在，我们随机选一个
            func = random.choice(CHANGE_FUNCTIONS)
        if (pos<0 or pos>len(data)-4):
            pos = random.randint(0,len(data)-4)

        x = data[pos]
        newX = func(x,4)
        hex_str = format(newX, '02x')
        data = data[:pos] + bytes.fromhex(hex_str) + data[pos + 4:]
    except:
        pass
    return data

def MULTI_BYTE_CHANGE(data:bytes,poss:list,func = None):
    """
    变异多个字节
    """
    if func not in CHANGE_FUNCTIONS: # 没指定 or 指定不存在，我们随机选一个
        func = random.choice(CHANGE_FUNCTIONS)
    try:
        for pos in poss:
            x = data[pos]
            newX = func(x,1)
            hex_str = format(newX, '02x')
            data = data[:pos] + bytes.fromhex(hex_str) + data[pos + 1:]
    except:
        pass
    return data

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

def INC_MULTI_BYTE_CHANGE(data:bytes,poss:list,bt=None):
    """
    增加多个字节
    多个字节是一样的
    """
    try:
        if bt == None:
            bt = random.randint(0,255)
        bt = (bt<<3) | (bt>>5)
        bt &= 0xFF
        hex_str = format(bt, '02x')
        for pos in poss:
            data = data[:pos] + bytes.fromhex(hex_str) + data[pos:]
    except:
        pass
    return data

def INC_CRAZY_BYTE_CHANGE(data:bytes,poss:list):
    """
    CRAZY!
    ~~肆意增加~~
    """
    try:
        for pos in poss:
            bt = random.randint(0,255)
            bt = (bt<<3) | (bt>>5)
            bt &= 0xFF
            hex_str = format(bt, '02x')
            data = data[:pos] + bytes.fromhex(hex_str) + data[pos:]
    except:
        pass
    return data

def RND_CHANGE_BYTE(data:bytes,ratio:float = 0.5):
    """
    封装的一个常用的, 随机选择单/多字节变异的函数

    @ratio: 变异比率
    """
    BYTE_CHANGE_FUNCS = CHANGE_FUNCS[:3]
    func = random.choice(BYTE_CHANGE_FUNCS)
    l = int(len(data)*ratio)
    try:
        poss = random.sample(range(1, len(data) + 1), l)
    except:
        poss = [random.randint(0,len(data))]
    pos = random.randint(0,len(data))

    if func == SINGLE_BYTE_CHANGE:
        data = SINGLE_BYTE_CHANGE(data,pos)
    elif func == MULTI_BYTE_CHANGE:
        data = MULTI_BYTE_CHANGE(data,poss)
    return data
    


CHANGE_FUNCS = [SINGLE_BYTE_CHANGE,MULTI_BYTE_CHANGE,SINGLE_WORD_CHANGE,INC_ONE_BYTE_CHANGE,INC_MULTI_BYTE_CHANGE,INC_CRAZY_BYTE_CHANGE]
#               0                  1                 2                   3                     4


# print(SINGLE_WORD_CHANGE(b'\x01\x02\x03\x04\x05\x06',2))