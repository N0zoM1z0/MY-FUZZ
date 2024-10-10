"""
EthernetIP协议
44818 端口
或许把CIP也包含尽量比较好;
CIP也是在ENIP的基础上加了一个Common Industrial Protocol(Command Specific Data不为空)

TODO
1. CIP (感觉optional吧。。。)
2. 优化 (比如增加初始报文种类)
3. ...
"""

import random
import VARIATION.CHANGE as CHANGE
from BYTE import *

class ENIP_PACKET():
    """
    ENIP数据包的结构封装
    """
    def __init__(self,Command,Length,Session_Handle,Status,Sender_Context,Options,
    Command_Specific_Data:bytes = None):
        self.Command = Command
        self.Length = Length # len(Command_Specific_Data)
        self.Session_Handle = Session_Handle
        self.Status = Status
        self.Sender_Context = Sender_Context
        self.Options = Options
        self.Command_Specific_Data = Command_Specific_Data
        self.lens = [2,2,4,4,8,4] # 各部分的Byte长度
        self.datas = [
                        Command,Length,Session_Handle,Status,
                        Sender_Context,Options,Command_Specific_Data
                    ]
    def __str__(self):
        s = rf"""============ENIP PACKET DATA============
            Command : {hex(self.Command)}
            Length : {hex(self.Length)}
            Session_Handle : {hex(self.Session_Handle)}
            Status : {hex(self.Status)}
            Sender_Context : {hex(self.Sender_Context)}
            Options : {hex(self.Options)}
            Command_Specific_Data : {self.Command_Specific_Data}
========================================="""
        return s
    
    def PACK(self):
        """
        对ENIP数据包的封装
        有些字段的大小端序还得测试看看
        """
        data = b''
        data += toLittle(self.Command,2)
        data += toLittle(self.Length,2)
        data += toLittle(self.Session_Handle,4)
        data += toLittle(self.Status,4)
        data += toBig(self.Sender_Context,8)
        data += toLittle(self.Options,4)
        data += self.Command_Specific_Data
        return data

    # Command
    ENCAP_CMD_NOP                       = 0x0000
    ENCAP_CMD_LISTSERVICES              = 0x0004
    ENCAP_CMD_LISTIDENTITY              = 0x0063
    ENCAP_CMD_LISTINTERFACES            = 0x0064
    ENCAP_CMD_REGISTERSESSION           = 0x0065
    ENCAP_CMD_UNREGISTERSESSION         = 0x0066
    ENCAP_CMD_SENDRRDATA                = 0x006F
    ENCAP_CMD_SENDUNITDATA              = 0x0070
    ENCAP_CMD_INDICATESTATUS            = 0x0072
    ENCAP_CMD_CANCEL                    = 0x0073

    KNOWN_CMDS = [
                    ENCAP_CMD_NOP,ENCAP_CMD_LISTSERVICES,ENCAP_CMD_LISTIDENTITY,ENCAP_CMD_LISTINTERFACES,
                    ENCAP_CMD_REGISTERSESSION,ENCAP_CMD_UNREGISTERSESSION,ENCAP_CMD_SENDRRDATA,
                    ENCAP_CMD_SENDUNITDATA,ENCAP_CMD_INDICATESTATUS,ENCAP_CMD_CANCEL
                ]
    
    # Status
    ENCAP_STATUS_SUCCESS                = 0x0000
    ENCAP_STATUS_INVALID_CMD            = 0x0001
    ENCAP_STATUS_OUT_OF_MEMORY          = 0x0002
    ENCAP_STATUS_INCORRECT_DATA         = 0x0003
    ENCAP_STATUS_INVALID_LENGTH         = 0x0065
    ENCAP_STATUS_UNSUPPORTED_VERSION    = 0x0069
    
    KNOWN_STATUS = [
                    ENCAP_STATUS_SUCCESS,ENCAP_STATUS_INVALID_CMD,ENCAP_STATUS_OUT_OF_MEMORY,
                    ENCAP_STATUS_INCORRECT_DATA,ENCAP_STATUS_INVALID_LENGTH,ENCAP_STATUS_UNSUPPORTED_VERSION
                ]
    pass

KNOWN_CMDS = ENIP_PACKET.KNOWN_CMDS
KNOWN_STATUS = ENIP_PACKET.KNOWN_STATUS

