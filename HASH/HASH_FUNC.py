HASHMAP = []
MAX_LEN = 65536 << 2 # 存储空间考量

def ROL32(x,r):
    return ((x << r) | (x >> (32 - r))) & 0xFFFFFFFF

def hash(x:bytes):
    try:
        import hashlib
        _md5 = hashlib.md5(x).hexdigest().encode()
        _hash = hashlib.sha3_512(_md5).hexdigest().encode()
        _hash = _hash[:16]
        return _hash
    except:
        return b'\xba\xde\xff'
def put(x:bytes):
    global HASHMAP
    if (len(HASHMAP) > MAX_LEN):
        HASHMAP = HASHMAP[MAX_LEN//2:]
    _hash = hash(x)
    if Is_Repeat(_hash):
        return False
    else:
        HASHMAP.append(_hash)
        return True


def Is_Repeat(hash:bytes):
    if HASHMAP.count(hash) != 0:
        return True
    return False