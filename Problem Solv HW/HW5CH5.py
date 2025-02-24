def selection_sort(students):
    n = len(students)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if students[j][1] < students[min_idx][1]:
                min_idx = j
        students[i], students[min_idx] = students[min_idx], students[i]

def main():
    num_students = int(input("ระบุจำนวนนักศึกษา: "))
    students = []

    for i in range(num_students):
        name = input(f"ป้อนชื่อนักศึกษาคนที่ {i+1}: ")
        score = float(input(f"ป้อนคะแนนของ {name}: "))
        students.append((name, score))

    selection_sort(students)

    print("\nคะแนนทั้งหมดจากมากไปน้อย:")
    for name, score in reversed(students):
        print(f"{name}: {score}")

    print("\nTop 3 นักศึกษาที่ได้คะแนนสูงสุด:")
    for i in range(min(3, len(students))):
        name, score = students[len(students) - 1 - i] 
        print(f"{name}: {score}")

    print("\nTop 3 นักศึกษาที่ได้คะแนนน้อยสุด:")
    for i in range(min(3, len(students))):
        name, score = students[i]
        print(f"{name}: {score}")

    search_score = float(input("\nป้อนคะแนนที่ต้องการค้นหา: "))
    found_count = 0
    found_names = []

    for name, score in students:
        if score == search_score:
            found_count += 1
            found_names.append(name)

    if found_count > 0:
        print(f"พบนักศึกษาที่ได้คะแนน {search_score} จำนวน {found_count} คน:")
        for name in found_names:
            print(name)
    else:
        print(f"ไม่พบนักศึกษาที่ได้คะแนน {search_score}")

if __name__ == "__main__":
    main()

### นายสุภชา เจริญสำเร็จกิจ INE 6706022610241 ###