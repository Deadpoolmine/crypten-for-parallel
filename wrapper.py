#!/usr/bin/python3
import multiprocessing
import os, sys 
import time
from multiprocessing import Pool
import torch

from common import build_fpath



def wrapper(uid):
    cmd = 'python3 sort_enc.py ' + str(uid)
    print(cmd)
    os.system(cmd)

def parallel(unum):
    with Pool(processes=multiprocessing.cpu_count()) as pool:
        for uid in range(unum):
            pool.apply_async(wrapper, (uid,))
        pool.close()
        pool.join()

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
    unum = 10                           # total user number
    dnum = 10000                        # data for each user
    
    data = torch.rand(unum, dnum)       # emulate data for all users
    torch.save(data, build_fpath(None, "original"))
    
    data = torch.load(build_fpath(None, "original"))

    for uid in range(unum):
        torch.save(data[:uid], build_fpath(uid))
    
    parallel(unum)

main()
