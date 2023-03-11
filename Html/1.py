def getMinimumCost(arr):
	sum_arr = []
	for i in arr:
		if i >= 0 and i != max(arr):
			sum_arr.append(i)

	

	if sum_arr[0] == 0:
		for i in range(1, len(arr)):
			if sum_arr[i] > 0:
				sum_arr[0] , sum_arr[i] = sum_arr[i], sum_arr[0]
				break

	sum_arr.append(max(arr))

	for j in arr:
		if j < 0:
			sum_arr.append(j)

	for k in range(1, len(arr)):
		sum_arr[k] = sum_arr[k] + sum_arr[k-1]

	count = 0
	for j in sum_arr:
		if j > 0:
			count += 1

	return count




print(getMinimumCost([-3,0,2,1]))