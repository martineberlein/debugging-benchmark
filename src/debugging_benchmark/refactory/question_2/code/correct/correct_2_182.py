def unique_day(day, possible_birthdays):
    a = 0
    for i in range(len(possible_birthdays)):
        if day == possible_birthdays[i][1]:
            a += 1
    if a == 1:
        return True
    else:
        return False

def unique_month(month, possible_birthdays):
    a = 0
    for i in range(len(possible_birthdays)):
        if month == possible_birthdays[i][0]:
            a += 1
    if a == 1:
        return True
    else:
        return False

def contains_unique_day(month, possible_birthdays):
    for i in range(len(possible_birthdays)):
        if month == possible_birthdays[i][0]:
            if unique_day(possible_birthdays[i][1], possible_birthdays) == True:
                return True
    else:
        return False
