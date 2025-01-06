saving_tg, year_tg = int(input("Enter your saving target: ")), int(input("Enter your year target to saving: "))

choice = int(input("For Monthly press 0 or Daily press 1: "))
if choice == 0:
    calculate_month = saving_tg / 12
    print(calculate_month)
elif choice == 1:
    calculate_day = saving_tg / 365
    print(calculate_day)
