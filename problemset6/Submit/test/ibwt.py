


def BWT_BWM(S):
    # create rotation matrix
    BWM = sorted([S[i:]+S[:i] for i in range(len(S))])
    # sort strings, concatenate last symbols
    return ''.join(r[-1] for r in sorted(BWM))

# Create a inverse Burrows-Wheeler transform of a string
# ANNB$AA
termchar = 17
def iBWT(BWT):
    orginal = bytearray()
    # create 2 lists, one for the BWT and one for the index
    BWT_list = list(BWT)
    index_list = list(range(len(BWT)))
    # sort the lists
    BWT_list, index_list = zip(*sorted(zip(BWT_list, index_list)))
    # get the index of the termchar
    index = BWT_list.index(termchar)
    # get the original message
    for i in range(len(BWT_list)):
        orginal.append(BWT_list[index])
        index = index_list[index]

    return orginal[1:]


arr = bytearray()
arr.append(65)
arr.append(78)
arr.append(78)
arr.append(66)
arr.append(17)
arr.append(65)
arr.append(65)
print(arr)
print(iBWT(arr))
