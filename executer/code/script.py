def fib(n):
    ns = [0,1]
    for i in range(0, n):
        if i % 2 == 0:
            ns[0] = ns[1]+ns[0]
        else:
            ns[1] = ns[1]+ns[0]
    if n % 2 == 0:
        return(ns[0])
    return(ns[1])

print(fib(int(input())))