def remove_extras(lst):
    list = []
    for i in lst:
        if i not in list:
            list.append(i)
    return list
