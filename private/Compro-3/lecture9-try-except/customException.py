class NegativeNumberError(Exception):
    def __init__(self, value):
        self.value = value
        super().__init__(f'Invalid input')

def check_positive_number(num):
    if num < 0:
        raise NegativeNumberError(num)
    else:
        print(f'{num} is a valid')

try:
    number = int(input('Enter a positive number: '))
    check_positive_number(number)
except NegativeNumberError as e:
    print(e)
except ValueError:
    print('Error: Enter a valid number')
finally:
    print('Program execution finished')