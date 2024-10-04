"""
主fuzz部分

TODO:
1. 加交叉功能码的fuzz(现在只是单个单个的测, 还应该考虑交叉的情况)
2. MAX_LEN选大点是否更好?
3. 
"""

import socket
import PACKET_DATA
import PACKET_DATA.MODBUS
import VARIATION
import VARIATION.MODBUS

def BFS(data:bytes,func):
    """
    use BFS to Fuzz
    """
    import time
    queue = []
    MAX_LEN = 65536
    cur = 0
    queue.append(data)
    time0 = time.time()
    while True:
        deltime = time.time() - time0
        if (deltime > 600): # 这个根据情况调整(比如挂着跑就开大点)
            break
        if(len(queue) >= MAX_LEN):
            """
            本来想写循环队列的, 
            想了想, 不如这么随机sample一下, 说不定还能跳出当前局部, 达到更好的效果
            """
            import random
            queue = random.sample(queue,1024)
            cur = 0
            pass
        print(f"\r[-] func : {func.__name__:<14} time : {deltime:.2f}s  "
              f"len of queue : {len(queue):<5}   cur : {cur}")
        top = queue[cur]
        try:
            s = new_socket()
            s.send(PACK(top))
            s.close()
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
            queue.append(newX)
        cur = (cur + 1) % MAX_LEN
        time.sleep(0.25)

    pass

def new_socket():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(("192.168.1.88",502))
    return s

DATAS = PACKET_DATA.MODBUS.DATAS
FUNCS = VARIATION.MODBUS.FUNCTIONS
PACK = PACKET_DATA.MODBUS.PACK

while True:
    for i in range(len(DATAS)):
        if (i<len(FUNCS) and FUNCS[i]!=None):
            bfs = 1
        else:
            bfs = 0    
        if bfs:
            BFS(DATAS[i],FUNCS[i])
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