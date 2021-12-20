#!/usr/bin/python3
import multiprocessing
from pickle import TRUE
import threading
import os, sys 
import time
from multiprocessing import Pool
import torch
import socket

from torch.functional import Tensor               
from common import *

client_cnt = 0
server = socket.socket()  
server.bind((HOST, PORT)) 
server.listen(5)
server_thread = ""
results = {}

def wrapper(uid):
    cmd = 'python3 sort_enc.py ' + str(uid)
    print(cmd)
    os.system(cmd)

def send(client: socket.socket, info, data, uid):
    global results

    length = len(data[:, 1])
    num_iter = 0
    client.send(length.to_bytes(8, "little", signed=False))
    while length > 0:
        if length >= 1024:
            data_iter:Tensor = data[num_iter * 1024 : (num_iter + 1) * 1024, uid]
        else:
            data_iter:Tensor = data[-length-1:, uid]
        client.send(longlist2bytes(data_iter.tolist()))
        length -= MAX_PACKET_LENGTH
        num_iter += 1

    res0 = []
    res1 = []
    length = 2 * len(data[:, 1])
    while length > 0:
        msg = client.recv(1024 * 8)
        msg_list = longbytes2list(msg)
        rank = int(msg_list[0])
        if rank == 0:
            res0.extend(msg_list[1:])
        else:
            res1.extend(msg_list[1:])
        length -= len(msg_list[1:])

    results[str(uid) + '-0'] = res0
    results[str(uid) + '-1'] = res1
     

def start_server(data, unum):
    client_cnt = 0

    while True:
        if client_cnt == unum:
            break
        client, info = server.accept()  # block
        bytes = client.recv(4)
        uid = int.from_bytes(bytes, byteorder="little", signed=False)
        print(uid)
        thread = threading.Thread(target=send, args=((client, info, data, uid, )))
        thread.start()
        client_cnt += 1

def parallel(unum):
    # with Pool(processes=multiprocessing.cpu_count()) as pool:
    global server_thread
    with Pool(multiprocessing.cpu_count()) as pool:
        for uid in range(unum):
            pool.apply_async(wrapper, (uid,))
        pool.close()
        pool.join()
        server_thread.join()
        for key, value in results.items():
            print("=============================")
            print("\nKey: " + key)
            print(value)


def serial(unum):
    for uid in range(unum):
        wrapper(uid)

def run_test(func, runtimes):
    times = []
    final = 0
    for i in range(runtimes):
        start = time.time()
        func()
        end = time.time()
        times.append(end - start)
    for t in times:
        final += t
    final /= float(runtimes)
    print("Run Time: %f" % (final))

def main():
    global server_thread

    unum = 10                           # total user number
    dnum = 10                           # data for each user
    
    data = torch.randint(-10000, 10000, (unum, dnum))       # emulate data for all users
    torch.save(data, build_fpath(None, "original"))
    
    data = torch.load(build_fpath(None, "original"))

    for uid in range(unum):
        torch.save(data[:, uid], build_fpath(uid))
    
    server_thread = threading.Thread(target=start_server, args=((data, unum)))
    server_thread.start()

    parallel(unum)
    
main()
