n = int(input("enter no of elements"))
a = list(map(int,input("enter the numbers").strip().split()))[:n]
i,j = 0,len(a)-1
while i<j:
    a[i],a[j]=a[j],a[i]
    i+=1
    j-=1

print(f"after reversing array is {a}")




#x,y = input("enter two numbers").split(" ")
