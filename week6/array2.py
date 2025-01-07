import numpy as np
import array as arr

number = arr.array('i', [50, 87, 65, 39])

print("Array before operations: ", number)

array_sum = np.sum(number)
array_avg = np.mean(number)

sorted_ascending = sorted(number)

sorted_descending = sorted(number, reverse=True)

search_num = 65
if search_num in number:
    print(f"Number {search_num} found at index {number.index(search_num)}")
else:
    print(f"Number {search_num} not found in the array.")

delete_num = 39 
if delete_num in number:
    number.remove(delete_num)
    print(f"Number {delete_num} deleted.")
else:
    print(f"Number {delete_num} not found, so it cannot be deleted.")

print(f"Array after deletion: {number}")
print(f"Sum of the array: {array_sum}")
print(f"Average of the array: {array_avg}")
print(f"Sorted (ascending): {sorted_ascending}")
print(f"Sorted (descending): {sorted_descending}")
