def change_cals(price, paid):

    change = paid - price
    print(f'Total change is: {change} baht')

    demominations = [1000, 500, 100, 50, 20, 10, 5, 2, 1]

    for demomination in demominations:
        count = change // demomination
        if count > 0:
            print(f'{demomination} baht: {count} piece')
            change %= demomination

price = float(input("Enter your goods price: "))
paid = float(input("Enter your paid: "))

change_cals(price, paid)