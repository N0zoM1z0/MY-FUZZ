"""
MODBUS协议

主要针对每个功能码有意义的字段进行变异

emmm, 写不来的先空着, 后面慢慢完善

TODO:
1. 扩充, 还有好几个功能码没有实现
2. 增加try except异常处理
3. 在正常实现的基础上, 加一些变异
4. 
"""
import random
import VARIATION.CHANGE as CHANGE

def CHANGE_1(data:bytes):
    """
    针对单线圈/单寄存器的,都是这种结构,没必要拆开来。
    针对性变异字段(下标):
    6 9 11
    """
    poss = [6,9,11]
    rd = random.randint(0,2) + random.randint(0,2) + random.randint(0,2)
    rd %= 3
    pos = poss[rd]
    new_data = CHANGE.SINGLE_BYTE_CHANGE(data,pos)
    return new_data

def CHANGE_0x01(data:bytes): # 传入的是MODBUS的PDU,没有封装前面的TCP的
    """
    READ COILS

    从设备地址 | 功能码(0x01) | 起始地址高 | 起始地址低 | 线圈数量高 | 线圈数量低
    """
    try:
        poss = [2,3,4,5]
        rd = random.choice(poss)
        pos = rd
        new_data = CHANGE.SINGLE_BYTE_CHANGE(data,pos)
        return new_data
    except:
        raise Exception("Error in CHANGE_0x01!")
    pass

def CHANGE_0x05(data:bytes):
    """
    WRITE SINGLE COIL

    从设备地址 | 功能码(0x05) | 输出地址高 | 输出地址低 | 输出值高 | 输出值低
    
    理论上,output value只能取FF 00:打开; 00 00:关闭
    """
    try:
        poss = [2,3]
        pos = random.choice(poss)
        new_data = CHANGE.SINGLE_BYTE_CHANGE(data,pos)
        newX = int.from_bytes(new_data)
        rd = random.randint(0,255)
        if rd & 1:
            if CRAZY == 0:
                newX ^= 0xFF << 8
            else:
                newX ^= random.randint(0,255) << 8
        new_data = int.to_bytes(newX,6)
        return new_data
    except:
        pass

def CHANGE_0x06(data:bytes):
    """
    WRITE SINGLE REGISTER

    从设备地址 | 功能码(0x06) | 寄存器地址高 | 寄存器地址低 | 寄存器值高 | 寄存器值低
    
    这个值就可以是任意值
    """
    try:
        poss = [2,3]
        pos = random.choice(poss)
        new_data = CHANGE.SINGLE_BYTE_CHANGE(data,pos)
        poss = [4,5]
        pos = random.choice(poss)
        new_data = CHANGE.SINGLE_BYTE_CHANGE(new_data,pos)
        return new_data
    except:
        pass


