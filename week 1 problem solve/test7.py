import random

def random_number():

    print(f'Welcome to the Number guessing Game!')
    print("I'm thinking of a number between 1 and 100. Can you guess it?")

    nums = random.randint(1, 100)
    attempt = 0

    while True:
        guess = int(input("Enter your guess: "))
        attempt += 1

        if guess == nums:
            print(f'Congrats! You guess number in {attempt} attempt.')
            break
        elif guess > nums:
            print("Too high! Try again.")
        else:
            print("Too low! Try again.")

print("That is the end of the game!")

random_number()