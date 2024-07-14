import statistics

first = int(input("Enter the first test score: "))
second = int(input("Enter the second test score: "))
third = int(input("Enter the third test score: "))
num_list = [first, second, third]
average = statistics.mean(num_list)

print("The average score is ", format(int(average)))
if average >= 95:
    print("Congratulation!")