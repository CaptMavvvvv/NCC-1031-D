start_num = int(input("Start num: "))
end_num = int(input("End num: "))

# Input for divisible number (condition)
divisible_by = int(input("Enter a number to divide by: "))

total_loops = 5  # Number of loops before asking the user

while True:
    count = 0
    for num in range(start_num + 1, end_num):
        if num % divisible_by == 0:
            print(f"Number: {num}")
            count += 1
        
        if count == total_loops:
            break

    # Ask user if they want to continue after 5 loops
    choice = int(input("Wanna continue or exit? (Exit=0, Continue=1): "))
    if choice == 0:
        print("Exiting the loop.")
        break
    elif choice == 1:
        continue
