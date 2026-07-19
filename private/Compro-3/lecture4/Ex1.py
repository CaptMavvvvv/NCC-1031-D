firstScore, secondScore, thirdScore = int(input("Enter the score for test 1: ")), int(input("Enter the score for test 2: ")), int(input("Enter the score for test 3: "))
average = (firstScore + secondScore + thirdScore) / 3
print(f'The average score is {average:.1f}')
if average >= 95:
    print(f'Congratulation !')
    print(f'This is great average.')