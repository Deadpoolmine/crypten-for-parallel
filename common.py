ORIGINAL_DATA_PATH_PREFIX="./data/original/original-data"
USER_DATA_PATH_PREFIX="./data/user/user-data"
USER_SORTED_DATA_PATH_PREFIX="./data/user-sorted/user-sorted-data"

MAX_PACKET_LENGTH=1024
MSG_END="Good Bye"

HOST = "127.0.0.1"
PORT = 12346

def build_fpath(uid=None, type="user"):
    if type == "original":
        return ORIGINAL_DATA_PATH_PREFIX
    elif type == "user":
        return USER_DATA_PATH_PREFIX + "-" + str(uid)
    elif type == "user-sorted":
        return USER_SORTED_DATA_PATH_PREFIX + "-" + str(uid)


def longlist2bytes(array):
    a = b''
    for i in array:
        bytes = i.to_bytes(8, byteorder="little", signed=True) 
        a += bytes
    return a

def longbytes2list(arrayb):
    list = []
    length = len(arrayb)
    i = 0
    while length > 0:
        bytes = arrayb[i : i + 8]
        long = int.from_bytes(bytes, "little", signed=True)
        length -= 8
        i += 8
        list.append(long)
    # print(list)
    return list