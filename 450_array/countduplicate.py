def countduplicate(s):
    breakpoint()
    k = {}
    for i in s:
        k[i] = k.get(i,0) + 1

    for w in k:
        if k[w] != 1:
            print(w,k[w])


countduplicate("adfdsfdsff")
            
           
