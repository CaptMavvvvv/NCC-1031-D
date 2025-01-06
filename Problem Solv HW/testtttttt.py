def calculate_gross(N):
    count = 0

    while count < N:
        count += 1
        print(f"\nProcessing Employee {count}")
        
        hour_rate = float(input("Enter employee's rate per hour: "))
        hour_work = float(input("Enter employee's hours of work: "))

        if hour_work <= 160:
            gross_pay = hour_rate * hour_work
        else:
            nor_rate = hour_rate * 160
            ot_hours = hour_work - 160
            ot_gross_pay = ot_hours * hour_rate * 1.5
            gross_pay = nor_rate + ot_gross_pay

        print(f"Employee {count}'s gross pay is {gross_pay:.2f} THB")
    
    print("\nAll data has been calculated.")

# Main Program
N = int(input("Enter employees count: "))
calculate_gross(N)
