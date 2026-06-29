def calculate_calories(): 
    results = []
    while True:
        time, type_ex = (int(input("Enter your exercise time in minute : "))), (int(input("Enter your exercise type (1:Running / 2:Cycling / 3:Swimming) : ")))

        if type_ex == 1:
            calories = time * 10
            results.append(f'Calories burn by running is {calories} calories.')
            print(f'Total calories by running : {calories} calories.')
        elif type_ex == 2:
            calories = time * 8
            results.append(f'Calories burn by cycling is {calories} calories.')
            print(f'Total calories by cycling : {calories} calories.')
        elif type_ex == 3:
            calories = time * 5
            results.append(f'Calories burn by swimming is {calories} calories.')
            print(f'Total calories by swimming : {calories} calories.')

        choice = (int(input('If ya want to stop > 0 / if not > 4 : ')))
        if choice == 0:
            print('EXITING THE LOOP')
            break
        elif choice == 4:
            continue
        
    print("\nSummary total calories")
    for result in results:
        print(result)

if __name__ == '__main__':
    calculate_calories()