def CHANGE_0x08(data:bytes):
    """
    DIAGNOSTICS

    从设备地址 | 功能码(0x08) | 子功能码(2B) | 数据(Nx2 Bytes)
    
    这个值就可以是任意值

    TODO 
    1) 概率可能需要优化; 
    2) 这个DIAGNOSTICS发的包的rep一直都是Exception Returned。。。(貌似是设备没开这个功能罢)
    """
    try:
        sub_cmds = [       0x0001,0x0002,0x0003,0x0004,
                    0x000A,0x000B,0x000C,0x000D,0x000E,
                    0x000F,0x0010,0x0011,0x0012,0x0014
                ]
        # 大多数从已知的sub_cmds中选, 当然可以变异选择不在里面的, 按概率来
        # 把 0x0000剔除了, 跟变异的拎一块
        sub_cmd = 0x0000
        old_data = data
        data = ''
        rd = random.randint(0,65535)
        if CRAZY == 0:
            if rd % 1024 == 17: # 小概率选择其他的sub_cmd
                while True:
                    sub_cmd = random.randint(0,0xFFFF)
                    if sub_cmd not in sub_cmds:
                        break
            else:
                sub_cmd = random.choice(sub_cmds)
        else:
            if rd % 2 == 0: # 1/2概率选择其他的sub_cmd
                while True:
                    sub_cmd = random.randint(0,0xFFFF)
                    if sub_cmd not in sub_cmds:
                        break
            else:
                sub_cmd = random.choice(sub_cmds)

        # 针对在sub_cmds中的不同的子功能码，相应的变异处理也不同。。。
        # print("[-] sub_cmd : ",hex(sub_cmd))
        if sub_cmd == 0x0000:
            """
            请求数据字段中传递的数据将在响应中返回（回送）。整个响应消息应与请求完全相同。
            这个请求字段任意。。。 2*N bytes
            """
            n = random.randint(1,256)
            b = hex(random.randint(0,256))[2:]
            data += b*n
            
        elif sub_cmd == 0x0001:
            """
            重新启动通信选项
            请求数据字段为FF 00十六进制会导致端口的通信事件日志也被清除。请求数据字段为00 00将保留日志在重新启动之前的状态。
            """
            data += random.choice(["0000","FF00"])
        elif sub_cmd == 0x0002:
            """
            返回诊断寄存器
            响应中返回远程设备的16位诊断寄存器的内容。
            """
            data += "0000"
        elif sub_cmd == 0x0003:
            """
            更改ASCII输入分隔符
            请求数据字段中传递的字符'CHAR'将成为未来消息的结束分隔符（替代默认的LF字符）。在ASCII消息末尾不需要换行符的情况下，此功能非常有用。
            CHAR 00
            """
            rd = random.randint(0,255)
            data += hex(rd)[2:] + "00"
        elif sub_cmd == 0x0004:
            """
            强制进入仅监听模式
            强制被寻址的远程设备进入仅监听模式，用于MODBUS通信。这将使其与网络上的其他设备隔离，允许它们在不受干扰的情况下继续通信。不返回响应。
            """
            data += "0000"
        elif sub_cmd in sub_cmds:
            """
            0x0A 0x0B 0x0C 0x0D 0x0E 0x0F 0x10 0x11 0x12 0x14
            """
            data += "0000"
        else:
            """
            变异得到的不在sub_cmds中的其他sub_cmd
            """
            if CRAZY == 0:
                n = random.randint(10,1000)
            else:
                n = random.randint(555,1000)
            b = hex(random.randint(0,256))[2:]
            data += b*n

        try:
            new_data = old_data[:2] + int.to_bytes(sub_cmd,2) + bytes.fromhex(data)
        except:
            new_data = old_data
        # print("[+] old_data : ",old_data)
        # print("[+] new_data : ",new_data)
        return new_data
    except:
        pass

def CHANGE_0x0F(data:bytes):
    """
    Write Multiple Coils

    从设备地址 | 0x0F | 起始地址(2B) | output值(2B) | output值/8(N) | N*1 Byte

    TODO:
    还是一样的问题, 发过去得不到"正常"的回显
    """
    try:
        new_data = data[:1]
        new_data += b'\x0F'
        # new_data += random.randbytes(2)
        new_data += data[3:5]
        if CRAZY == 0:
            # 控制N小一点
            N = random.randint(1,0x7B0)
            N = random.randint(1,N)
            N = random.randint(1,N)
            N = random.randint(1,N)
        else:
            N = random.randint(0x666,0x7B0)
        new_data += int.to_bytes(N,2)
        new_data += int.to_bytes(N//8+1)
        b = random.randint(0,0x0A)
        b = int.to_bytes(b)
        new_data += b * N
        return new_data
    except:
        raise Exception("Error in CHANGE_0x0F!")

def CHANGE_0x10(data:bytes):
    """
    Write Multiple registers

    从设备地址 | 0x10 | 起始地址(2B) | 寄存器数量(2B)N | 2*N | 值 2*N bytes
    """
    try:
        new_data = data[:2]
        new_data += random.randbytes(2)
        if CRAZY == 0:
            N = random.randint(1,0x7B)
        else:
            N = random.randint(0x7B,0x7C)
        new_data += int.to_bytes(N,2)
        bc = N*2
        new_data += int.to_bytes(bc,1)
        v = random.randint(0,0xA)
        v = int.to_bytes(v,1)
        new_data += v * bc
        return new_data
    except:
        raise Exception("Error in CHANGE_0x10!")

FUNCTIONS = [None,CHANGE_0x01,None,None,None,CHANGE_0x05,
             CHANGE_0x06,None,CHANGE_0x08,None,None,
             None,None,None,None,CHANGE_0x0F,CHANGE_0x10]

#=================================
FUNCTIONS = FUNCTIONS[::-1]
# FUNCTIONS = FUNCTIONS[:2][::-1]

#=================================
CRAZY = 1 # 是否更离谱的fuzz……
#=================================
# print(CHANGE_1(b'\x00\x12\x34\x56'))

# print(CHANGE.INC_ONE_BYTE_CHANGE(b'\x00\x11\x22\x33',1))