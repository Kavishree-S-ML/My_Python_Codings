""" FIBONACCI SERIES """
print("**** FIBONACCI SERIES ****")

class Fibonacci:
    def __init__(self):
        self.a = "HAi"
    def fib(self, n):
        if n == 0: return 0
        elif n == 1: return 1
        else: return self.fib(n - 1) + self.fib(n - 2)

n = int(input("Enter the limit : "))
i = 0
f = Fibonacci()
while i < n:
    print f.fib(i),
    i += 1
print "\nComplete List of Attributes : ",dir(f)
print getattr(f, 'a')
print getattr(f, 'fib')