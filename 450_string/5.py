def isrotation(s1,s2):
    str = s1+s1
    if s2 in str:
        return f'{s2} is rotation of {s1}'
    else:
        return f'{s2} is not rotation of {s1}'


print(isrotation('abcd','bcda'))
