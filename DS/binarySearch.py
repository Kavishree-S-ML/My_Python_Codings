""" BINARY SEARCH """


def binarysearch(arr, l, r, f):
    if r >= l:
        mid = l + (r - l) / 2
        mid = int(mid)
        if arr[mid] == f:
            return mid
        elif arr[mid] > f:
            return binarysearch(arr, l, mid - 1, f)
        else:
            return binarysearch(arr, mid + 1, r, f)
    else:
        return -1


a = [1, 2, 3, 4, 5]
print "Element : %s" % str(a)
x = int(input("Enter the Element to search : "))
result = binarysearch(a, 0, len(a) - 1, x)

if result != -1:
    print("Element present at the index : %d" % result)
else:
    print("Element is not present ... !!!")
