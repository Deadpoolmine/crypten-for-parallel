import torch
import multiprocessing
from multiprocessing.pool import Pool

import sys
import os 
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../../')))
import crypten
import crypten.mpc as mpc
import crypten.communicator as comm
from common import build_fpath

def compare_and_swap_joint(i, j, arr1, arr2 = None, isAsc = True):
    ''' arr1: sort by this array
        arr2: idx for arr1
        isAsc: True if ascending 
    '''
    b = (arr1[i] < arr1[j])
    smaller = b * arr1[i] + (1 - b) * arr1[j]
    larger = arr1[i] + arr1[j] - smaller

    if arr2 is not None:
        smaller2 = b * arr2[i] + (1 - b) * arr2[j]
        larger2 = arr2[i] + arr2[j] - smaller2

    if isAsc:   # ascending
        arr1[i], arr1[j] = smaller, larger
        if arr2 is not None:
            arr2[i], arr2[j] = smaller2, larger2
    else:
        arr1[i], arr1[j] = larger, smaller
        if arr2 is not None:
            arr2[i], arr2[j] = larger2, smaller2


# ============================== bitonic sort ==============================
def bitonic_sort(arr1, left, length, arr2 = None, isAsc = True):
    ''' sort arr1, arr2 is idx array
        When firstly call bitonic sort, left=0，length=len(arr1)
    '''
    if length > 1:
        m = int(length / 2)
        bitonic_sort(arr1, left, m, arr2, not isAsc)
        bitonic_sort(arr1, left + m, length - m, arr2, isAsc)
        bitonic_merge(arr1, left, length, arr2, isAsc)


def bitonic_merge(arr1, low, length, arr2 = None, isAsc = True):
    ''' assume arr1 is a bitonic sequence '''
    if length > 1:
        m = greatestPowerOfTwoLessThan(length)
        for i in range(low, low + length - m):
            compare_and_swap_joint(i, i + m, arr1, arr2, isAsc)

        bitonic_merge(arr1, low, m, arr2, isAsc)
        bitonic_merge(arr1, low + m, length - m, arr2, isAsc)
 
def greatestPowerOfTwoLessThan(n):
    ''' n may not be the power of 2 '''
    k = 1
    while (k > 0) and (k < n):
        k = k << 1
    return k >> 1


# @mpc.run_multiprocess(world_size=2)
# def test_bitonic_sort(): 
#     data1 = crypten.cryptensor(torch.tensor([200, 40.5, 31, 555, 6.4, 1.10, 777, 80, 9.3, 10]))
     
#     data2 = crypten.cryptensor(torch.tensor([2, 4, 3, 5, 6, 1, 7, 8, 9, 10]))
     
#     print(str(comm.get().get_rank()), data1)
     
#     length = len(data1)
 
#     arr1 = data1.clone()
#     arr2 = data2.clone()
#     bitonic_sort(arr1, 0, length, arr2, True)
#     print("joint bitonic sort arr1 and arr2\n")
#     print(arr1.get_plain_text(), "\n")
#     print(arr2.get_plain_text(), "\n")

   
# @mpc.run_multiprocess(world_size=2)
# def parellel_sort(data1, row, col):   
#     arr1_enc = crypten.cryptensor(data1)  
#     print("CPU count", multiprocessing.cpu_count())
#     with Pool(multiprocessing.cpu_count()) as pool:  
#         # deadlock here! 
#         pool.starmap(bitonic_sort, [(arr1_enc[:, i], 0, row) for i in range(col)])
        
#     print(arr1_enc.get_plain_text()) 

@mpc.run_multiprocess(world_size=2)
def user_bitonic_sort(uid, userdata):
    crypto_data = crypten.cryptensor(userdata)
    length = len(crypto_data)
    bitonic_sort(crypto_data, 0, length, None, True)
    torch.save(crypto_data.get_plain_text(), build_fpath(uid, "user-sorted"))

uid = int(sys.argv[1])                          # get user id
userdata = torch.load(build_fpath(uid))    # get user data

crypten.init()                                  # initialize crypten for each instance
user_bitonic_sort(uid, userdata)
crypten.uninit()
