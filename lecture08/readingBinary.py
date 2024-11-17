import struct

with open("records.bin", "rb") as file:
    data = file.read(struct.calcsize('i20sif'))
    record = struct.unpack('i20sif', data)
    record = (record[0], record[1].decode().strip('\x00'), record[2], record[3])
    print(f"ID: {record[0]}, Name: {record[1]}, Age: {record[2]}, GPA: {record[3]}")