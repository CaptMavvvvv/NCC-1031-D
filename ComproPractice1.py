def find_single_occurrence_numbers(numbers: list) -> list:
    from collections import defaultdict
    count = defaultdict(int)
    multiple_occurrence = set()
    
    for number in numbers:
        count[number] += 1

    for number in count:
        if count[number] > 1:
            multiple_occurrence.add(number)
    
    single_occurrence = [number for number in numbers if count[number] == 1]
    result = [number for number in single_occurrence if number not in multiple_occurrence]

    return result

print(find_single_occurrence_numbers([4, 5, 6, 4, 7, 5, 8]))
print(find_single_occurrence_numbers([1, 2, 2, 3, 3, 4, 4]))
print(find_single_occurrence_numbers([1, 2, 3, 4, 5, 6]))
print(find_single_occurrence_numbers([1, 1, 1, 1, 1]))