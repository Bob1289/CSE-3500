# removeDuplicates using for loop

def removeDuplicates(list):
    newList = []
    for i in list:
        if i not in newList:
            newList.append(i)
    return newList