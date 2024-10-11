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
        l = random.randint(0,4)
        func = random.choice(BYTE_CHANGE_FUNCS)
        try:
            poss = random.sample(range(1, len(recBufSize) + 1), l)
        except:
            poss = [random.randint(0,len(recBufSize))]
        pos = random.randint(0,len(recBufSize))

        if func == CHANGE.SINGLE_BYTE_CHANGE:
            recBufSize = CHANGE.SINGLE_BYTE_CHANGE(recBufSize,pos)
        elif func == CHANGE.MULTI_BYTE_CHANGE:
            recBufSize = CHANGE.MULTI_BYTE_CHANGE(recBufSize,poss)

        data += recBufSize

        """
        sdBufSize
        """

        func = random.choice(BYTE_CHANGE_FUNCS)
        try:
            poss = random.sample(range(1, len(sdBufSize) + 1), l)
        except:
            poss = [random.randint(0,len(sdBufSize))]
        pos = random.randint(0,len(sdBufSize))

        if func == CHANGE.SINGLE_BYTE_CHANGE:
            sdBufSize = CHANGE.SINGLE_BYTE_CHANGE(sdBufSize,pos)
        elif func == CHANGE.MULTI_BYTE_CHANGE:
            sdBufSize = CHANGE.MULTI_BYTE_CHANGE(sdBufSize,poss)

        data += sdBufSize

        """
        maxMsgSize
        """
        func = random.choice(BYTE_CHANGE_FUNCS)
        try:
            poss = random.sample(range(1, len(maxMsgSize) + 1), l)
        except:
            poss = [random.randint(0,len(maxMsgSize))]
        pos = random.randint(0,len(maxMsgSize))

        if func == CHANGE.SINGLE_BYTE_CHANGE:
            maxMsgSize = CHANGE.SINGLE_BYTE_CHANGE(maxMsgSize,pos)
        elif func == CHANGE.MULTI_BYTE_CHANGE:
            maxMsgSize = CHANGE.MULTI_BYTE_CHANGE(maxMsgSize,poss)

        data += maxMsgSize

        """
        maxBlkCnt
        """
        func = random.choice(BYTE_CHANGE_FUNCS)
        try:
            poss = random.sample(range(1, len(maxBlkCnt) + 1), l)
        except:
            poss = [random.randint(0,len(maxBlkCnt))]
        pos = random.randint(0,len(maxBlkCnt))

        if func == CHANGE.SINGLE_BYTE_CHANGE:
            maxBlkCnt = CHANGE.SINGLE_BYTE_CHANGE(maxBlkCnt,pos)
        elif func == CHANGE.MULTI_BYTE_CHANGE:
            maxBlkCnt = CHANGE.MULTI_BYTE_CHANGE(maxBlkCnt,poss)

        data += maxBlkCnt

        """
        EpUrl

        这个有点难弄...
        TODO
        1. 变异url?
        2. 增加url长度
        3. 还得考虑与MessageSize的契合...
        """
        data += EpUrl
        return data



    elif MessageType == b'ACK':
        """
        """
    elif MessageType == b'ERR':
        """
        """
    elif MessageType == b'RHE':
        """
        """

def GENERAL_FUZZ_CHANGE(data:bytes):
        """

    """
    
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
        return new_data

    
        return data

FUNCTIONS = []