"""
主fuzz部分

TODO:
1. 加交叉功能码的fuzz(现在只是单个单个的测, 还应该考虑交叉的情况)
2. MAX_LEN选大点是否更好?
3. 稍微封装一下
4. 命令行传参数? (optional, 显得更Advanced一点 :) )
5. 
"""

import socket
import HASH.HASH_FUNC
import HASH.HASH_MAP
import CONFIG

def BFS(data:bytes,func):
    """
    use BFS to Fuzz
    """
    import time
    queue = []
    MAX_LEN = CONFIG.BFS_QUEUE_MAX_LEN
    cur = 0
    queue.append(data)
    time0 = time.time()
    while True:
        deltime = time.time() - time0
        if (deltime > CONFIG.BFS_DEL_TIME): # 这个根据情况调整(比如挂着跑就开大点)
            break
        if(len(queue) >= MAX_LEN):
            """
            本来想写循环队列的, 
            想了想, 不如这么随机sample一下, 说不定还能跳出当前局部, 达到更好的效果
            """
            import random
            queue = random.sample(queue,MAX_LEN >> 2)
            cur = 0
            # HASH.HASH_FUNC.HASHMAP.clear() # 不应该clear..
            pass
        print(f"\r[-] func : {func.__name__:<14} time : {deltime:.2f}s  "
              f"len of queue : {len(queue):<5}   cur : {cur}    total time : {time.time() - start_time:.2f}")
        try:
            top = queue[cur]
        except:
            break
        try:
            s = new_socket()
            s.send(PACK(top))
            # 保证modbus双方通信完成后再close, 同时close后, sleep保证close包发送完全.
            # 其实就是使得packet的req和rep中间不掺杂其他(如TCP)报文
            # 避免出现重传的包, 影响fuzz结果
            time.sleep(0.15)
            s.close()
            time.sleep(0.35)
        except:
            try:
                time.sleep(1)
                s = new_socket()
                s.send(PACK(top))
                s.close()
            except:
                print("\033[91m[+] MAYBE CRASHED!\033[0m")
                print(f"[*] CURRENT FUNC: {func}")
                print(f"[*] CURRENT TOP: {PACK(top)}")
                print(f"[*] CURRENT ORIGIN DATA: {PACK(data)}")
                exit()

        for i in range(16):
            newX = func(top)
            if HASH.HASH_FUNC.put(newX) == True:
                queue.append(newX)
        cur = (cur + 1) % MAX_LEN
        # time.sleep(0.5)

    pass

def new_socket():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((CONFIG.IP,CONFIG.PORT))
    # s.connect(("192.168.1.88",502))
    return s

if CONFIG.PROTOCOL == "MODBUS":
    import PACKET_DATA.MODBUS
    import VARIATION.MODBUS
    DATAS = PACKET_DATA.MODBUS.DATAS
    FUNCS = VARIATION.MODBUS.FUNCTIONS
    PACK = PACKET_DATA.MODBUS.PACK
elif CONFIG.PROTOCOL == "ETHERNETIP":
    import PACKET_DATA.ETHERNETIP
    import VARIATION.ETHERNETIP
    DATAS = PACKET_DATA.ETHERNETIP.DATAS
    FUNCS = VARIATION.ETHERNETIP.FUNCTIONS
    PACK = PACKET_DATA.ETHERNETIP.PACK
elif CONFIG.PROTOCOL == "OPCUA":
    import PACKET_DATA.OPCUA
    import VARIATION.OPCUA
    DATAS = PACKET_DATA.OPCUA.DATAS
    FUNCS = VARIATION.OPCUA.FUNCTIONS
    PACK = PACKET_DATA.OPCUA.PACK
    

import time
start_time = time.time()

while True:
    # for i in range(len(DATAS)):
    # 将遍历DATAS改为了随机;
    if(1):
        import random
        i = random.randint(0,len(DATAS)-1)
        if (i<len(FUNCS) and FUNCS[i]!=None and DATAS[i] != None):
            bfs = 1
        else:
            bfs = 0    
        bfs = 1
        if bfs:
            if CONFIG.PROTOCOL == "MODBUS":
                func = VARIATION.MODBUS.GENERAL_FUZZ_CHANGE
            elif CONFIG.PROTOCOL == "ETHERNETIP":
                func = VARIATION.ETHERNETIP.GENERAL_FUZZ_CHANGE
            elif CONFIG.PROTOCOL == "OPCUA":
                func = VARIATION.OPCUA.GENERAL_FUZZ_CHANGE
            BFS(DATAS[i],func)
        else:
            try:
                s = new_socket()
                s.send(PACK(DATAS[i]))
                s.close()
            except:
                    try:
                        import time
                        time.sleep(1)
                        s = new_socket()
                        s.send(PACK(DATAS[i]))
                        s.close()
                    except:
                        print("\033[91m[+] MAYBE CRASHED!\033[0m")
                        print(f"[*] CURRENT DATA: {PACK(DATAS[i])}")
                        exit()