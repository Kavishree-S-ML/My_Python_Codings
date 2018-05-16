"""
    MERGE SORT ALGORITHM
"""


def merge(a, b):
    c = []

    while len(a)!=0 and len(b)!=0:
        if a[0] < b[0]:
            c.append(a[0])
            a.remove(a[0])
        else:
            c.append(b[0])
            b.remove(b[0])
    if len(a) != 0: c += a
    else: c += b

    return c

def mergeSort(arr):
    if len(arr) <= 1: return arr
    else:
        mid = len(arr)/2
        a = mergeSort(arr[:mid])
        b = mergeSort(arr[mid:])
        return merge(a,b)


print "Merge Sort : %s" % str(mergeSort([3,6,1,2,8,0]))