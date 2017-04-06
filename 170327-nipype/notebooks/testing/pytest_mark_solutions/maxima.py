def find_maxima(list_of_numbers):
    maxima = []
    if list_of_numbers[0] > list_of_numbers[1]:
        maxima.append(0)
    for i in range(1, len(list_of_numbers)-1):
        if list_of_numbers[i-1] < list_of_numbers[i] > list_of_numbers[i+1]:
                maxima.append(i)
    if list_of_numbers[-1] > list_of_numbers[-2]:
        maxima.append(len(list_of_numbers)-1)
    return maxima
