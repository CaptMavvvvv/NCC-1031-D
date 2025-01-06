import time

def sum_even_odd(N):
    
    sum_even = (N // 2) * (N // 2 + 1)
    
    sum_odd = ((N + 1) // 2) ** 2

    return sum_odd, sum_even

start_time = time.time()

N = int(input("Enter N number: "))
sum_odd, sum_even = sum_even_odd(N)

end_time = time.time()

print(f'Sum of odd numbers = {sum_odd}')
print(f'Sum of even number = {sum_even}')

total = end_time - start_time

print(f'Total time used is {total}')