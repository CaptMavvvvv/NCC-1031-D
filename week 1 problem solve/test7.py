print(f'Welcome to the Number guessing Game!')
print("I'm thinking of a number between 1 and 100. Can you guess it?")

import random

nums = random.randint(1, 100)
print(nums)
attempt = 0 #Set attempt to collect the data of attempt.
guess = None

while guess != nums:
    guess = int(input("Enter your guess: "))

    if guess == nums:
        print(f'Congrats! Your guess attempt is: {attempt}')
    elif guess < nums:
        print(f'Too low! Try again.')
    elif guess > nums:
        print(f'Too high! Try again.')