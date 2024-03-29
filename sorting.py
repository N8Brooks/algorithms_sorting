# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 14:05:22 2019

@author: DSU
"""

def bubbleSort(arr): 
    # traverse through all array elements 
    for i in range(len(arr)): 
        # last i elements are already in place 
        for j in range(0, len(arr)-i-1): 
            # traverse the array from 0 to n-i-1 
            # Swap if the element found is greater 
            # than the next element 
            if arr[j] > arr[j+1] : 
                arr[j], arr[j+1] = arr[j+1], arr[j] 

def insertionSort(arr): 
    # traverse through 1 to len(arr) 
    for i, key in enumerate(arr[1:], start=1): 
        # move elements of arr[0..i-1], that are 
        # greater than key, to one position ahead 
        # of their current position 
        j = i - 1
        while j >= 0 and key < arr[j] : 
                arr[j + 1] = arr[j] 
                j -= 1
        arr[j + 1] = key

def mergeSort(arr): 
    if len(arr) >1: 
        mid = len(arr) // 2 #Finding the mid of the array 
        L = arr[:mid]       # Dividing the array elements  
        R = arr[mid:]       # into 2 halves 
  
        mergeSort(L)        # Sorting the first half 
        mergeSort(R)        # Sorting the second half 
  
        i = j = k = 0
          
        # copy data to temp arrays L[] and R[] 
        while i < len(L) and j < len(R): 
            if L[i] < R[j]: 
                arr[k] = L[i] 
                i+=1
            else: 
                arr[k] = R[j] 
                j+=1
            k+=1
          
        # checking if any element was left 
        while i < len(L): 
            arr[k] = L[i] 
            i+=1
            k+=1
          
        while j < len(R): 
            arr[k] = R[j] 
            j+=1
            k+=1

def partition(arr, low, high): 
    i = (low - 1)         # index of smaller element 
    pivot = arr[high]     # pivot 
  
    for j in range(low , high): 
        # ff current element is smaller than the pivot 
        if   arr[j] < pivot:
            # increment index of smaller element 
            i = i+1 
            arr[i],arr[j] = arr[j],arr[i] 
  
    arr[i+1],arr[high] = arr[high],arr[i+1] 
    return ( i+1 ) 

def quickSortWorker(arr, low, high): 
    if low < high: 
        # pi is partitioning index, arr[p] is now 
        # at right place 
        pi = partition(arr,low,high) 
        
        # Separately sort elements before 
        # partition and after partition 
        quickSortWorker(arr, low, pi-1) 
        quickSortWorker(arr, pi+1, high) 

def quickSort(arr):
    return quickSortWorker(arr, 0, len(arr) - 1)

def quickSortNaiveWorker(arr):
    # Base case 
    if len(arr) <= 1: return arr
    
    # Let us choose first element as pivot 
    else: 
        mid = 0
        pivot = arr[0] 
  
        # key element is used to break the array 
        # into 2 halves according to their values 
        smaller,greater = [],[] 
   
        # Put greater elements in greater list, 
        # smaller elements in smaller list. Also, 
        # compare positions to decide where to put. 
        for indx, val in enumerate(arr): 
            if indx != mid: 
                if val < pivot: 
                    smaller.append(val) 
                elif val > pivot: 
                    greater.append(val) 
  
                # If value is same, then considering 
                # position to decide the list. 
                else: 
                    if indx < mid: 
                        smaller.append(val) 
                    else: 
                        greater.append(val) 
        
        return quickSortNaiveWorker(smaller)+[pivot]+\
                    quickSortNaiveWorker(greater) 

def quickSortNaive(arr):
    for i, x in enumerate(quickSortNaiveWorker(arr)):
        arr[i] = x

# python's built in sorting function (way faster since it's written in c)
def timSort(arr):
    arr.sort()

# the worst algorithm I could think of - only added for reference
def facSort(arr):
    from itertools import permutations
    for arr1 in permutations(arr, len(arr)):
        if all(a <= b for a, b in zip(arr1, arr1[1:])):
            return arr1

# list of all sorting functions
algorithms = [bubbleSort, insertionSort, mergeSort, quickSort, quickSortNaive,\
              timSort]

"""
correctness tests section
driver code to make sure all sorting functions work
"""
if __name__ == '__main__':
    from random import sample
    from tqdm import trange
    
    # verifies a list is sorted
    def verifySorted(arr):
        return all(a <= b for a, b in zip(arr, arr[1:]))
    
    # returns True iff the algorithm sorts the function
    def checkSortCorrectness(algorithm, arr, verbose):
        arr_copy = arr.copy()   # don't change original array
        algorithm(arr_copy)
        if verbose: print(f'{algorithm.__name__}:\t{arr_copy}')
        return verifySorted(arr_copy)
    
    # checks each algorithm for correctness
    def checkAlgorithms(arr, verbose=False):
        if verbose: print(f'unsorted:\t{arr_original}')
        for algo in algorithms:
            assert checkSortCorrectness(algo, arr, verbose)
    
    # Check algorithms visually with small list
    print('Check visually:')
    arr_original = [1,3,6,7,8,2,9,4,5]
    checkAlgorithms(arr_original, verbose=True)
    
    # check with BIG lists several times
    print('\nChecking algorithmically:')
    for i in trange(10):
        arr_original = sample(range(int(-2e9), int(2e9)), 1000)
        checkAlgorithms(arr_original)
    
    # all algorithms correctly sorted the list
    print('\nAll algorithms correctly sorted the lists.')
