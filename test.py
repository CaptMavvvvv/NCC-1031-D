# Sample data structure for employee performance
performance_data = {
    "Sales": {
        "Alice": [80, 85, 88, 90],
        "Bob": [70, 75, 78, 80],
        "Charlie": [60, 65, 70, 72],
    },
    "Engineering": {
        "David": [90, 92, 94, 95],
        "Eve": [85, 88, 87, 90],
        "Frank": [88, 87, 86, 85],
    },
    "HR": {
        "Grace": [70, 72, 74, 76],
        "Heidi": [65, 68, 70, 73],
        "Ivan": [60, 62, 64, 66]
    }
}

# --- 1. คำนวณคะแนนเฉลี่ยของพนักงานแต่ละคน ---
employee_averages = {}
for department, employees in performance_data.items():
    employee_averages[department] = {}
    for employee, scores in employees.items():
        if scores:  # ตรวจสอบว่ามีคะแนนหรือไม่ เพื่อป้องกันหารด้วยศูนย์
            average_score = sum(scores) / len(scores)
            employee_averages[department][employee] = round(average_score, 2)

# --- 2. หาพนักงานที่มีผลงานดีที่สุดในแต่ละแผนก ---
top_performers = {}
for department, employees in employee_averages.items():
    # ใช้ max() เพื่อหาชื่อพนักงานที่มีคะแนนเฉลี่ยสูงสุด
    top_employee = max(employees, key=employees.get)
    # ดึงคะแนนสูงสุดจากชื่อพนักงานที่หาได้
    top_score = employees[top_employee]
    top_performers[department] = {
        "name": top_employee,
        "score": top_score
    }

# --- 3. หาแผนกที่มีคะแนนเฉลี่ยสูงสุด ---
department_scores = {}
for department, employees in performance_data.items():
    total_scores = 0
    total_count = 0
    for scores in employees.values():
        total_scores += sum(scores)
        total_count += len(scores)
    
    if total_count > 0:
        department_scores[department] = total_scores / total_count
    
# หาแผนกที่มีคะแนนเฉลี่ยรวมสูงสุดจาก Dictionary ที่สร้างขึ้น
best_department = max(department_scores, key=department_scores.get)
best_department_score = department_scores[best_department]

# --- 4. หาพนักงานที่คะแนนดีขึ้นอย่างต่อเนื่อง ---
improving_employees = []
for department, employees in performance_data.items():
    for employee, scores in employees.items():
        is_improving = True
        for i in range(1, len(scores)):
            # ถ้าคะแนนลดลงแม้แต่ครั้งเดียว ถือว่าไม่ใช่
            if scores[i] < scores[i-1]:
                is_improving = False
                break # หยุดการตรวจสอบของพนักงานคนนี้ทันที
        
        if is_improving:
            improving_employees.append(employee)

# --- 5. แสดงผลลัพธ์ทั้งหมด ---
print("--- Performance Analysis Report ---")

print("\n1. คะแนนเฉลี่ยของพนักงานแต่ละคน:")
for department, employees in employee_averages.items():
    print(f"  แผนก: {department}")
    for employee, avg_score in employees.items():
        print(f"    - {employee}: {avg_score}")

print("\n2. พนักงานที่ผลงานดีที่สุดในแต่ละแผนก:")
for department, data in top_performers.items():
    print(f"  - {department}: {data['name']} (คะแนน: {data['score']})")

print(f"\n3. แผนกที่มีคะแนนเฉลี่ยสูงสุด:")
print(f"  - {best_department} (คะแนนเฉลี่ย: {round(best_department_score, 2)})")

print("\n4. พนักงานที่มีผลงานดีขึ้นอย่างต่อเนื่อง:")
if improving_employees:
    print(f"  - {', '.join(improving_employees)}")
else:
    print("  - ไม่มี")
    
print("\n--- End of Report ---")