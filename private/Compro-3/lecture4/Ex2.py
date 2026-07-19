hoursWork, payRate = int(input("Enter the number of hours worked: ")), int(input(f'Enter the hourly pay rate: '))
if hoursWork <= 40:
    grossPay = hoursWork * payRate
    print(f'The gross pay is {grossPay}')
elif hoursWork > 40:
    ot_hours = hoursWork - 40 # เอามาแยกเป็นเวลาที่เกินมาจาก 40 hours
    ot_grossPay = (40 * payRate) + (ot_hours * payRate * 1.5)
    print(f'The gross pay is {ot_grossPay}')