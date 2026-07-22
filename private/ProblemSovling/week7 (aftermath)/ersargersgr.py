def manage_student_scores():
    num_students = int(input("Enter the number of students: "))
    student_scores = {}

    for i in range(num_students):
        name = input(f"Enter the name of student {i+1}: ")
        score = float(input(f"Enter the score of student {i+1}: "))
        student_scores[name] = score

    sorted_scores = sorted(student_scores.items(), key=lambda item: item[1], reverse=True)

    print("\nScores sorted from highest to lowest:")
    for name, score in sorted_scores:
        print(f"{name}: {score}")

    print("\nTop 3 scores:")
    for i in range(min(3, len(sorted_scores))):
        name, score = sorted_scores[i]
        print(f"{name}: {score}")

    print("\nBottom 3 scores:")
    for i in range(max(0, len(sorted_scores) - 3), len(sorted_scores)):
        name, score = sorted_scores[i]
        print(f"{name}: {score}")

    search_score = float(input("\nEnter the score to search for: "))
    found_students = [name for name, score in student_scores.items() if score == search_score]

    if found_students:
        print(f"Found {len(found_students)} student(s) with score {search_score}:")
        for name in found_students:
            print(name)
    else:
        print(f"No students found with score {search_score}")
        
manage_student_scores()