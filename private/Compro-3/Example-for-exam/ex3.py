def find_single_occurrence_numbers(numbers: list) -> list:
    dup_num = {}
    result = []
    for i in numbers:
        if i in dup_num:
            dup_num[i] += 1
        else:
            dup_num[i] = 1

    for a,b in dup_num.items():
        if b == 1:
            result.append(a)
    return result

print(find_single_occurrence_numbers([4,5,6,4,7,5,8]))
print(find_single_occurrence_numbers([1,2,2,3,3,4,4]))
print(find_single_occurrence_numbers([1,2,3,4,5,6]))
print(find_single_occurrence_numbers([1,1,1,1,1,1]))