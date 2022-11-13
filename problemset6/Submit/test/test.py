from functools import partial

termchar = 17

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
            
# memory efficient BWT
def bwt(msg):
    def bw_key(text, value, step):
        return text[(value + step) % len(text)]

    msg = msg + termchar.to_bytes(1, byteorder='big')

    bwtM = bytearray()

    rs = radix_sort(range(len(msg)), partial(bw_key, msg))
    for i in rs:
        bwtM.append(msg[i - 1])

    return bwtM[::-1] 

def ibwt(msg):
    orginal = bytearray()
    # create 2 lists, one for the BWT and one for the index
    BWT_list = list(msg)
    index_list = list(range(len(msg)))
    # sort the lists
    BWT_list, index_list = zip(*sorted(zip(BWT_list, index_list)))
    # get the index of the termchar
    index = BWT_list.index(termchar)
    # get the original message
    for i in range(len(BWT_list)):
        orginal.append(BWT_list[index])
        index = index_list[index]

    return orginal[1:]

arr = 'I like to eat apples and bananas'
arr = arr.encode()
arr = bytearray(arr)

print(ibwt(bwt(arr)))
# print(ibwt(arr))
# how to sort dictionary by values
s = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}
print(sorted(s.items(), key=lambda x: x[1]))


