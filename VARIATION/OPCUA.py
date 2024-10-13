"""
OPC UA 协议
4840 端口 (opcua-tcp)
主要实现的其实是 opcua-tcp, 即over tcp的opcua协议;
还有另外一个`OPC UA Secure Conversation`


协议可能存在的问题:
1. 消息大小与消息体不匹配：如果消息大小字段的值小于消息长度，是否会带来缓冲区溢出的问题
2. 消息大小字段、接收缓冲区/发送缓冲区大小字段可以指定高达2^32的内存分配,可能会引起资源耗尽从而导致拒绝服务
3. 终端URL是否会导致潜在的安全问题?例如连接到恶意URL
"""

import random
import VARIATION.CHANGE as CHANGE
from BYTE import *

class OPCUA_PACKET():
    """
    opcua 报文的封装
    格式:
    MessageType(3B)  |  Reserved(1B)  |  MessageSize(4B LE) |  Payload

    """

    def __init__(self,MessageType:bytes,Reserved:bytes,MessageSize:int,Payload:bytes) -> None:
        self.MessageType = MessageType
        self.Reserved = Reserved # b'F'
        self.MessageSize = MessageSize
        self.Payload = Payload
        self.data = MessageType + Reserved + i2b(MessageSize,4,"little") + Payload
        pass
    def __str__(self):
        s = rf"""============OPCUA PACKET DATA============
            MessageType : {self.MessageType}
            Reserved : {self.Reserved}
            MessageSize : {hex(self.MessageSize)}
            Payload : {self.Payload}
=========================================="""
        
    def PACK(self):
        """
        对opcua数据包的封装
        """
        data = b''
        data += self.MessageType
        data += self.Reserved
        data += i2b(self.MessageSize,4,"little")
        data += self.Payload
        return data
    
    # MessageType
    KNOWN_MTs = [b'HEL',b'ACK',b'ERR',b'RHE']


    pass

def PAYLOAD_CHANGE(MessageType:bytes,MessageSize:int,Payload:bytes):
    """
    针对四种不同的类型 作不同的变异
    """
    if MessageType == b'HEL':
        """
        HELLO报文
        pVersion(4B)  |  recBufSize(4B LE)  |  sdBufSize(4B LE)  |  maxMsgSize(4B LE)  |  maxBlkCnt(4B LE)  |  EpUrl( <= 4096B)
        """
        pVersion = Payload[:4]
        recBufSize = Payload[4:8]
        sdBufSize = Payload[8:12]
        maxMsgSize = Payload[12:16]
        maxBlkCnt = Payload[16:20]
        EpUrl = Payload[20:]
        
        BYTE_CHANGE_FUNCS = CHANGE.CHANGE_FUNCS[:3]
        INC_CHANGE_FUNCS = CHANGE.CHANGE_FUNCS[3:]

        data = b''

        """
        pVersion
        """

        data += pVersion
        
        """
        recBufSize
        """
        data += CHANGE.RND_CHANGE_BYTE(recBufSize)

        """
        sdBufSize
        """
        data += CHANGE.RND_CHANGE_BYTE(sdBufSize)

        """
        maxMsgSize
        """
        data += CHANGE.RND_CHANGE_BYTE(maxMsgSize)

        """
        maxBlkCnt
        """
        data += CHANGE.RND_CHANGE_BYTE(maxBlkCnt)

        """
        EpUrl

        这个有点难弄...
        TODO
        1. 变异url?
        2. 增加url长度
        3. 还得考虑与MessageSize的契合...

        主要是保证长度对应, 这个影响不大
        """
        data += EpUrl[:11] + CHANGE.RND_CHANGE_BYTE(EpUrl[11:])
        return data



    elif MessageType == b'ACK':
        """
        ACK报文
        虽说一般都是服务端发回给我们, 但是fuzz随便弄, 指不定把PLC弄崩溃了呢。。
        pVersion(4B)  |  recBufSize(4B LE)  |  sdBufSize(4B LE)  |  maxMsgSize(4B LE)  |  maxBlkCnt(4B LE)
        """
        pVersion = Payload[:4]
        recBufSize = Payload[4:8]
        sdBufSize = Payload[8:12]
        maxMsgSize = Payload[12:16]
        maxBlkCnt = Payload[16:20]

        data = b''

        """
        pVersion
        """
        data += pVersion
        
        """
        recBufSize
        """
        data += CHANGE.RND_CHANGE_BYTE(recBufSize)

        """
        sdBufSize
        """
        data += CHANGE.RND_CHANGE_BYTE(sdBufSize)

        """
        maxMsgSize
        """
        data += CHANGE.RND_CHANGE_BYTE(maxMsgSize)

        """
        maxBlkCnt
        """
        data += CHANGE.RND_CHANGE_BYTE(maxBlkCnt)

        return data
        

    elif MessageType == b'ERR':
        """
        ErrCode (4B)  |  ErrReason (<= 4096B)
        """
        ErrCode = Payload[:4]
        ErrReason = Payload[4:]
        data = b''

        """
        ErrCode
        后续可以补一个ERRCODE列表, 现在就随便variate了
        """
        data += CHANGE.RND_CHANGE_BYTE(ErrCode)
        
        """
        ErrReason
        """
        data += CHANGE.RND_CHANGE_BYTE(ErrReason)

        return data

    elif MessageType == b'RHE':
        """
        SvURL (<= 4096B)  |  EpURL (<= 4096B)
        """

        """
        ...

        """
        return Payload

def GENERAL_FUZZ_CHANGE(data:bytes):
    """
    如果真要四种交叉的话, 得开多个队列。。。
    或者不考虑有效报文, malformed也无妨
    """
    try:
        MessageType = data[:3]
        Reserved = data[3:4]
        MessageSize = data[4:8]
        MessageSize = b2i(MessageSize,"little")
        Payload = data[8:]
        new_data = b''

        """
        MessageType 变异
        TODO:
        1. 四种
        """
        MessageType = random.choice(OPCUA_PACKET.KNOWN_MTs)
        new_data += MessageType

        """
        Reserved
        """
        new_data += Reserved

        """
        MessageSize 变异
        TODO:
        1. 变异
        """
        new_data += i2b(MessageSize,4,"little")

        """
        Payload 变异
        """
        new_payload = PAYLOAD_CHANGE(MessageType,MessageSize,Payload)
        new_data += new_payload
        prob = random.randint(0,65536)
        if prob % 117 == 1:
            """
            小概率不管长度, 发多少是多少, 甚至加长度
            """
            prob = random.randint(0,65536)
            if prob % 3 == 1:
                return new_data
            else:
                """
                增加长度
                """
                l = random.randint(1,7)
                for i in range(l):
                    new_data += CHANGE.RND_CHANGE_BYTE(new_payload,0,2)
                return new_data
        else:
            new_data = new_data.ljust(MessageSize,random.randbytes(1))
            return new_data[:MessageSize]

    except:
        return data

FUNCTIONS = [GENERAL_FUZZ_CHANGE]