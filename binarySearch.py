""" BINARY SEARCH """

def binarysearch(arr, l, r, f):
    if r>=l:
        print("left and right : %d %d" %(l,r))
        mid = l + (r - l) / 2
        mid = int(mid)
        print(mid)
        if arr[mid] == f:
            return mid
        elif arr[mid] > f:
            print("Samller")
            print(l, mid-1)
            return binarysearch(arr, l, mid-1, f)
        else:
            print("Bigger")
            print(mid+1,r)
            return binarysearch(arr, mid+1, r, f)
    else:
        return -1

a = [1,2,3,4,5]
x = 4
result = binarysearch(a, 0, len(a)-1, x)

if result != -1:
    print("Element present at the index : %d" %result)
else:
    print("Element is not present ... !!!")