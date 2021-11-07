import time
import numpy as np

l=list(range(3000))
def func1(x):
    x = (x**2)**2**2
    return x

def func2(x):
    x = (x**2)**2**2
    return x

def func3(x):
    global l
    return np.array(list(map(func2, l)))

def func4(x):
    f = []
    for num in range(3000):
        f.append(func1(num))
    return f

lists = list(range(3000))

start = time.time()
a=[]

for n in lists:
    f = []
    for num in range(3000):
        f.append(func1(num))
    a.append(f)
end = time.time()
print('Serial computing time:\t',end - start)

start = time.time()
g=np.array(list(map(func4,lists)))
end = time.time()

# print(a == g)
print('Parallel Computing time:\t',end - start)
print(a[0])
print(g.shape)

