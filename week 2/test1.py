def change_calculator(price, paid):

    change = paid - price
    print(f'Your total change is {change} baht')

    dominations = [1000, 500, 100, 50, 20, 10, 5, 2, 1]

    for domination in dominations:
        count = change // domination
        if count > 0:
            print(f'{domination} baht: {count} piece')
        change %= domination

price = float(input("Enter you goods price: "))
paid = float(input("Enter your paid: "))

change_calculator(price, paid)