from functools import partial
termchar = 17

def bwt(msg):
    def bw_key(text, value, step):
        return text[(value + step) % len(text)]

    msg = msg + termchar.to_bytes(1, byteorder='big')

    bwtM = bytearray()

    rs = radix_sort(range(len(msg)), partial(bw_key, msg))
    for i in rs:
        bwtM.append(msg[i - 1])

    return bwtM[::-1] 

def radix_sort(values, key, step=0):
    sortedvals = []
    radix_stack = []
    radix_stack.append((values, key, step))

    while len(radix_stack) > 0:
        values, key, step = radix_stack.pop()
        if len(values) < 2:
            for value in values:
                sortedvals.append(value)
            continue

        bins = {}
        for value in values:
            bins.setdefault(key(value, step), []).append(value)

        for k in sorted(bins.keys()):
            radix_stack.append((bins[k], key, step + 1))
    return sortedvals


def ibwt(msg):
    
    last_col = [[msg[i], i] for i in range(len(msg))]
    first_col = sorted(last_col, key=lambda x: x[0])
    for i in range(len(msg)):
        if last_col[i][0] == termchar:
            index = i
    og = bytearray()
    for i in range(len(msg)):
        og.append(first_col[index][0])
        index = first_col[index][1]

    return og[:-1]
            
print(ibwt(bwt(b'BANANA')))