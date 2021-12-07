import numpy as np
import time 

def bitonicSort(A, direction):
    n = len(A)
    if n <= 1:
        return A
    else:
        first = bitonicSort(A[:(n//2)], True)
        second = bitonicSort(A[(n//2):], False)
        return bitonicMerge(first + second, direction)

def bitonicMerge(A, direction):
    n = len(A)
    if n == 1:
        return A
    else:
        bitonicCompandSwap(A, direction)
        first = bitonicMerge(A[:(n//2)], direction)
        second = bitonicMerge(A[(n//2):], direction)
        ans = first + second
        return ans

def bitonicCompandSwap(A, direction):
    k = len(A) // 2
    for i in range(k):
        if (A[i] > A[i+k]) == direction:
            A[i], A[i+k] = A[i+k], A[i]

def sort(A):
    return bitonicSort(A, True)

#A = [3, 7, 4, 8, 6, 2, 1, 5]
A = list(np.random.randint(1,400000,8192))
start = time.time()
ans = sort(A)
end = time.time()
print(end - start, "s")