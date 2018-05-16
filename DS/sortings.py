"""
    SORTING ALGORITHMS

    METHODS: Bubble, Insertion, Quick, Selection, Merge
"""

def bubbleSort(arr):
    for i in range(0, len(arr)):
        if (i + 1) < (len(arr) - 1) and arr[i] > arr[i + 1]:
            arr[i], arr[i+1] = arr[i+1], arr[i]
    return arr


def insertionSort(arr):
    for i in range(0, len(arr) - 1):
        for j in range(i, len(arr)):
            if arr[i] > arr[j]:
                temp = arr[i]
                arr[i] = arr[j]
                arr[j] = temp
    return arr


def selectionSort(arr):
    for i in range(0, len(arr)):
        min_indx = i
        for j in range(i, len(arr)):
            if arr[i] > arr[j]:
                min_indx = j
        arr[i], arr[min_indx] = arr[min_indx], arr[i]
    return arr

def quickSort(arr):
    if len(arr) <= 1: return arr
    else:
        return quickSort([x for x in arr[1:] if x<arr[0]]) + [arr[0]] + quickSort([x for x in arr[1:] if x>=arr[0]])

a = [5, 2, 4, 8, 1]
print "Insertion Sort : %s" % str(insertionSort(a))
print "Bubble Sort : %s" % str(bubbleSort(a))
print "Selection Sort : %s" % str(selectionSort(a))
print "Quick Sort : %s" % str(quickSort(a))