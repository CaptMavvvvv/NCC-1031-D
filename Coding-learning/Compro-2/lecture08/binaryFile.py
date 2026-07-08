import struct
num_records = int(input("How many records do you want to create? "))

with open("records.bin", "wb") as file:
    for _ in range(num_records):
        id_num = int(input("Enter ID: "))
        name = input("Enter Name: ")
        age = int(input("Enter Age: "))
        gpa = float(input("Enter GPA: "))

        data = struct.pack('i20sif', id_num, name.encode(), age, gpa())
        file.write(data)

print(f"{num_records} records have been written to records.bin")