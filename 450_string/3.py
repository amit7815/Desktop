def find_Duplcate(s):
    d  = {}
    for i in s:
        d[i] = d.get(i,0) + 1

    for i in d:
        if d[i] > 1:
            print(i,d[i])


find_Duplcate('geeks for geeks')
