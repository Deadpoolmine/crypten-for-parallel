#!/usr/bin/python3
import os
import time
from multiprocessing import Pool

def wrapper():
    os.system('python3 sort_enc.py')

def parallel():
    with Pool(processes=4) as pool:
        for i in range(4):
            pool.apply_async(wrapper, ())
        pool.close()
        pool.join()

def serial():
    for i in range(4):
        wrapper()

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


# run_test(parallel, 5) 7.66s

# run_test(serial, 5)   8.422829s
