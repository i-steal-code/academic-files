#!/usr/bin/env python3
"""Simplify S&S.ipynb code comments — keep original meaning, concise."""

import json
from pathlib import Path

path = Path("computing practical/computing practical all boilerplates/S&S.ipynb")
nb = json.loads(path.read_text(encoding="utf-8"))


def set_src(cell, text):
    lines = text.split("\n")
    cell["source"] = [ln + "\n" for ln in lines[:-1]] + (
        [lines[-1] + "\n"] if lines[-1] != "" or text.endswith("\n") else []
    )


set_src(
    nb["cells"][1],
    """def Fact(n):
    # base: 0! / 1! = 1
    if n <= 1:
        return 1
    return n * Fact(n - 1)

def Sum1toN(n):
    # base: sum to 0 is 0
    if n <= 0:
        return 0
    return n + Sum1toN(n - 1)

def ReverseString(s):
    # base: empty or single char
    if len(s) <= 1:
        return s
    # last char + reverse of the rest
    return s[-1] + ReverseString(s[:-1])
""",
)

set_src(
    nb["cells"][3],
    """# random test list of length n
import random
def reset_test_list():
    global test_list
    test_list = []
    n = 10
    lower_bound = 0
    upper_bound = n
    for i in range(n):
        test_list.append(random.randint(lower_bound, upper_bound))
    print(f"test list: {test_list}")
reset_test_list()
""",
)

set_src(
    nb["cells"][5],
    """def LinearSearch(Arr, FindValue):
    for i in range(len(Arr)):
        if Arr[i] == FindValue:
            return i  # first match index
    return -1  # not found
""",
)

set_src(
    nb["cells"][7],
    """# recursive binary search
def BinarySearch(Arr, FindValue, Low, High):
    # empty window — absent
    if Low > High:
        return -1
    middle = (Low + High) // 2  # mid index of current window
    if Arr[middle] == FindValue:
        return middle  # found
    elif FindValue < Arr[middle]:
        # go left: discard middle and right
        return BinarySearch(Arr, FindValue, Low, middle - 1)
    else:
        # go right: discard middle and left
        return BinarySearch(Arr, FindValue, middle + 1, High)
# ±1 drops middle — already checked, not in the remaining region

# iterative binary search — same decisions, loop instead of call stack
def BinarySearchIterative(Arr, FindValue, Low, High):
    while Low <= High:  # until window empty
        middle = (Low + High) // 2
        if Arr[middle] == FindValue:
            return middle
        elif FindValue < Arr[middle]:
            High = middle - 1  # move left
        else:
            Low = middle + 1  # move right
    return -1  # bounds crossed — not in list
""",
)

set_src(
    nb["cells"][9],
    """# hashing with separate chaining (LLM-written early 2025; prefer ADT.ipynb HashTable)
BUCKET_SIZE = 7
class Hash(object):
    def __init__(self, bucket):
        self.__bucket = bucket  # number of buckets
        self.__table = [[] for _ in range(bucket)]  # one list per bucket

    def hashFunction(self, key):
        return (key % self.__bucket)

    def insertItem(self, key):
        index = self.hashFunction(key)
        self.__table[index].append(key)

    def deleteItem(self, key):
        index = self.hashFunction(key)
        if key not in self.__table[index]:
            return
        self.__table[index].remove(key)

    def displayHash(self):
        for i in range(self.__bucket):
            print("[%d]" % i, end='')
            for x in self.__table[i]:
                print(" --> %d" % x, end='')
            print()


# drive
if __name__ == "__main__":
    reset_test_list()
    h = Hash(BUCKET_SIZE)
    for x in test_list:
        h.insertItem(x)
    h.deleteItem(x)  # deletes last inserted x from the loop
    h.displayHash()
""",
)

set_src(
    nb["cells"][11],
    """def InsertionSort(Arr):
    for i in range(1, len(Arr)):
        current = Arr[i]  # next item from unsorted portion
        j = i - 1
        # shift larger sorted items right until insertion spot found
        while j >= 0 and Arr[j] > current:
            Arr[j + 1] = Arr[j]  # shift right; leaves a hole behind
            j -= 1  # walk left
        # j stepped one past the spot, so hole is at j+1
        Arr[j + 1] = current  # drop into sorted portion
    return Arr
""",
)