def GENERAL_FUZZ_CHANGE(data:bytes):
    """
    ETHERNET-IP协议数据包的变异

    Command: 2B
    Length: 2B
    Session Handle: 4B
    Status: 4B
    Sender Context: 8B
    Options: 4B
    Command Specific Data: Length B
    """
    try:
        Command = data[:2]
        Length = data[2:4]
        Session_Handle = data[4:8]
        Status = data[8:12]
        Sender_Context = data[12:20]
        Options = data[20:24]
        Command_Specific_Data = data[24:]
        
        new_data = []
        """
        Command
        大概率选择KNWON_CMDS内的
        """
        prob = random.randint(0,65536)
        if prob % 17 == 1:
            Command = random.randint(0,0xFF) # 这个得看cmd的范围
        else:
            Command = random.choice(KNOWN_CMDS)

        """
        Command Specific Data && Length
        就瞎变异吧, 和MODBUS的data[2:]一样的
        后续可以把这个单独抽出来做个module
        """
        BYTE_CHANGE_FUNCS = CHANGE.CHANGE_FUNCS[:3]
        INC_CHANGE_FUNCS = CHANGE.CHANGE_FUNCS[3:]
        prob = random.randint(0,65536)
        """
        多BYTE 少INC
        """
        if prob % 7 != 3:
            func = random.choice(BYTE_CHANGE_FUNCS)
        else:
            func = random.choice(INC_CHANGE_FUNCS)
        l = 2
        prob = random.randint(0,65536)
        if prob % 17 == 1:
            l = random.randint(2,10)
            l = random.randint(2,l)
            l <<= 1
        try:
            poss = random.sample(range(1, len(Command_Specific_Data) + 1), l)
        except:
            poss = [random.randint(0,len(Command_Specific_Data))]
        pos = random.randint(0,len(Command_Specific_Data))
        if func == CHANGE.SINGLE_BYTE_CHANGE:
            Command_Specific_Data = CHANGE.SINGLE_BYTE_CHANGE(Command_Specific_Data,pos)
        elif func == CHANGE.MULTI_BYTE_CHANGE:
            Command_Specific_Data = CHANGE.MULTI_BYTE_CHANGE(Command_Specific_Data,poss)
        elif func == CHANGE.INC_ONE_BYTE_CHANGE:
            Command_Specific_Data = CHANGE.INC_ONE_BYTE_CHANGE(Command_Specific_Data,pos)
        elif func == CHANGE.INC_MULTI_BYTE_CHANGE:
            Command_Specific_Data = CHANGE.INC_MULTI_BYTE_CHANGE(Command_Specific_Data,poss)
        elif func == CHANGE.INC_CRAZY_BYTE_CHANGE:
            Command_Specific_Data = CHANGE.INC_CRAZY_BYTE_CHANGE(Command_Specific_Data,poss)
        
        Length = len(Command_Specific_Data)

        """
        Session_Handle
        较小概率改变; 保持不变可能更有效
        """
        prob = random.randint(0,65536)
        if prob % 17 == 13:
            Session_Handle = random.randint(0,0xFFFFFFFF)
            try:
                Session_Handle = random.randint(Session_Handle,0xFFFFFFFF)
                Session_Handle = random.randint(Session_Handle,0xFFFFFFFF)
            except:
                pass
        else:
            Session_Handle = int.from_bytes(Session_Handle)

        """
        Status
        同样的, 大概率选择KNOWN_STATUS里面的
        """
        prob = random.randint(0,65536)
        if prob % 17 == 1:
            Status = random.randint(0,0xFF) # 也是得看Status范围
        else:
            Status = random.choice(KNOWN_STATUS)

        """
        Sender_Context
        这个就纯随机了
        """
        Sender_Context = random.randint(0,0xFFFFFFFFFFFFFFFF)
        try:
            Sender_Context = random.randint(0,Sender_Context)
            Sender_Context = random.randint(Sender_Context,0xFFFFFFFFFFFFFFFF)
        except:
            pass
        
        """
        Options
        。。。:? 暂不清楚 都归零吧
        """
        Options = 0x0

        enip = ENIP_PACKET(
                            Command,Length,Session_Handle,
                            Status,Sender_Context,Options,Command_Specific_Data
                        )
        new_data = enip.PACK()
        """
        同样的, 适当变异发多倍长度
        """
        prob = random.randint(0,65536)
        if prob % 19 == 17:
            _new_data = new_data
            ls = [2,4,6,8]
            l = random.choice(ls)
            for i in range(l):
                try:
                    poss = random.sample(range(1, len(_new_data) + 1), l)
                except:
                    poss = [random.randint(0,len(_new_data))]
                pos = random.randint(0,len(data))
                if prob % 7 == 3:
                    new_data += CHANGE.MULTI_BYTE_CHANGE(_new_data,poss)
                else:
                    new_data += CHANGE.SINGLE_BYTE_CHANGE(_new_data,pos)

        return new_data
    except:
        return data

FUNCTIONS = [GENERAL_FUZZ_CHANGE]
# packet = ENIP_PACKET(1,2,3,4,5,6,7)
# print(packet)