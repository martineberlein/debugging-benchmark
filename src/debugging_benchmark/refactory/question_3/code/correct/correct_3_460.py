def remove_extras(lst):
    new_list = []
    for number in lst:
       if number not in new_list:
           new_list.append(number)
    return new_list
