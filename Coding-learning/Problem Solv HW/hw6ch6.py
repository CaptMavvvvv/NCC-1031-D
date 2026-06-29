thai = {
    "ภาคเหนือ": ["เชียงใหม่", "เชียงราย", "ลำพูน", "ลำปาง"],
    "ภาคกลาง": ["กรุงเทพ", "นครปฐม", "สมุทรปราการ", "ลพบุรี"],
    "ภาคอีสาน": ["ขอนแก่น", "ศรีสะเกษ", "บุรีรัมย์", "อุบลราชธานี"],
    "ภาคใต้": ["สงขลา", "ตรัง", "พัทลุง", "ภูเก็ต"]
}
def menu():
    while True:
        print("\n-- menu --")
        print("1.เพิ่มจังหวัด")
        print("2.แก้ไขจังหวัด")
        print("3.ค้นหาจังหวัด")
        print("4.ลบจังหวัด")
        print("5.แสดงข้อมูลจังหวัดทั้งหมด")
        print("0.ออกจากโปรแกรม")

        choose = int(input("choose number:"))
        if choose == 1 :
            region = input("กรุณาป้อนชื่อภาค: ")
            province = input("กรุณาป้อนชื่อจังหวัด: ")
            thai.setdefault(region, []).append(province)
        elif choose == 2 :
            region = input("กรุณาป้อนชื่อภาค: ")
            old = input("กรุณาป้อนชื่อจังหวัดเดิม:")
            new = input("กรุณาป้อนชื่อจังหวัดใหม่:")
            if region in thai and old in thai[region]:
                thai[region][thai[region].index(old)] = new
        elif choose == 3 :
            province = input("กรุณาป้อนชื่อจังหวัดที่จะค้นหา: ")
            found = False
            for region, provinces in thai.items():
                if province in provinces:
                    print(f"{province} in {region}")
                    found = True
                    break
            if not found:
                print("ไม่พบข้อมูล")
        elif choose == 4 :
            region = input("กรุณาป้อนชื่อภาค: ")
            province = input("กรุณาป้อนชื่อจังหวัดที่จะลบ: ")
            if region in thai and province in thai[region]:
                thai[region].remove(province)
        elif choose == 5 :
            for region, provinces in thai.items():
                print(f"{region}: {', '.join(provinces)}")
        elif choose == 0 :
            break

menu()


# นา่ย ชยพัฒน์ วงษ์ทำมา
# นาย สุภชา เจริญสำเร็จกิจ

print(f"\n 1.InsertData\n 2.UpdateData\n 3.SearchData\n 4.DeleteData\n 5.ViewAllData")
thai_data = dict ( ภาคเหนือ= "เชียงใหม่ เชียงราย",
            ภาคตะวันออกเฉียงเหนือ= "อุดรธานี อุบลราชธานี", 
            ภาคกลาง= "นครสวรรค์ นครปฐม", 
            ภาคตะวันออก= "จันทบุรี ชลบุรี", 
            ภาคตะวันตก= "กาญจนบุรี ราชบุรี", 
            ภาคใต้= "กระบี่ ชุมพร")

while True:
    choice = input("ใส่หมายเลชตัวเลือก: ")
    if choice == '1':
        region = input("ใส่ภูมิภาค: ")
        if region in thai_data:
            province = input("ใส่จังหวัดที่จะเพิ่ม : ")
            thai_data[region] += " " + province
            print(f"เพิ่ม {province} ใน {region} แล้ว")

    elif choice == '2':
        region = input("ใส่ภูมิภาที่จะแก้ไข: ")
        if region in thai_data:
            province = input("ใส่จังหวัดที่จะแก้ไข: ")
            thai_data[region] = province
            print(f"แก้ไขข้อมูลในภาค{region}")

    elif choice == '3':
        region = input("ใส่ภูมิภาค: ")
        province = thai_data.get(region)
        print(province)

    elif choice == '4':
        region = input("ใส่ภูมิภาค: ")
        if region in thai_data:
            thai_data.pop(region)
            print(thai_data)
        else:
            print("ไม่พบภูมิภาค!!!")

    elif choice == '5':
        print(thai_data)
    else:
        print("ตัวเลือกไม่ถูกต้อง")
        break