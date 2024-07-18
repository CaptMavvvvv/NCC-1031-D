one = int(input("Enter the score for test 1: "))
two = int(input("Enter the score for test 2: "))
three = int(input("Enter the score for test 3: "))
numlist = one + two + three
average = (numlist / 3)

print("Your average is ", average)
if average > 95:
    print("Congratulation!")