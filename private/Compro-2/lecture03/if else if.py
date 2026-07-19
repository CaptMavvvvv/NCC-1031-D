num_employs = int(input("Enter the number of employees: "))

if num_employs < 50:
    print("This is a small company")
elif num_employs < 250:
    print("This is a medium-size company")
elif num_employs >= 250:
    print("This is a large company")
    