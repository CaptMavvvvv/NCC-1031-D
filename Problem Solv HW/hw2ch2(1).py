N = int(input("Enter the number of Collagees: "))

count = 0

while count < N:
    score = int(input("Enter your score: "))
    if N == 0:
        break
    elif score >= 80:
        print("Your grade is A")
    elif score >= 75:
        print("Your grade is B+")
    elif score >= 70:
        print("Your grade is B")
    elif score >= 65:
        print("Your grade is C+")
    elif score >= 60:
        print("Your grade is C")
    elif score >= 55:
        print('Your grade is D+')
    elif score >= 50:
        print('Your grade is D')
    else:
        print('Your score is F')

    count += 1

print("All data has entered.")