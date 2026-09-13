attendance_week = [
    ["Alice", "Bob", "Charlie", "David"],
    ["Alice", "Charlie", "David"],
    ["Alice", "Bob", "Daviก"],
    ["Alice", "David", "Eve"],
    ["Bob", "Charlie", "David"]
]

attendance_sets = [set(day) for day in attendance_week]
print(attendance_sets)

present_every_day = set.intersection(*attendance_sets)
print(present_every_day)

all_students = set.union(*attendance_sets)
absent_at_least_one_day = all_students - present_every_day
print(absent_at_least_one_day)

first_day_present = attendance_sets[0]
last_day_present = attendance_sets[-1]
first_day_but_not_last = list(first_day_present - last_day_present)
print(first_day_but_not_last)

unique_students_count = len(all_students)
print(unique_students_count)