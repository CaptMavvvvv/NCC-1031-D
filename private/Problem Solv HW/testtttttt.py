# โปรแกรมคำนวณการเผาผลาญแคลอรี่

def calculate_calories(activity, minutes):
    """
    คำนวณแคลอรี่ที่เผาผลาญ
    Parameters:
        activity (str): ประเภทการออกกำลังกาย ("Running", "Cycling", "Swimming")
        minutes (int): ระยะเวลา (นาที)
    Returns:
        int: แคลอรี่ที่เผาผลาญ
    """
    rates = {"Running": 10, "Cycling": 8, "Swimming": 5}
    return rates.get(activity, 0) * minutes

def main():
    print("\nโปรแกรมคำนวณแคลอรี่ที่เผาผลาญ")
    print("-----------------------------------")

    while True:
        activity = input("เลือกกิจกรรม (Running, Cycling, Swimming): ").capitalize()
        if activity not in ["Running", "Cycling", "Swimming"]:
            print("กิจกรรมไม่ถูกต้อง! ลองใหม่")
            continue

        minutes_input = input("ระยะเวลา (นาที): ")
        if not minutes_input.isdigit():
            print("กรุณากรอกตัวเลข! ลองใหม่")
            continue

        minutes = int(minutes_input)
        calories = calculate_calories(activity, minutes)
        print(f"คุณเผาผลาญ {calories} แคลอรี่ จากการ {activity} {minutes} นาที")

        with open("calorie_burn_log.txt", "a") as log:
            log.write(f"{activity}, {minutes} นาที, {calories} แคลอรี่\n")

        if input("คำนวณอีกครั้ง? (yes/no): ").lower() != "yes":
            print("ขอบคุณที่ใช้โปรแกรม!")
            break

if __name__ == "__main__":
    main()