set_src(
    nb["cells"][13],
    """def BubbleSort(Arr):
    n = len(Arr)
    swapped = True
    while swapped:
        swapped = False
        for i in range(n - 1):  # one pass over adjacent pairs
            if Arr[i] > Arr[i + 1]:  # pair out of order — swap
                temp = Arr[i]
                Arr[i] = Arr[i + 1]
                Arr[i + 1] = temp
                swapped = True  # something moved; need another pass
        # full pass with no swaps → already sorted
    return Arr
""",
)

set_src(
    nb["cells"][15],
    """def partition(arr, first, last):
    pivotvalue = arr[first]  # first value is pivot
    leftmark = first + 1
    rightmark = last
    done = False
    while not done:  # until marks cross (rightmark < leftmark)
        # bounds check before arr[...] — avoids IndexError
        while leftmark <= rightmark and arr[leftmark] <= pivotvalue:
            # move right until > pivot or marks meet
            leftmark += 1
        while rightmark >= leftmark and arr[rightmark] >= pivotvalue:
            # move left until < pivot or marks meet
            rightmark -= 1
        if rightmark < leftmark:
            done = True  # crossed — stop swapping
        else:
            # swap the two misplaced values
            temp = arr[leftmark]
            arr[leftmark] = arr[rightmark]
            arr[rightmark] = temp
    # park pivot at rightmark (final sorted index)
    arr[first] = arr[rightmark]
    arr[rightmark] = pivotvalue
    return rightmark  # split for the two halves

def quickSort(array, first, last):
    if first < last:
        split = partition(array, first, last)  # pivot fixed at split
        quickSort(array, first, split - 1)  # left half
        quickSort(array, split + 1, last)  # right half
    return array
""",
)

set_src(
    nb["cells"][18],
    """def merge(array, low, mid, high):
    # copy the two halves (same array still holds both sections)
    left = array[low : mid + 1]
    right = array[mid + 1 : high + 1]
    # left/right are already sorted runs from earlier merges
    # copies mean this merge is NOT in-place
    l = 0  # front of left
    r = 0  # front of right
    a = low  # write-back index into array
    # take smaller head until one run empties
    while l < len(left) and r < len(right):
        if left[l] <= right[r]:
            array[a] = left[l]
            l += 1
        else:
            array[a] = right[r]
            r += 1
        a += 1
    # drain leftovers
    while l < len(left):
        array[a] = left[l]
        l += 1
        a += 1
    while r < len(right):
        array[a] = right[r]
        r += 1
        a += 1
    return array  # merged sorted range [low..high]

def mergeSort(array, low, high):
    if low < high:  # single element already sorted
        # divide
        mid = (low + high) // 2  # same mid idea as binary search
        mergeSort(array, low, mid)  # left half
        mergeSort(array, mid + 1, high)  # right half
        # conquer — merge on the way back up the call stack
        merge(array, low, mid, high)
    return array  # always the same array object, sorted in its range
""",
)

set_src(
    nb["cells"][20],
    """# scaffold — run definition cells above first
reset_test_list()
print("linear:", LinearSearch(test_list, test_list[0]))

sorted_for_binary = sorted(test_list[:])  # binary needs sorted input
print("binary on", sorted_for_binary, "->", BinarySearch(sorted_for_binary, test_list[0], 0, len(sorted_for_binary) - 1))
print("binary iterative ->", BinarySearchIterative(sorted_for_binary, test_list[0], 0, len(sorted_for_binary) - 1))
print("binary miss ->", BinarySearch(sorted_for_binary, -1, 0, len(sorted_for_binary) - 1),
      BinarySearchIterative(sorted_for_binary, -1, 0, len(sorted_for_binary) - 1))

a = test_list[:]
print("insertion:", InsertionSort(a))

b = test_list[:]
print("bubble:", BubbleSort(b))

c = test_list[:]
print("quick:", quickSort(c, 0, len(c) - 1))

d = test_list[:]
print("merge:", mergeSort(d, 0, len(d) - 1))
""",
)

path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
print("updated comment style in S&S.ipynb")
