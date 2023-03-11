def leftnegative(arr):
    left = 0
    right = len(arr)-1
    while left <= right:
        if arr[left] < 0:
            left += 1
        elif arr[left] > 0 and arr[right] < 0:
            arr[left],arr[right] = arr[right],arr[left]
            left += 1
            right -= 1
        elif arr[left] > 0 and arr[right] > 0:
            right -= 1
    return arr
            
print(leftnegative([-2,-3,5,6,-2,8,-3]))

