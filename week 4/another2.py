start_num = int(input("S num: "))
end_num = int(input("E num: "))

count = 0

for i in range(start_num+1, end_num):
    if count % 3 == 0:
        print(count)