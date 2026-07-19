def calculate_savings(goal_amount, years, frequency):
    if frequency == 'daily':
        total_days = years * 365
        saving_per_day = goal_amount / total_days
        return saving_per_day
    elif frequency == 'monthly':
        total_months = years * 12
        saving_per_month = goal_amount / total_months
        return saving_per_month
    else:
        return "Invalid frequency. Please choose 'daily' or 'monthly'."

def main():
    goal_amount = float(input("Enter the total amount you want to save: "))
    years = int(input("Enter the number of years you want to save: "))
    frequency = input("Do you want to save 'daily' or 'monthly'? ").strip().lower()

    savings_needed = calculate_savings(goal_amount, years, frequency)
    if isinstance(savings_needed, str):
        print(savings_needed)
    else:
        if frequency == 'daily':
            print(f"You need to save {savings_needed:.2f} each day to reach your goal of {goal_amount} in {years} years.")
        elif frequency == 'monthly':
            print(f"You need to save {savings_needed:.2f} each month to reach your goal of {goal_amount} in {years} years.")

if __name__ == "__main__":
    main()