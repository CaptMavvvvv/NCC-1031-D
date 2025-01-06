start_num, end_num, divisible_by = int(input("Enter ur start number: ")), int(input("Enter ur end number: ")), int(input("Enter a number to divide by: "))

while True:
    count = 0
    num_list = [num for num in range(start_num+1, end_num) if num % divisible_by == 0]
    print(f"Number: {num_list}")
    count += 1
        
    choice = int(input("Wanna continue or exit? (Exit=0, Continue=1): "))
    if choice == 0:
        print("Exiting the loop.")
        break
    elif choice == 1:
        continue